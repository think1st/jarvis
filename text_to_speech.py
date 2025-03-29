import pyttsx3
from gtts import gTTS
import os
import tempfile
import subprocess
from config_manager import load_config


def speak_text(text):
    config = load_config()
    tts_engine = config.get("tts_engine", "gtts")  # Changed to gTTS default
    voice_settings = config.get("voice_settings", {})
    voice_id = voice_settings.get("voice_id", 0)
    rate = voice_settings.get("rate", 170)
    volume = voice_settings.get("volume", 1.0)

    if tts_engine == "gtts":
        try:
            tts = gTTS(text=text, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_path = fp.name
                tts.save(temp_path)

            # 🔍 Autodetect if a Bluetooth speaker is connected
            sinks = subprocess.check_output(["pactl", "list", "short", "sinks"]).decode()
            if "bluez_sink" in sinks:
                os.system(f"paplay {temp_path}")
            else:
                os.system(f"mpg123 {temp_path}")

            os.remove(temp_path)

        except Exception as e:
            print("[ERROR] Failed to use gTTS:", e)

    else:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)

            voices = engine.getProperty('voices')
            if 0 <= voice_id < len(voices):
                engine.setProperty('voice', voices[voice_id].id)
            else:
                print(f"[WARN] Voice ID {voice_id} not found. Using default.")

            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("[ERROR] pyttsx3 failed:", e)


if __name__ == '__main__':
    speak_text("Hello, MR. Stark. Testing voice engine.")
