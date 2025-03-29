import os
import queue
import sounddevice as sd
import vosk
import json
import time
import tempfile
import soundfile as sf
from config_manager import load_config

# Whisper fallback
try:
    from faster_whisper import WhisperModel
    whisper_available = True
except ImportError:
    whisper_available = False

MODEL_PATH = "vosk_model"
SAMPLE_RATE = 16000
WAKE_WORD = load_config().get("wake_word", "hey jarvis").lower()

def load_vosk_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Vosk model not found. Please download and extract to 'vosk_model/'")
    return vosk.Model(MODEL_PATH)

def detect_wake_word():
    q = queue.Queue()
    model = load_vosk_model()
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("👂 Waiting for wake word...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()
                print("💬 Heard:", text)
                if WAKE_WORD in text:
                    print("✅ Wake word detected.")
                    return True

def record_after_wake(duration=10, silence_timeout=3):
    print("🎤 Recording after wake word...")
    silence_threshold = 100  # Adjust as needed
    silence_duration = 0
    start_time = time.time()
    frames = []

    def callback(indata, frames_count, time_info, status):
        nonlocal silence_duration, start_time
        volume = max(indata[:, 0])
        frames.append(indata.copy())

        if abs(volume) < 0.01:
            if time.time() - start_time > silence_duration:
                silence_duration = time.time()
        else:
            silence_duration = 0

        if time.time() - silence_duration >= silence_timeout:
            raise sd.CallbackStop

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16', callback=callback):
        try:
            sd.sleep(int(duration * 1000))
        except sd.CallbackStop:
            print("⏹️ Silence detected, stopping recording.")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, b''.join(frames), SAMPLE_RATE)
    return temp_file.name

def transcribe_with_whisper(filename):
    if not whisper_available:
        raise ImportError("faster-whisper is not installed")

    config = load_config()
    model_name = config.get("whisper_model", "base.en")
    model = WhisperModel(model_name, compute_type="int8")
    segments, _ = model.transcribe(filename)

    full_text = " ".join([segment.text.strip() for segment in segments])
    return full_text.strip()

def recognize_speech():
    engine = load_config().get("stt_engine", "whisper")

    if engine != "whisper":
        print("⚠️ Wake word + silence only works with Whisper. Falling back to default.")
        return recognize_with_vosk()

    if detect_wake_word():
        temp_wav = record_after_wake()
        text = transcribe_with_whisper(temp_wav)
        os.remove(temp_wav)
        return text
    return ""

# For fallback
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

if __name__ == '__main__':
    print("Recognized:", recognize_speech())
