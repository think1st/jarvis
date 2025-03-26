# personality_manager.py
import os
from config_manager import load_config, save_config
from text_to_speech import speak_text
from speech_to_text import recognize_speech

class PersonalityManager:
    def __init__(self):
        self.base_path = "personalities"
        self.config = load_config()
        self.active = self.config.get("personality", "default")

    def get_video_path(self, state):
        return os.path.join(self.base_path, self.active, f"{state}.mp4")

    def get_all_personalities(self):
        return [name for name in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, name))]

    def get_voice_settings(self):
        return self.config.get("voice_settings", {})

    def apply_personality(self, name):
        if name in self.get_all_personalities():
            self.config["personality"] = name
            save_config(self.config)
            speak_text(f"Personality switched to {name}.")
            return True
        speak_text(f"I couldn't find a personality named {name}.")
        return False

    def speak_and_listen_personalities(self):
        personalities = self.get_all_personalities()
        title = self.config.get("user_title", "MR. Stark")
        current = self.config.get("personality", "default")

        if not personalities:
            speak_text("No personalities found. Please add one to the personalities folder.")
            return

        speak_text(f"My current personality is {current}, {title}.")
        other_personas = [p for p in personalities if p != current]
        if other_personas:
            speak_text("I can also be: " + ", ".join(other_personas))
        else:
            speak_text("I don't have any other personalities to switch to just yet.")
            return

        speak_text("Which one would you like?")
        response = recognize_speech().lower()
        for name in personalities:
            if name.lower() in response:
                self.apply_personality(name)
                return

        speak_text("I didn’t catch that. You can always try again.")

# Example voice triggers to integrate in main.py:
# "Jarvis, what's with the attitude?" or "Jarvis, change your attitude"

if __name__ == '__main__':
    pm = PersonalityManager()
    pm.speak_and_listen_personalities()
    print("Active personality:", pm.active)
    print("Speaking video path:", pm.get_video_path("speaking"))
