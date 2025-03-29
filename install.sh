#!/bin/bash

set -e

JARVIS_DIR="$HOME/jarvis"
VENV_DIR="$JARVIS_DIR/venv"
CURRENT_USER=$(whoami)

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
pip install flask pyttsx3 pynput openai gtts vosk \
  SpeechRecognition pyaudio faster-whisper \
  sounddevice soundfile \
  google-auth google-auth-oauthlib google-api-python-client
  

echo "📁 Creating folder structure..."
mkdir -p config backup features assets/qr assets/video assets/easter_eggs personalities static/js static/css templates
touch features/__init__.py

if [ ! -f "config/config.json" ]; then
  echo "⚙️ Copying default config..."
  cp config_default.json config/config.json
fi

# 🗣️ Set TTS engine to gTTS
echo "🎤 Setting TTS engine to gTTS in config..."
CONFIG_FILE="$JARVIS_DIR/config/config.json"
if grep -q '"tts_engine":' "$CONFIG_FILE"; then
  sed -i 's/"tts_engine": *"[^"]*"/"tts_engine": "gtts"/' "$CONFIG_FILE"
else
  sed -i '1s/^/{\n  "tts_engine": "gtts",\n/' "$CONFIG_FILE"
fi

echo "🧠 Downloading Whisper base.en model..."
mkdir -p ~/.cache/whisper/base.en
cd ~/.cache/whisper/base.en
wget -nc https://huggingface.co/guillaumekln/faster-whisper-base.en/resolve/main/model.bin -O model.bin || true
cd "$JARVIS_DIR"

echo "🔗 Creating bluetooth_auto_connect.sh script..."
cat <<EOF > "$JARVIS_DIR/bluetooth_auto_connect.sh"
#!/bin/bash
echo "🔄 Auto-connecting to trusted Bluetooth devices..."
bluetoothctl devices | while read -r _ MAC _; do
  echo "🔍 Checking \$MAC..."
  bluetoothctl connect "\$MAC"
done
sleep 3
SINK=\$(pactl list short sinks | grep bluez_sink | awk '{print \$2}' | head -n 1)
if [ -n "\$SINK" ]; then
  echo "🎧 Setting default sink to \$SINK"
  pactl set-default-sink "\$SINK"
else
  echo "⚠️ No active Bluetooth sink found."
fi
EOF

chmod +x "$JARVIS_DIR/bluetooth_auto_connect.sh"

echo "📎 Adding bluetooth auto-connect to /etc/rc.local..."
RC_FILE="/etc/rc.local"
if [ ! -f "$RC_FILE" ]; then
  echo -e "#!/bin/bash\nexit 0" | sudo tee "$RC_FILE" > /dev/null
  sudo chmod +x "$RC_FILE"
fi

if ! grep -q "bluetooth_auto_connect.sh" "$RC_FILE"; then
  sudo sed -i "/^exit 0/i $JARVIS_DIR/bluetooth_auto_connect.sh &" "$RC_FILE"
  echo "✅ Added bluetooth auto-connect command to rc.local."
else
  echo "ℹ️ bluetooth_auto_connect.sh already in rc.local."
fi

echo "🛠 Creating systemd service..."
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

echo "🔁 Enabling and reloading systemd..."
sudo systemctl daemon-reexec
sudo systemctl enable jarvis.service

echo -e "\n✅ Jarvis installed and set to start on boot."
echo "You can start it manually with:"
echo "   sudo systemctl start jarvis"
echo "Or reboot and it will auto-start."
