# panic_mode.py
import os
import time
import traceback
import random
from config_manager import load_config
from text_to_speech import speak_text
from video_manager import VideoManager
from network_utils import is_online
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class PanicMode:
    def __init__(self):
        self.video = VideoManager()
        self.config = load_config()
        self.email_to = self.config.get("alert_email", None)
        self.personality = self.config.get("personality", "default")

        self.panic_messages = [
            "Something is wrong. Activating panic protocol.",
            "Unidentified error detected. Engaging cinematic-level concern.",
            "Jarvis feels... disturbed. Executing panic mode.",
            "Alert! The Chitauri just attacked Stark Tower — metaphorically.",
            "Something broke. Again. Just like Tony's heart in Infinity War.",
            "Critical malfunction. If I had arms, I'd wave them frantically now.",
            "This system's having a panic attack. Allow me to demonstrate.",
            "Oops. That wasn’t supposed to happen. Initiating dramatic protocol.",
            "I'm not saying it's Ultron, but... it's Ultron.",
            "Well this is awkward. Entering panic.mp4 in style."
        ]

    def handle_error(self, error_message, critical=False):
        print("[PanicMode] Error detected")
        self.video.play_once("panic")
        speak_text(random.choice(self.panic_messages))

        log_path = f"logs/panic_{int(time.time())}.log"
        os.makedirs("logs", exist_ok=True)
        with open(log_path, "w") as f:
            f.write(error_message)

        if self.email_to and is_online():
            self.send_log_email(log_path, error_message)

        if critical:
            speak_text("This error requires a system reboot. Hold on.")
            time.sleep(3)
            os.system("sudo reboot")

    def send_log_email(self, path, message):
        try:
            sender = "jarvis@localhost"
            subject = "Jarvis System Panic Log"
            msg = MIMEText(message)
            msg['From'] = formataddr(("Jarvis", sender))
            msg['To'] = self.email_to
            msg['Subject'] = subject

            with smtplib.SMTP('localhost') as server:
                server.sendmail(sender, self.email_to, msg.as_string())

            print("[PanicMode] Log email sent.")
        except Exception as e:
            print(f"[PanicMode] Failed to send email: {e}")

    def try_wrap(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            self.handle_error(tb, critical=True)
            return None

if __name__ == '__main__':
    panic = PanicMode()
    def unstable_function():
        raise RuntimeError("Oh no, the arc reactor exploded!")

    panic.try_wrap(unstable_function)
