#!/bin/bash

set -e

JARVIS_DIR="$HOME/jarvis"
VENV_DIR="$JARVIS_DIR/venv"
CURRENT_USER=$(whoami)
CONFIG_FILE="$JARVIS_DIR/config/config.json"

echo "🔧 Updating system and installing base dependencies..."
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
  python3 python3-pip python3-venv \
  mpv portaudio19-dev libasound2-dev \
  libffi-dev python3-dev build-essential \
  feh ffmpeg git wget curl unzip \
  pulseaudio pulseaudio-module-bluetooth bluez mpg123

echo "📁 Ensuring Jarvis directory exists..."
mkdir -p "$JARVIS_DIR"

cd "$JARVIS_DIR"

echo "🐍 Creating Python virtual environment (if needed)..."
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

echo "🚀 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install flask pyttsx3 pynput openai vosk \
  SpeechRecognition pyaudio faster-whisper \
  sounddevice soundfile \
  google-auth google-auth-oauthlib google-api-python-client \
  requests

echo "📁 Creating folder structure..."
mkdir -p config backup features assets/qr assets/video assets/easter_eggs personalities static/js static/css templates
touch features/__init__.py

if [ ! -f "$CONFIG_FILE" ]; then
  echo "⚙️ Copying default config..."
  cp config_default.json "$CONFIG_FILE"
fi

echo "🎙️ Injecting ElevenLabs-compatible text_to_speech.py..."
cat <<'EOF' > "$JARVIS_DIR/text_to_speech.py"
import os
import tempfile
import requests
import subprocess
import pyttsx3
from config_manager import load_config

def is_online():
    try:
        return os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1") == 0
    except:
        return False

def is_bluetooth_audio_connected():
    try:
        sinks = subprocess.check_output(["pactl", "list", "short", "sinks"]).decode()
        return "bluez_sink" in sinks
    except:
        return False

def play_audio(path):
    if is_bluetooth_audio_connected():
        os.system(f"paplay {path}")
    else:
        os.system(f"mpg123 {path}")

def speak_text(text):
    config = load_config()
    engine_preference = config.get("tts_engine", "elevenlabs")
    fallback = config.get("fallback_tts_engine", "pyttsx3")
    tts_settings = config.get("tts_settings", {})
    online = is_online()
    selected_engine = engine_preference if online else fallback

    if selected_engine == "elevenlabs":
        try:
            eleven = tts_settings.get("elevenlabs", {})
            api_key = eleven.get("api_key")
            voice_id = eleven.get("voice_id")
            if not api_key or not voice_id:
                raise ValueError("Missing ElevenLabs API key or voice ID.")
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                fp.write(response.content)
            play_audio(fp.name)
            os.remove(fp.name)
        except Exception as e:
            print("[ERROR] ElevenLabs failed:", e)
    else:
        try:
            settings = tts_settings.get("pyttsx3", {})
            rate = settings.get("rate", 170)
            volume = settings.get("volume", 1.0)
            voice_id = settings.get("voice_id", 0)
            engine = pyttsx3.init()
            engine.setProperty("rate", rate)
            engine.setProperty("volume", volume)
            voices = engine.getProperty("voices")
            if 0 <= voice_id < len(voices):
                engine.setProperty("voice", voices[voice_id].id)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("[ERROR] pyttsx3 failed:", e)

if __name__ == '__main__':
    speak_text("Hello, MR. Stark. ElevenLabs voice is ready.")
EOF

echo "🧠 Updating config for ElevenLabs..."
if grep -q '"tts_engine":' "$CONFIG_FILE"; then
  sed -i 's/"tts_engine": *"[^"]*"/"tts_engine": "elevenlabs"/' "$CONFIG_FILE"
else
  sed -i '1s/^/{\n  "tts_engine": "elevenlabs",\n/' "$CONFIG_FILE"
fi

if ! grep -q '"tts_settings":' "$CONFIG_FILE"; then
  sed -i "/\"voice_settings\": {/a \  },\n  \"tts_settings\": {\n    \"elevenlabs\": {\n      \"api_key\": \"REPLACE_ME\",\n      \"voice_id\": \"REPLACE_ME\"\n    },\n    \"pyttsx3\": {\n      \"rate\": 170,\n      \"volume\": 1.0,\n      \"voice_id\": 0\n    }\n  }," "$CONFIG_FILE"
fi

echo "📥 Downloading Whisper base.en model..."
mkdir -p ~/.cache/whisper/base.en
cd ~/.cache/whisper/base.en
wget -nc https://huggingface.co/guillaumekln/faster-whisper-base.en/resolve/main/model.bin -O model.bin || true
cd "$JARVIS_DIR"

echo "🗣️ Downloading and setting up Vosk model..."
VOSK_DIR="$JARVIS_DIR/vosk_model"
mkdir -p "$VOSK_DIR"
cd "$VOSK_DIR"
wget -nc https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -O model.zip
unzip -o model.zip
mv -n vosk-model-small-en-us-0.15/* . || true
rmdir vosk-model-small-en-us-0.15 || true
rm -f model.zip
cd "$JARVIS_DIR"

echo "🔗 Creating bluetooth_auto_connect.sh..."
cat <<EOF > "$JARVIS_DIR/bluetooth_auto_connect.sh"
#!/bin/bash
echo "🔄 Auto-connecting to trusted Bluetooth devices..."
bluetoothctl devices | while read -r _ MAC _; do
  echo "🔍 Connecting \$MAC..."
  bluetoothctl connect "\$MAC"
done
sleep 3
SINK=\$(pactl list short sinks | grep bluez_sink | awk '{print \$2}' | head -n 1)
if [ -n "\$SINK" ]; then
  pactl set-default-sink "\$SINK"
else
  echo "⚠️ No Bluetooth sink found."
fi
EOF

chmod +x "$JARVIS_DIR/bluetooth_auto_connect.sh"

echo "📎 Ensuring bluetooth auto-connect runs at boot..."
RC_FILE="/etc/rc.local"
if [ ! -f "$RC_FILE" ]; then
  echo -e "#!/bin/bash\nexit 0" | sudo tee "$RC_FILE" > /dev/null
  sudo chmod +x "$RC_FILE"
fi

if ! grep -q "bluetooth_auto_connect.sh" "$RC_FILE"; then
  sudo sed -i "/^exit 0/i $JARVIS_DIR/bluetooth_auto_connect.sh &" "$RC_FILE"
  echo "✅ Added to rc.local."
fi

echo "🛠 Creating systemd service for Jarvis..."
SERVICE_FILE="/etc/systemd/system/jarvis.service"
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Jarvis Assistant
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/python $JARVIS_DIR/main.py
WorkingDirectory=$JARVIS_DIR
Restart=always
User=$CURRENT_USER
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

echo "🔁 Enabling systemd service..."
sudo systemctl daemon-reexec
sudo systemctl enable jarvis.service

echo -e "\n✅ Jarvis is installed and ready to rock."
echo "Use 'sudo systemctl start jarvis' or just reboot." 
