import pymumble_py3 as pymumble
import time
import os
import re

SERVER = "127.0.0.1"
PORT = 64738
USERNAME = "SoundBot"

SOUNDS = {
    "!boom": "sounds/boom.wav"
}

def strip_html(text):
    message = text.message.strip()
    message = re.sub('<[^<]+?>', '', message)
    return message

def message_received(text):
    message = strip_html(text)

    print("Message: " + message)
    if message in SOUNDS:
        print(f"Playing sound for {message}")
        play_sound(SOUNDS[message])

def play_sound(file_path):
    with open(file_path, 'rb') as f:
        mumble.sound_output.add_sound(f.read())

# Connect to Mumble
mumble = pymumble.Mumble(SERVER, USERNAME, password="charliemumbles", port=PORT)
mumble.start()
mumble.is_ready()

# Register callback
mumble.callbacks.set_callback(
    pymumble.constants.PYMUMBLE_CLBK_TEXTMESSAGERECEIVED,
    message_received
)

print("Soundboard bot running...")
while True:
    time.sleep(1)

