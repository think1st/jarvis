# habit_engine.py
import os
import json
import time
import random
from datetime import datetime
from config_manager import load_config
from text_to_speech import speak_text

HABIT_FILE = "data/habits.json"

class HabitEngine:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.config = load_config()
        self.habits = self.load_habits()
        self.messages = [
            "You usually say '{command}' around this time. Want me to do it for you?",
            "It's about time for '{command}', isn't it? Just say the word.",
            "Hey {title}, ready for your usual: '{command}'?",
            "Pattern detected. Would you like me to run '{command}' again?",
            "Looks like it's your usual time for '{command}', {title}.",
            "Habit alert! Should I go ahead with '{command}'?"
        ]

    def load_habits(self):
        if os.path.exists(HABIT_FILE):
            with open(HABIT_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_habits(self):
        with open(HABIT_FILE, "w") as f:
            json.dump(self.habits, f, indent=2)

    def record(self, command):
        now = datetime.now().isoformat()
        if command not in self.habits:
            self.habits[command] = []
        self.habits[command].append(now)
        self.save_habits()

    def get_stats(self):
        return {cmd: len(timestamps) for cmd, timestamps in self.habits.items()}

    def suggest_command(self):
        if not self.habits:
            return None
        now = time.time()
        frequent = [(cmd, times) for cmd, times in self.habits.items() if len(times) >= 3]
        for cmd, times in frequent:
            last_time = datetime.fromisoformat(times[-1]).timestamp()
            if now - last_time > 86400:
                return cmd
        return None

    def check_and_suggest(self):
        suggestion = self.suggest_command()
        if suggestion:
            title = self.config.get("user_title", "MR. Stark")
            message = random.choice(self.messages).replace("{command}", suggestion).replace("{title}", title)
            speak_text(message)

# Example:
if __name__ == '__main__':
    engine = HabitEngine()
    engine.record("play music")
    engine.check_and_suggest()
    print("Stats:", engine.get_stats())
