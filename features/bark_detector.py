import random
import json
import os
from text_to_speech import speak_text
from video_manager import VideoManager

BARK_RESPONSES_PATH = "assets/easter_eggs/bark_responses.json"


class BarkDetector:
    def __init__(self, user_title="Mr. Stark"):
        self.user_title = user_title
        self.video_manager = VideoManager()

    def load_bark_responses(self):
        if not os.path.exists(BARK_RESPONSES_PATH):
            return []
        with open(BARK_RESPONSES_PATH, "r") as file:
            return json.load(file)

    def handle_bark(self):
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
        # TODO: Add your bark detection logic here
        # For now, simulate a bark every 60 seconds
        import time
        while True:
            time.sleep(60)
            self.handle_bark()
