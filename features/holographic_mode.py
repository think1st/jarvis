# holographic_mode.py
import os
import subprocess
from config_manager import load_config, save_config
from text_to_speech import speak_text

class HolographicMode:
    def __init__(self):
        self.config = load_config()
        self.enabled = self.config.get("holographic_mode", False)

    def enable(self):
        if not self.enabled:
            speak_text("Activating holographic mode.")
            self.set_orientation(180)
            self.config["holographic_mode"] = True
            save_config(self.config)
            self.enabled = True

    def disable(self):
        if self.enabled:
            speak_text("Deactivating holographic mode.")
            self.set_orientation(0)
            self.config["holographic_mode"] = False
            save_config(self.config)
            self.enabled = False

    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def set_orientation(self, degrees):
        rotation_cmd = f"xrandr --output DSI-1 --rotate {'inverted' if degrees == 180 else 'normal'}"
        try:
            subprocess.run(rotation_cmd, shell=True, check=True)
            print(f"[HolographicMode] Screen rotated to {degrees} degrees")
        except subprocess.CalledProcessError:
            print("[HolographicMode] Failed to rotate display")

    def handle_voice_command(self, transcript):
        system_name = self.config.get("system_name", "jarvis").lower()
        command = transcript.lower()

        if system_name in command:
            if "activate holographic mode" in command or "turn on holographic mode" in command:
                self.enable()
                return True
            elif "deactivate holographic mode" in command or "turn off holographic mode" in command:
                self.disable()
                return True
            elif "toggle holographic mode" in command:
                self.toggle()
                return True
        return False

# Example usage
if __name__ == '__main__':
    holo = HolographicMode()
    example_input = "Jarvis, activate holographic mode"
    holo.handle_voice_command(example_input)
