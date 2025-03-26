from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
import os
import json
from config_manager import load_config, save_config
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

CONFIG_FILE = "config/config.json"
WHISPER_CACHE = os.path.expanduser("~/.cache/whisper")
BACKUP_DIR = "backup/"
DEVICE_FILE = "config/devices.json"
PROTOCOL_FILE = "config/protocols.json"

@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    username = request.form.get("username")
    password = request.form.get("password")
    config = load_config()

    if username == config.get("admin", {}).get("username", "admin") and password == config.get("admin", {}).get("password", "tonystark"):
        session["logged_in"] = True
        return redirect(url_for("index"))
    return render_template("login.html", error="Invalid credentials.")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    config = load_config()
    whisper_models = [f for f in os.listdir(WHISPER_CACHE) if os.path.isdir(os.path.join(WHISPER_CACHE, f))]
    personalities = os.listdir("personalities/") if os.path.exists("personalities/") else []

    return render_template("index.html",
                           config=config,
                           whisper_models=whisper_models,
                           personalities=personalities)

@app.route("/update", methods=["POST"])
def update():
    config = load_config()

    # General assistant settings
    config["wake_word"] = request.form.get("wake_word", config["wake_word"])
    config["assistant_name"] = request.form.get("assistant_name", config["assistant_name"])
    config["user_title"] = request.form.get("user_title", config["user_title"])
    config["personality"] = request.form.get("personality", config.get("personality", "default"))
    config["selected_personality"] = request.form.get("selected_personality", config.get("selected_personality", "personality01"))

    # Prompts
    config["pre_prompt"] = request.form.get("pre_prompt", config["pre_prompt"])
    config["post_prompt"] = request.form.get("post_prompt", config["post_prompt"])

    # TTS / STT
    config["tts_engine"] = request.form.get("tts_engine", config["tts_engine"])
    config["stt_engine"] = request.form.get("stt_engine", config["stt_engine"])
    config["whisper_model"] = request.form.get("whisper_model", config["whisper_model"])
    config["voice_settings"]["voice_id"] = int(request.form.get("voice_settings.voice_id", 0))
    config["voice_settings"]["rate"] = int(request.form.get("voice_settings.rate", 170))
    config["voice_settings"]["volume"] = float(request.form.get("voice_settings.volume", 1.0))

    # Personalization
    config["email_signoff"] = request.form.get("email_signoff", config.get("email_signoff", "Kind regards,\nJarvis"))

    # Integrations
    config["openai_key"] = request.form.get("openai_key", config.get("openai_key", ""))
    config["auth0_domain"] = request.form.get("auth0_domain", config.get("auth0_domain", ""))
    config["auth0_client_id"] = request.form.get("auth0_client_id", config.get("auth0_client_id", ""))
    config["auth0_client_secret"] = request.form.get("auth0_client_secret", config.get("auth0_client_secret", ""))

    # Modes
    config["dream_mode_timeout"] = int(request.form.get("dream_mode_timeout", 60))
    config["paranoid_check_interval"] = int(request.form.get("paranoid_check_interval", 120))
    config["alert_email"] = request.form.get("alert_email", config["alert_email"])
    config["holographic_mode"] = True if request.form.get("holographic_mode") == "true" else False

    # Password
    if request.form.get("action") == "change_password":
        config["admin"]["password"] = request.form.get("new_password", config["admin"]["password"])

    # Whisper models
    if request.form.get("action") == "download_model":
        model_name = request.form.get("download_model")
        if model_name:
            os.system(f"pip install faster-whisper && whisper-download --model {model_name}")

    if request.form.get("action") == "remove_model":
        model = request.form.get("remove_model")
        model_path = os.path.join(WHISPER_CACHE, model)
        if os.path.exists(model_path):
            os.system(f"rm -rf {model_path}")

    # Backup
    if request.form.get("action") == "download_backup":
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"config_backup_{now}.json")
        os.makedirs(BACKUP_DIR, exist_ok=True)
        with open(backup_path, "w") as f:
            json.dump(config, f, indent=4)
        return send_file(backup_path, as_attachment=True)

    if request.form.get("action") == "upload_backup":
        file = request.files.get("upload_backup")
        if file:
            content = json.load(file)
            save_config(content)

    save_config(config)
    return redirect(url_for("index"))

@app.route("/voices", methods=["GET"])
def voices():
    import text_to_speech
    voices = text_to_speech.list_voices()
    return jsonify({"voices": voices})

@app.route("/check_update", methods=["GET"])
def check_update():
    return jsonify({"status": "Update check feature coming soon."})
