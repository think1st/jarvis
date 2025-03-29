# text_to_speech.py
import os
import tempfile
import requests
import subprocess
import pyttsx3
from gtts import gTTS
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
    engine_preference = config.get("tts_engine", "gtts")
    fallback = config.get("fallback_tts_engine", "pyttsx3")
    tts_settings = config.get("tts_settings", {})
    online = is_online()

    selected_engine = engine_preference if online else fallback

    if selected_engine == "gtts":
        try:
            lang = tts_settings.get("gtts", {}).get("lang", "en")
            tts = gTTS(text=text, lang=lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
            play_audio(fp.name)
            os.remove(fp.name)
        except Exception as e:
            print("[ERROR] gTTS failed:", e)

    elif selected_engine == "elevenlabs":
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
                    "stability": 0.7,
                    "similarity_boost": 0.8,
                    "style": 0.3,
                    "use_speaker_boost": True,
                    "speed": 0.90  # 👈 Add this line to slow it down (default is 1.0)
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

    else:  # pyttsx3
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
            else:
                print(f"[WARN] pyttsx3 voice ID {voice_id} not found, using default.")

            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("[ERROR] pyttsx3 failed:", e)

if __name__ == '__main__':
    speak_text("Hello, MR. Stark. ElevenLabs voice is ready.")
