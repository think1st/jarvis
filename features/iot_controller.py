# smart_room.py
import json
import os
from config_manager import load_config
from text_to_speech import speak_text

ROOM_FILE = "data/protocols.json"

class SmartRoom:
    def __init__(self):
        self.protocols = {}
        self.config = load_config()
        os.makedirs("data", exist_ok=True)
        self.load_protocols()

    def load_protocols(self):
        if os.path.exists(ROOM_FILE):
            with open(ROOM_FILE, 'r') as f:
                self.protocols = json.load(f)
        else:
            self.protocols = {}
            self.save_protocols()

    def save_protocols(self):
        with open(ROOM_FILE, 'w') as f:
            json.dump(self.protocols, f, indent=2)

    def execute_protocol(self, name):
        name = name.lower()
        if name in self.protocols:
            actions = self.protocols[name]
            for action in actions:
                self.trigger_device(action)
            speak_text(f"Protocol '{name}' executed.")
        else:
            speak_text(f"I don't have a protocol named '{name}' set up yet.")

    def trigger_device(self, device_command):
        print(f"[SmartRoom] Triggered device command: {device_command}")
        # Integration point for MQTT or HTTP control logic

    def list_protocols(self):
        if self.protocols:
            speak_text("You have the following smart room protocols: " + ", ".join(self.protocols.keys()))
        else:
            speak_text("No smart room protocols configured yet.")

# Example:
if __name__ == '__main__':
    room = SmartRoom()
    room.list_protocols()
    room.execute_protocol("party protocol")
