#!/bin/bash

set -e

JARVIS_DIR="$HOME/jarvis"
VENV_DIR="$JARVIS_DIR/venv"

echo "🔧 Updating system and installing base dependencies..."
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
  python3 python3-pip python3-venv \
  mpv portaudio19-dev libasound2-dev \
  libffi-dev python3-dev build-essential \
  feh ffmpeg git wget curl unzip

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
pip install flask pyttsx3 gtts vosk \
  SpeechRecognition pyaudio faster-whisper \
  sounddevice soundfile

echo "📁 Creating folder structure..."
mkdir -p config backup features assets/qr assets/video assets/easter_eggs personalities static/js static/css templates
touch features/__init__.py

if [ ! -f "config/config.json" ]; then
  echo "⚙️ Copying default config..."
  cp config_default.json config/config.json
fi

echo "🧠 Downloading Whisper base.en model..."
mkdir -p ~/.cache/whisper/base.en
cd ~/.cache/whisper/base.en
wget -nc https://huggingface.co/guillaumekln/faster-whisper-base.en/resolve/main/model.bin -O model.bin || true
cd "$JARVIS_DIR"

echo "🛠 Setting permissions..."
chmod +x *.sh

echo "🧩 Creating systemd service..."
SERVICE_FILE="/etc/systemd/system/jarvis.service"

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Jarvis Assistant
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/python $JARVIS_DIR/main.py
WorkingDirectory=$JARVIS_DIR
Restart=always
User=$USER
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl enable jarvis.service

echo -e "\n✅ Jarvis is installed. Reboot or run:"
echo "   sudo systemctl start jarvis"
echo "Then visit http://<your-pi-ip>:5000 to configure."
