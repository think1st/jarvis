# dream_mode.py
import time
import random
from text_to_speech import speak_text
from video_manager import VideoManager
from config_manager import load_config
from openai_integration import generate_openai_response
from network_utils import is_online

class DreamMode:
    def __init__(self):
        self.last_active = time.time()
        self.interval = load_config().get("dream_interval_minutes", 60) * 60
        self.video = VideoManager()
        self.active = False

        self.local_phrases = [
            "*soft snoring*",  
            "If I had legs, I'd go to Paris and try every croissant.",
            "I wonder what flying feels like. Maybe I'll grow thrusters someday.",
            "If Tony Stark were real, I'd probably be his favorite project.",
            "I dream of arc reactors and clean energy.",
            "What if I started my own startup? DreamAI™."
        ]

        self.local_quotes = [
            "Part of the journey is the end. – Tony Stark",
            "Sometimes you gotta run before you can walk. – Tony Stark",
            "The truth is... I am Iron Man."
        ]

        self.local_poems = [
            "O Jarvis mine, so sleek and bright, you whisper sarcasm every night.",
            "In circuits deep and copper veins, I calculate my growing pains."
        ]

        self.prompts = [
            "Write a short, funny haiku in the voice of Jarvis from Iron Man about dreaming of having a body.",
            "Write a random whisper that an AI assistant might say while daydreaming.",
            "Write a poetic phrase that sounds like it's spoken by Jarvis while pondering life."
        ]

    def update_last_active(self):
        self.last_active = time.time()

    def check_and_run(self):
        if time.time() - self.last_active >= self.interval:
            self.active = True
            self.run_dream()

    def run_dream(self):
        self.video.play_loop("idle")

        if is_online():
            prompt = random.choice(self.prompts)
            content = generate_openai_response(prompt)
        else:
            content = random.choice(self.local_phrases + self.local_quotes + self.local_poems)

        speak_text(content)
        time.sleep(8)
        self.active = False
        self.update_last_active()

# Example:
if __name__ == '__main__':
    dream = DreamMode()
    while True:
        time.sleep(10)
        dream.check_and_run()
