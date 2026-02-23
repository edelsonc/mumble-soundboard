import pymumble_py3 as pymumble
import time
import os
import re
import logging

SERVER = "127.0.0.1"
PORT = 64738
USERNAME = "SoundBot"

SOUNDS = {
    "!boom": "sounds/boom.wav"
}

# ----------------------
# Logging Configuration
# ----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("soundbot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def strip_html(text):
    message = text.message.strip()
    message = re.sub('<[^<]+?>', '', message)
    return message

def message_received(text):
    message = strip_html(text)

    logger.info(f"Message received: {message}")

    if message in SOUNDS:
        logger.info(f"Playing sound for command: {message}")
        play_sound(SOUNDS[message])

def play_sound(file_path):
    try:
        with open(file_path, 'rb') as f:
            mumble.sound_output.add_sound(f.read())
        logger.info(f"Sound played: {file_path}")
    except Exception as e:
        logger.error(f"Failed to play sound {file_path}: {e}")

# Connect to Mumble
logger.info("Connecting to Mumble server...")
mumble = pymumble.Mumble(SERVER, USERNAME, password="charliemumbles", port=PORT)
mumble.start()
mumble.is_ready()
logger.info("Connected and ready.")

# Register callback
mumble.callbacks.set_callback(
    pymumble.constants.PYMUMBLE_CLBK_TEXTMESSAGERECEIVED,
    message_received
)

logger.info("Soundboard bot running...")

while True:
    time.sleep(1)
