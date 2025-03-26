# Install dependencies for all TTS/STT backends
sudo apt update
sudo apt install -y espeak espeak-ng mpg123 ffmpeg git libffi-dev python3-dev build-essential

# Python packages
pip install --upgrade pip
pip install pyttsx3 gtts
pip install vosk SpeechRecognition pyaudio
pip install faster-whisper

# Download the English-only small model for Faster-Whisper (approx 50MB)
mkdir -p ~/.cache/whisper
cd ~/.cache/whisper
wget https://huggingface.co/guillaumekln/faster-whisper-large-v2/resolve/main/model.bin -O model.bin || true