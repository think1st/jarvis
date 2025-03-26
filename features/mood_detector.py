# mood_detector.py
import random
from config_manager import load_config
from text_to_speech import speak_text

# Simulated mood analysis engine
class MoodDetector:
    def __init__(self):
        self.config = load_config()

        self.sad_responses = [
            "You sound down. Would you like to hear a joke?",
            "Feeling blue? I have a haiku that might help.",
            "Would you like a distraction, or should I just sit here quietly, {title}?"
        ]

        self.stressed_responses = [
            "You seem tense. Want me to play something calming?",
            "I recommend deep breathing and low-fi beats, {title}.",
            "Would a short break help? I can keep the world running in your absence."
        ]

        self.angry_responses = [
            "Whoa. Someone's channeling the Hulk today. Need a quote from Tony to chill?",
            "I detect anger. I also detect the urge to punch things. Let’s redirect that.",
            "I've heard therapy works wonders. Or Iron Man quotes. Shall I proceed?"
        ]

    def analyze_tone(self, loudness=0.5, pitch=0.5):
        # This is a placeholder for real pitch/loudness analysis or AI emotion detection
        mood = random.choice(["sad", "stressed", "angry", "neutral"])
        return mood

    def respond_to_mood(self, mood):
        title = self.config.get("user_title", "MR. Stark")
        if mood == "sad":
            speak_text(random.choice(self.sad_responses).replace("{title}", title))
        elif mood == "stressed":
            speak_text(random.choice(self.stressed_responses).replace("{title}", title))
        elif mood == "angry":
            speak_text(random.choice(self.angry_responses).replace("{title}", title))
        else:
            pass  # Stay silent if no mood requires response

# Example usage
if __name__ == '__main__':
    detector = MoodDetector()
    mood = detector.analyze_tone()
    print(f"Detected mood: {mood}")
    detector.respond_to_mood(mood)
