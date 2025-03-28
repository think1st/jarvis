import os
import random
import subprocess
from config_manager import load_config

class VideoManager:
    def __init__(self):
        self.current_process = None
        self.config = load_config()
        self.base_path = "personalities"

    def _get_video_file(self, state):
        personality = self.config.get("selected_personality", "personality01")
        personality_path = os.path.join(self.base_path, personality)
        matching_files = [
            f for f in os.listdir(personality_path)
            if f.startswith(state) and f.endswith(".mp4")
        ]
        if not matching_files:
            print(f"[WARN] No video files found for state: {state}")
            return None
        return os.path.join(personality_path, random.choice(matching_files))

    def play_loop(self, state):
        self.stop()
        file = self._get_video_file(state)
        if file:
            self.current_process = subprocess.Popen(
                ["mpv", "--fs", "--loop", "--no-osd-bar", "--no-terminal", file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    def display_image(self, image_path):
        self.stop()
        self.current_process = subprocess.Popen(
            ["feh", "--fullscreen", "--hide-pointer", "--auto-zoom", image_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def stop(self):
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
            self.current_process = None
