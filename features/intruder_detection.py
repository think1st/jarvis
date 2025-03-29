# intruder_detection.py
import time
import random
import os
from config_manager import load_config
from text_to_speech import speak_text
from video_manager import VideoManager

RESPONSE_LIST = [
    "You are not {title}, you have no power over me.",
    "Access denied. This voice does not match the authorized user.",
    "Imposter detected. Please step away from the console.",
    "You're not {title}, but I admire your confidence.",
    "Authorization failed. This unit obeys only {title}.",
    "Voice mismatch. Engaging passive-aggressive sarcasm mode.",
    "Request denied. Maybe next time, buddy.",
    "You may be charming, but you’re still not {title}.",
    "Only {title} can activate this system. Please fetch them.",
    "Impressive impersonation, still not enough."
]

TRAINED_FLAG = "features/voice_trained.flag"

class IntruderDetection:
    def __init__(self):
        self.guest_mode_until = 0
        self.video = VideoManager()

    def is_trained(self):
        return os.path.exists(TRAINED_FLAG)

    def allow_guest_temporarily(self, duration_minutes=30):
        self.guest_mode_until = time.time() + duration_minutes * 60
        print("Guest mode enabled")

    def is_guest_mode(self):
        return time.time() < self.guest_mode_until

    def check_voice_profile(self, voice_id):
        if not self.is_trained():
            print("[INFO] IntruderDetection skipped — not trained.")
            return True
        if self.is_guest_mode():
            return True
        config = load_config()
        authorized_id = config.get("voice_profile_id", "default")
        return voice_id == authorized_id

    def respond_to_intruder(self):
        config = load_config()
        title = config.get("user_title", "MR. Stark")
        response = random.choice(RESPONSE_LIST).replace("{title}", title)
        self.video.play_loop("idle")
        speak_text(response)

# Example usage:
if __name__ == "__main__":
    detector = IntruderDetection()
    if not detector.check_voice_profile("imposter"):
        detector.respond_to_intruder()
