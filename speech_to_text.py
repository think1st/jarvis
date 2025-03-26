# speech_to_text.py
import os
import queue
import sounddevice as sd
import vosk
import json
from config_manager import load_config

# Whisper fallback
try:
    from faster_whisper import WhisperModel
    whisper_available = True
except ImportError:
    whisper_available = False

MODEL_PATH = "vosk_model"
SAMPLE_RATE = 16000

def load_vosk_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Vosk model not found. Please download and extract to 'vosk_model/'")
    return vosk.Model(MODEL_PATH)

def recognize_with_vosk():
    q = queue.Queue()
    model = load_vosk_model()
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎤 Listening with Vosk...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    return text

def recognize_with_whisper():
    if not whisper_available:
        raise ImportError("faster-whisper is not installed")

    config = load_config()
    model_name = config.get("whisper_model", "base.en")

    print(f"🎤 Listening with Whisper ({model_name})...")
    import tempfile
    import soundfile as sf

    duration = 5  # seconds of recording
    filename = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

    print("Recording...")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    sf.write(filename, audio, SAMPLE_RATE)

    model = WhisperModel(model_name, compute_type="int8")
    segments, _ = model.transcribe(filename)

    full_text = ""
    for segment in segments:
        full_text += segment.text.strip() + " "

    os.remove(filename)
    return full_text.strip()

def recognize_speech():
    config = load_config()
    engine = config.get("stt_engine", "vosk")

    if engine == "vosk":
        return recognize_with_vosk()
    elif engine == "whisper":
        return recognize_with_whisper()
    else:
        print("No STT engine selected or supported.")
        return ""

if __name__ == '__main__':
    print("Recognized:", recognize_speech())
