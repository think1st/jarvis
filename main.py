import time
import threading
import glob
import os

# 🧼 Clean up old temp .wav files from Whisper
for f in glob.glob("/tmp/tmp*.wav"):
    try:
        os.remove(f)
        print(f"[Cleanup] Removed leftover temp file: {f}")
    except Exception as e:
        print(f"[Cleanup Error] Could not remove {f}: {e}")

from pynput import keyboard as kb
from config_manager import load_config
from speech_to_text import recognize_speech
from text_to_speech import speak_text
from video_manager import VideoManager

# Feature modules (from features/)
from features.bark_detector import BarkDetector
from features.dream_mode import DreamMode
from features.email_calendar import EmailCalendarAssistant
from features.habit_engine import HabitEngine
from features.holographic_mode import HolographicMode
from features.intruder_detection import IntruderDetection
from features.mood_detector import MoodDetector
from features.panic_mode import PanicMode
from features.paranoid_mode import ParanoidMode
from features.personality_manager import PersonalityManager
from features.smart_room import SmartRoom

config = load_config()
video = VideoManager()
video_enabled = True  # Visuals ON by default
system_name = config.get("system_name", "jarvis").lower()
user_title = config.get("user_title", "MR. Stark")

def hotkey_listener():
    global video_enabled

    def on_press(key):
        try:
            if key == kb.HotKey.parse('<ctrl>+<alt>+j').keys[-1]:
                # Check if modifiers are active
                if current_keys == {kb.Key.ctrl_l, kb.Key.alt_l} or current_keys == {kb.Key.ctrl_r, kb.Key.alt_r}:
                    toggle_visuals()
        except:
            pass

    def on_release(key):
        if key in current_keys:
            current_keys.remove(key)

    def on_key_down(key):
        current_keys.add(key)

    def toggle_visuals():
        global video_enabled
        video_enabled = not video_enabled
        if video_enabled:
            speak_text("Visuals resumed, sir.")
            video.play_loop("idle")
        else:
            speak_text("Visuals disabled.")
            video.stop()

    current_keys = set()
    with kb.Listener(on_press=on_key_down, on_release=on_release) as listener:
        listener.join()


def main_loop(): 
    global video_enabled
    panic = PanicMode()
    detector = IntruderDetection()
    dream = DreamMode()
    paranoid = ParanoidMode()
    personality = PersonalityManager()
    emailer = EmailCalendarAssistant()
    habits = HabitEngine()
    room = SmartRoom()
    mood = MoodDetector()
    holo = HolographicMode()
    bark = BarkDetector()

    threading.Thread(target=paranoid.loop, daemon=True).start()
    threading.Thread(target=bark.listen_for_barks, daemon=True).start()
    threading.Thread(target=hotkey_listener, daemon=True).start()

    if video_enabled:
        video.play_loop("idle")
    speak_text(f"Good {get_greeting()}, {user_title}.")

    while True:
        try:
            if video_enabled:
                video.play_loop("listening")
            transcript = recognize_speech()
            habits.record(transcript)
            if video_enabled:
                video.play_loop("thinking")

            if not detector.check_voice_profile(transcript):
                if video_enabled:
                    video.play_loop("idle")
                detector.respond_to_intruder()
                continue

            if "be nice to our guest" in transcript.lower():
                if video_enabled:
                    video.play_loop("idle")
                detector.allow_guest_temporarily()
                continue

            if any(phrase in transcript.lower() for phrase in ["change your attitude", "what's with the attitude"]):
                if video_enabled:
                    video.play_loop("idle")
                personality.speak_and_listen_personalities()
                continue

            if holo.handle_voice_command(transcript):
                if video_enabled:
                    video.play_loop("idle")
                continue

            if "check my calendar" in transcript.lower():
                emailer.check_todays_events()
                if video_enabled:
                    video.play_loop("idle")
                continue

            if any(phrase in transcript.lower() for phrase in ["send an email", "write an email"]):
                emailer.handle_email_command(transcript)
                if video_enabled:
                    video.play_loop("idle")
                continue

            if "activate protocol" in transcript.lower():
                spoken = transcript.lower().replace("activate protocol", "").strip()
                room.execute_protocol(spoken)
                if video_enabled:
                    video.play_loop("idle")
                continue

            if any(phrase in transcript.lower() for phrase in ["stop the visuals", "disable video", "cut the loop"]):
                video.stop()
                video_enabled = False
                speak_text("Visuals disengaged, sir.")
                continue

            if any(phrase in transcript.lower() for phrase in ["resume visuals", "start video", "bring visuals back"]):
                video_enabled = True
                speak_text("Visuals restored, sir.")
                video.play_loop("idle")
                continue

            mood_type = mood.analyze_tone()
            mood.respond_to_mood(mood_type)

            dream.check_and_run()
            habits.check_and_suggest()

            if video_enabled:
                video.play_loop("idle")
            time.sleep(1)

        except Exception as e:
            panic.handle_error(str(e), critical=True)
            if video_enabled:
                video.play_loop("idle")

def get_greeting():
    hour = time.gmtime().tm_hour
    if hour < 12:
        return "morning"
    elif hour < 18:
        return "afternoon"
    else:
        return "evening"

if __name__ == "__main__":
    main_loop()
