import random
import json
import os
from text_to_speech import speak
from video_manager import display_image

BARK_RESPONSES_PATH = "assets/easter_eggs/bark_responses.json"


def load_bark_responses():
    if not os.path.exists(BARK_RESPONSES_PATH):
        return []
    with open(BARK_RESPONSES_PATH, "r") as file:
        return json.load(file)


def handle_bark(user_title="Mr. Stark"):
    responses = load_bark_responses()
    if not responses:
        speak("A dog barked, but I have nothing witty to say.")
        return

    choice = random.choice(responses)
    phrase = choice.get("phrase", "Can I pet that daawg?").replace("{title}", user_title)
    image = choice.get("image", "assets/easter_eggs/dawg.jpg")

    speak(phrase)
    display_image(image)


# Example usage:
# handle_bark("Dr. Banner")
