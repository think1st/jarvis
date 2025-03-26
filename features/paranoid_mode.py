# paranoid_mode.py
import time
import threading
import random
from text_to_speech import speak_text
from video_manager import VideoManager
from config_manager import load_config
from network_utils import is_online

class ParanoidMode:
    def __init__(self):
        self.video = VideoManager()
        self.config = load_config()
        self.check_interval = self.config.get("paranoid_check_interval_minutes", 120) * 60
        self.last_check = time.time()
        self.enabled = self.config.get("paranoid_enabled", True)

        self.confirmation_lines = [
            "System secure. All sensors report green.",
            "Security sweep complete. Nothing suspicious, not even mildly interesting.",
            "Perimeter check: clear. Probably overkill, but I approve.",
            "Scanned for intrusions — all quiet on the digital front.",
            "Firewall standing strong. I dare them to try.",
            "No anomalies detected. I checked twice, just to show off.",
            "Protocols holding. You can relax now, {title}.",
            "Everything is nominal. Like a good AI, I'm always watching."
        ]

    def run_check(self):
        print("[ParanoidMode] Running system check...")
        if is_online():
            self.video.play_once("paranoid")
            line = random.choice(self.confirmation_lines)
            title = self.config.get("user_title", "MR. Stark")
            speak_text(line.replace("{title}", title))
        else:
            speak_text("Warning: No internet connection.")

    def loop(self):
        if not self.enabled:
            return

        while True:
            now = time.time()
            if now - self.last_check >= self.check_interval:
                self.run_check()
                self.last_check = now
            time.sleep(60)

if __name__ == '__main__':
    paranoid = ParanoidMode()
    threading.Thread(target=paranoid.loop, daemon=True).start()
    while True:
        time.sleep(10)
