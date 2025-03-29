import random
import json
import os
import time
from text_to_speech import speak_text
from video_manager import VideoManager

BARK_RESPONSES_PATH = "assets/easter_eggs/bark_responses.json"
TRAINED_FLAG = "features/bark_trained.flag"

class BarkDetector:
    def __init__(self, user_title="Mr. Stark"):
        self.user_title = user_title
        self.video_manager = VideoManager()

    def is_trained(self):
        return os.path.exists(TRAINED_FLAG)

    def load_bark_responses(self):
        if not os.path.exists(BARK_RESPONSES_PATH):
            return []
        with open(BARK_RESPONSES_PATH, "r") as file:
            return json.load(file)

    def handle_bark(self):
        if not self.is_trained():
            print("[INFO] BarkDetector skipped — not trained.")
            return

        responses = self.load_bark_responses()
        if not responses:
            speak_text("Can I pet that daaaawg?")
            return

        choice = random.choice(responses)
        phrase = choice.get("phrase", "Can I pet that daawg?").replace("{title}", self.user_title)
        image = choice.get("image", "assets/easter_eggs/dawg.jpg")

        speak_text(phrase)
        self.video_manager.display_image(image)

    def listen_for_barks(self):
        while True:
            time.sleep(60)  # Simulate bark interval
            self.handle_bark()
