# voice_routes.py
from flask import jsonify
import pyttsx3


def get_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_list = [
        {"id": i, "name": v.name, "lang": v.languages[0].decode('utf-8') if v.languages else ""}
        for i, v in enumerate(voices)
    ]
    return jsonify(voice_list)
