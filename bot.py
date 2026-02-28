import pymumble_py3 as pymumble
import time
import re
import logging
import sys
from pathlib import Path

SERVER = "127.0.0.1"
PORT = 64738
USERNAME = "SoundBot"
PASSWORD = "password"

SOUNDS_DIR = Path(__file__).resolve().parent / "sounds"
SOUND_EXT = ".wav"

# Accept commands like !boom, !air-horn_2, etc.
COMMAND_RE = re.compile(r"^!([A-Za-z0-9][A-Za-z0-9_-]{0,63})$")

ADMIN_MESSAGE = (
    "To add/remove/rename sounds, visit home.nickabboud.com/soundboard. "
    "Username: leave blank. Password: same as server password."
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("soundbot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

_sound_cache = {
    "dir_mtime_ns": None,
    "names": [],      # list[str] of stems
    "paths": {},      # stem -> Path
}


def strip_html(msg: str) -> str:
    msg = msg.strip()
    msg = re.sub(r"<[^<]+?>", "", msg)
    return msg


def refresh_sound_cache_if_needed() -> None:
    try:
        st = SOUNDS_DIR.stat()
    except FileNotFoundError:
        _sound_cache["dir_mtime_ns"] = None
        _sound_cache["names"] = []
        _sound_cache["paths"] = {}
        return

    mtime_ns = getattr(st, "st_mtime_ns", int(st.st_mtime * 1e9))
    if _sound_cache["dir_mtime_ns"] == mtime_ns:
        return

    paths = {}
    names = []

    try:
        for entry in SOUNDS_DIR.iterdir():
            if entry.is_file() and entry.suffix.lower() == SOUND_EXT:
                stem = entry.stem
                if COMMAND_RE.match(f"!{stem}"):
                    names.append(stem)
                    paths[stem] = entry
    except Exception as e:
        logger.error(f"Failed to scan sounds dir {SOUNDS_DIR}: {e}")
        names, paths = [], {}

    names.sort()
    _sound_cache["dir_mtime_ns"] = mtime_ns
    _sound_cache["names"] = names
    _sound_cache["paths"] = paths

    logger.info(f"Sound cache refreshed: {len(names)} sound(s) available")


def sounds_help_text() -> str:
    refresh_sound_cache_if_needed()
    if not _sound_cache["names"]:
        return "Available sounds: (none found in sounds/)"
    parts = ["Available sounds:"]
    parts.extend(f"!{stem}" for stem in _sound_cache["names"])
    return " ".join(parts)


def reply_in_same_context(text_msg, reply: str) -> None:
    actor = getattr(text_msg, "actor", None)
    channel_ids = list(getattr(text_msg, "channel_id", []))
    tree_ids = list(getattr(text_msg, "tree_id", []))

    try:
        # DM context
        if len(channel_ids) == 0 and len(tree_ids) == 0:
            if actor is None:
                return
            mumble.users[actor].send_text_message(reply)
            return

        # Channel / tree context
        for cid in channel_ids:
            try:
                mumble.channels[cid].send_text_message(reply)
            except Exception as e:
                logger.error(f"Failed to send to channel_id={cid}: {e}")

        for tid in tree_ids:
            try:
                mumble.channels[tid].send_text_message(reply)
            except Exception as e:
                logger.error(f"Failed to send to tree_id={tid}: {e}")

    except Exception as e:
        logger.error(f"Failed to reply in context: {e}")


def reply_in_same_context_many(text_msg, replies) -> None:
    for r in replies:
        if r:
            reply_in_same_context(text_msg, r)


def play_sound_file(path: Path) -> None:
    try:
        with path.open("rb") as f:
            mumble.sound_output.add_sound(f.read())
        logger.info(f"Sound queued: {path}")
    except Exception as e:
        logger.error(f"Failed to play sound {path}: {e}")


def message_received(text_msg) -> None:
    raw = getattr(text_msg, "message", "")
    message = strip_html(raw)

    channel_ids = list(getattr(text_msg, "channel_id", []))
    tree_ids = list(getattr(text_msg, "tree_id", []))
    dm = (len(channel_ids) == 0 and len(tree_ids) == 0)

    logger.info(f"TextMessage: dm={dm} msg={message!r}")

    # If it's a DM and doesn't start with "!", send the list + admin info
    # (only in this circumstance)
    if dm and not message.startswith("!"):
        reply_in_same_context_many(text_msg, [sounds_help_text(), ADMIN_MESSAGE])
        return

    # From here down: only handle proper !commands
    m = COMMAND_RE.match(message)
    if not m:
        return  # ignore malformed commands (including "!" alone)

    cmd = m.group(1)

    # !help: send list + admin info (DM or channel, same context)
    if cmd == "help":
        reply_in_same_context_many(text_msg, [sounds_help_text(), ADMIN_MESSAGE])
        return

    refresh_sound_cache_if_needed()
    path = _sound_cache["paths"].get(cmd)

    if path and path.exists():
        play_sound_file(path)
        return

    reply_in_same_context_many(
        text_msg,
        [
            f"Unknown sound: !{cmd}.",
            sounds_help_text(),
        ],
    )


logger.info("Connecting to Mumble server...")
mumble = pymumble.Mumble(SERVER, USERNAME, password=PASSWORD, port=PORT)
mumble.start()
mumble.is_ready()
logger.info("Connected and ready.")

# IMPORTANT: constants are on the pymumble_py3 module, not the mumble instance
mumble.callbacks.set_callback(
    pymumble.constants.PYMUMBLE_CLBK_TEXTMESSAGERECEIVED,
    message_received,
)

logger.info("Soundboard bot running...")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    logger.info("Ctrl+C detected. Shutting down...")
    try:
        mumble.stop()
        logger.info("Disconnected from Mumble server.")
    except Exception as e:
        logger.error(f"Error during disconnect: {e}")
    logger.info("Shutdown complete.")
    sys.exit(0)
