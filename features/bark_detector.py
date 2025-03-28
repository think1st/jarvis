import random
import json
import os
from text_to_speech import speak_text
from video_manager import VideoManager  # Import the class

BARK_RESPONSES_PATH = "assets/easter_eggs/bark_responses.json"
video_manager = VideoManager()  # Create an instance of the class


def load_bark_responses():
    if not os.path.exists(BARK_RESPONSES_PATH):
        return []
    with open(BARK_RESPONSES_PATH, "r") as file:
        return json.load(file)


def handle_bark(user_title="Mr. Stark"):
    responses = load_bark_responses()
    if not responses:
        speak_text("Can I pet that daaaawg?")
        return

    choice = random.choice(responses)
    phrase = choice.get("phrase", "Can I pet that daawg?").replace("{title}", user_title)
    image = choice.get("image", "assets/easter_eggs/dawg.jpg")

    speak_text(phrase)
    video_manager.display_image(image)  # Call method on the instance
