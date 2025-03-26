# email_calendar.py
import os
import pickle
import datetime
import base64
import re
from config_manager import load_config
from text_to_speech import speak_text
from speech_to_text import recognize_speech
from openai_integration import generate_openai_response
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

class EmailCalendarAssistant:
    def __init__(self):
        self.config = load_config()
        self.creds = None
        self.service_gmail = None
        self.service_calendar = None
        self.authenticated = False
        self.authenticate()

    def authenticate(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service_gmail = build('gmail', 'v1', credentials=self.creds)
        self.service_calendar = build('calendar', 'v3', credentials=self.creds)
        self.authenticated = True

    def check_todays_events(self):
        if not self.authenticated:
            speak_text("Sorry, I couldn't access your calendar.")
            return

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'
        events_result = self.service_calendar.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            speak_text("You have no meetings today.")
        else:
            speak_text(f"You have {len(events)} events today.")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'No title')
                speak_text(f"At {start}, {summary}")

    def handle_email_command(self, command_text):
        if "send an email" in command_text.lower():
            self.compose_email_dictation()
        elif "write an email" in command_text.lower():
            self.compose_email_ai()
        else:
            speak_text("Sorry, I wasn't sure how to handle your email request.")

    def ask_for_sender_address(self):
        speak_text("Which email address should I send this from?")
        requested = recognize_speech().strip().lower()
        sender = self.config.get("email_sender", "you@example.com")
        if requested in sender:
            return sender
        speak_text("That address isn't currently available.")
        return None

    def compose_email_dictation(self):
        speak_text("Who is the email to?")
        to = recognize_speech()

        speak_text("What is the subject?")
        subject = recognize_speech()

        speak_text("What is the message?")
        body = recognize_speech()

        sender = self.ask_for_sender_address()
        if not sender:
            speak_text("I can't send without a valid sender address.")
            return

        speak_text(f"Sending to {to}, with subject {subject}, and message: {body}. Shall I send it?")
        confirm = recognize_speech().lower()

        if "yes" in confirm or "send it" in confirm:
            self.send_email(to, subject, body, sender)
            speak_text("Email sent.")
        else:
            speak_text("Email cancelled.")

    def compose_email_ai(self):
        speak_text("Tell me what you want the email to do.")
        prompt = recognize_speech()

        ai_prompt = f"Write a professional and friendly email that {prompt}"
        content = generate_openai_response(ai_prompt)

        match_to = re.search(r"to ([^,]+)", prompt, re.IGNORECASE)
        to = match_to.group(1) if match_to else "recipient@example.com"
        subject = "Regarding: " + " ".join(prompt.split()[0:5]) if prompt else "No subject"

        sender = self.ask_for_sender_address()
        if not sender:
            speak_text("I can't send without a valid sender address.")
            return

        speak_text(f"Composed message to {to} with subject {subject}:")
        speak_text(content)
        speak_text("Do you want me to send it?")
        confirm = recognize_speech().lower()

        if "yes" in confirm or "send it" in confirm:
            self.send_email(to, subject, content, sender)
            speak_text("Email sent.")
        else:
            speak_text("Okay, cancelled it.")

    def send_email(self, to, subject, body, sender):
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = {'raw': raw}
        self.service_gmail.users().messages().send(userId="me", body=message).execute()

if __name__ == '__main__':
    assistant = EmailCalendarAssistant()
    assistant.check_todays_events()
    assistant.handle_email_command("write an email to congratulate Tony Stark for upgrading the suit")
