# Jarvis Assistant 🧠

A fully offline-capable, sarcastic, highly customizable AI assistant — inspired by Iron Man’s JARVIS — built for Raspberry Pi.  
Made by [Krisztian Nagy @ Studio MirAI](https://studiomirai.co.uk)

---

## 🚀 Features

- 🎙️ Wake word + offline speech recognition (Vosk or Whisper)
- 🤖 ChatGPT integration with pre/post prompt modifiers
- 🎭 Multiple personalities: each with their own face, voice, and flair
- 📺 Video states: idle, listening, thinking, talking, paranoid, panic, dreaming
- 🗣️ Text-to-Speech via eSpeak, eSpeak-NG, or gTTS
- 💬 Dictation mode or AI-composed email mode
- 📅 Calendar access with Google Auth
- 📡 Bluetooth file transfer + email support
- 🎛️ Web-based admin panel (mobile-optimized)
- 🔒 Voice-based intruder detection + 30min guest override
- 🌙 Dream Mode (quirky musings after inactivity)
- 🧠 Habit Engine: learns your routines and makes suggestions
- 😈 Mood Detector: responds with empathy or snark based on how you speak
- 🎉 Protocols: control groups of IoT devices by voice
- 🪞 Holographic Mode: flips display for mirrored projection
- 🐶 Bark Wakeup: detects dog barking and reacts with random fun responses
- 🎵 Voice-controlled music playback from YouTube (others coming soon)

---

## 🧰 Hardware Tested On

- Raspberry Pi 5 (recommended)
- Raspberry Pi 3B (minimum)
- 5-inch portrait touchscreen (800x480px)
- WM8960 audio module

---

## ⚙️ Installation (on Raspberry Pi)

### 1. Run the install script

```bash
chmod +x install.sh
./install.sh
```

This will:
- Install all dependencies
- Set up a Python virtual environment
- Download Whisper base model
- Create required folders
- Register the systemd service for autostart

### 2. Optional: Enable GUI launcher at boot

```bash
chmod +x install_desktop_launcher.sh
./install_desktop_launcher.sh
```

---

## 🔧 Admin Panel

Access: `http://<your-pi-ip>:5000`  
Default login:  
- Username: `admin`  
- Password: `tonystark`

From here, you can:
- Edit TTS/STT, voice config, assistant name & title
- Upload/download backups
- Add or remove Whisper models
- Set dream/paranoid timing
- Change how Jarvis addresses you
- Select or manage personalities
- Control IoT devices (via Protocols)
- Upload logos & configure holographic mode
- Enter API keys (OpenAI, Auth0, etc.)

---

## 💬 Voice Commands

> Replace “Jarvis” with your assistant's configured name

- “Jarvis, change your attitude” → switches personality
- “Jarvis, what’s with the attitude” → same as above
- “Jarvis, be nice to our guest” → disables intruder detection for 30 mins
- “Jarvis, activate holographic mode” → flips display for mirror projection
- “Check my calendar” → reads today’s events
- “Send an email to Emma Stone…” → verbatim email
- “Write an email to Emma Stone…” → AI-composed email
- “Jarvis, volume 80” → sets system volume
- “Jarvis, blast it” → switch to headphone output
- “Activate protocol MovieTime” → turns on a group of IoT devices
- (bark sound) → wakes Jarvis with “Can I pet that daawg?” or similar

---

## 📦 Folder Structure

```
jarvis/
├── assets/
│   ├── easter_eggs/
│   │   └── bark_responses.json
│   ├── qr/
│   │   └── logo.png
│   └── video/
├── backup/
├── config/
│   ├── config.json
│   └── config_default.json
├── features/
│   ├── __init__.py
│   ├── bark_detector.py
│   ├── dream_mode.py
│   ├── email_calendar.py
│   ├── habit_engine.py
│   ├── holographic_mode.py
│   ├── intruder_detection.py
│   ├── mood_detector.py
│   ├── panic_mode.py
│   ├── paranoid_mode.py
│   ├── personality_manager.py
│   ├── personality_selector.py
│   └── smart_room.py
├── personalities/
│   ├── custompersonality/
│   ├── personality01/
│   └── personality02/
├── static/
│   ├── login_background.mp4
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
├── templates/
│   ├── index.html
│   └── login.html
├── admin_routes.py
├── admin_util_routes.py
├── backup.sh
├── config_manager.py
├── install.sh
├── install_desktop_launcher.sh
├── main.py
├── setup.desktop
├── setup_tts_stt_whisper.sh
├── speech_to_text.py
├── text_to_speech.py
├── update.sh
├── video_manager.py
└── web_admin.py
```

---

## 🔁 Updating Jarvis

```bash
cd ~/jarvis-assistant
git pull
./install.sh
```

Or use the admin panel’s update/check feature.

---

## 🧪 Testing Locally (on the Pi)

```bash
source venv/bin/activate
python main.py
```

---

## 📩 Transferring Files from Mac

```bash
scp file.jpg pi@<your-pi-ip>:/home/pi/jarvis-assistant/assets/
```

Or to sync everything:

```bash
rsync -av ./assets/ pi@<your-pi-ip>:/home/pi/jarvis-assistant/assets/
```

---

Built with passion, sarcasm, and an unhealthy love for Iron Man.  
Made for real homes, demo flair, and futuristic interfaces.

Stay shiny, Mr. Stark.
