Here’s a clean, professional `README.md` you can use for your project:

---

# 🎧 PyMumble Soundboard Bot

A simple **Mumble soundboard bot** built with Python 3.11.7 using `pymumble_py3`.
The bot listens for chat commands and plays `.wav` sound effects into the voice channel.

---

## ✨ Features

* Connects to a Mumble server
* Listens for text chat messages
* Plays sound effects when specific commands are triggered
* Logs activity to both console and `soundbot.log`
* Graceful shutdown with `Ctrl+C`

---

## 📦 Requirements

* Python **3.11.7**
* Mumble server
* Virtual environment (recommended)
* `pymumble_py3`

---

## 🚀 Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/pymumble-soundboard.git
cd pymumble-soundboard
```

---

### 2️⃣ Create Virtual Environment

```bash
python3.11 -m venv .
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install pymumble-py3
```

---

### 4️⃣ Project Structure

```
pymumble-soundboard/
│
├── sounds/
│   └── boom.wav
│
├── soundbot.log
├── soundbot.py
└── README.md
```

---

## ⚙️ Configuration

Edit these values in `soundbot.py`:

```python
SERVER = "127.0.0.1"
PORT = 64738
USERNAME = "SoundBot"
```

Update the password here:

```python
mumble = pymumble.Mumble(SERVER, USERNAME, password="yourpassword", port=PORT)
```

---

## 🎵 Adding Sounds

Modify the `SOUNDS` dictionary:

```python
SOUNDS = {
    "!boom": "sounds/boom.wav",
    "!airhorn": "sounds/airhorn.wav"
}
```

* The **key** is the chat command.
* The **value** is the file path to the `.wav` file.

When a user types:

```
!boom
```

The bot will play `boom.wav` in the channel.

---

## ▶️ Running the Bot

```bash
python soundbot.py
```

If successful, you should see:

```
Connecting to Mumble server...
Connected and ready.
Soundboard bot running...
```

---

## 📝 Logging

The bot logs to:

* Console output
* `soundbot.log` file

Logs include:

* Received messages
* Triggered sounds
* Errors
* Shutdown events

---

## 🛑 Stopping the Bot

Press:

```
Ctrl + C
```

The bot will:

* Disconnect from the server
* Log shutdown status
* Exit cleanly

---

## 🔒 Security Notes

⚠️ Do NOT hardcode production passwords in source files.
Instead, consider using:

* Environment variables
* A `.env` file
* Configuration files excluded via `.gitignore`

Example:

```python
import os
PASSWORD = os.getenv("MUMBLE_PASSWORD")
```

---

## 🛠 Troubleshooting

**Bot connects but no sound plays**

* Ensure `.wav` files exist
* Verify correct file path
* Check server permissions (Transmit audio allowed)

**Connection fails**

* Verify server IP and port
* Confirm password
* Ensure Mumble server is running

---

## 📜 License

MIT License (or your preferred license)

---

## 🤖 Future Improvements

* Slash-style commands
* Volume control
* Per-channel restrictions
* Sound queue system
* Web dashboard
* Docker support

---

If you'd like, I can also generate:

* A version with badges
* A Dockerized version
* A `.env` configuration refactor
* A more production-ready structure
* GitHub Actions CI config

