#!/bin/bash

set -e

JARVIS_DIR="$HOME/jarvis"

echo "🔧 Updating system and installing base dependencies..."
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
  python3 python3-pip python3-venv \
  mpv portaudio19-dev libasound2-dev espeak-ng mpg123 ffmpeg \
  git hostapd dnsmasq unzip libffi-dev python3-dev build-essential fbida wget curl

# Clone or update repo
if [ ! -d "$JARVIS_DIR" ]; then
  echo "📦 Cloning Jarvis repo..."
  git clone https://github.com/think1st/jarvis.git "$JARVIS_DIR"
else
  echo "🔄 Updating existing Jarvis repo..."
  cd "$JARVIS_DIR"
  git pull
fi

cd "$JARVIS_DIR"

# Setup Python virtual environment
if [ ! -d "venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate

# Install Python packages
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install flask pyttsx3 gtts \
  vosk SpeechRecognition pyaudio \
  faster-whisper sounddevice soundfile

# Create folders
echo "📁 Preparing folder structure..."
mkdir -p config backup features assets/qr assets/video assets/easter_eggs personalities static/js static/css templates

# Ensure feature init
touch features/__init__.py

# Copy config if missing
if [ ! -f "config/config.json" ]; then
  echo "⚙️ Copying default config..."
  cp config_default.json config/config.json
fi

# Download Whisper base model (faster-whisper base.en)
echo "🧠 Downloading Whisper base.en model..."
mkdir -p ~/.cache/whisper/base.en
cd ~/.cache/whisper/base.en
wget -nc https://huggingface.co/guillaumekln/faster-whisper-base.en/resolve/main/model.bin -O model.bin || true
cd "$JARVIS_DIR"

# Set permissions
chmod +x *.sh

# Create systemd service
SERVICE_FILE="/etc/systemd/system/jarvis.service"
echo "🛠 Creating systemd service..."
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Jarvis Assistant
After=network.target

[Service]
ExecStart=$JARVIS_DIR/venv/bin/python $JARVIS_DIR/main.py
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
