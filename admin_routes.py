# admin_routes.py (Add to your web_admin.py or import separately)
import zipfile
from flask import request, redirect, url_for
from config_manager import load_config, save_config
import os, json

UPLOAD_DIR = "personalities"
IOT_DEVICES_FILE = "config/iot_devices.json"

@app.route('/upload-personality', methods=['POST'])
def upload_personality():
    name = request.form['personality_name']
    zip_file = request.files['personality_zip']
    extract_path = os.path.join(UPLOAD_DIR, name)
    os.makedirs(extract_path, exist_ok=True)
    
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    config = load_config()
    config['personality'] = name
    save_config(config)
    return redirect(url_for('index'))

@app.route('/update-keys', methods=['POST'])
def update_keys():
    config = load_config()
    config['openai_key'] = request.form['openai_key']
    config['auth0_domain'] = request.form['auth0_domain']
    config['auth0_client_id'] = request.form['auth0_client_id']
    config['auth0_client_secret'] = request.form['auth0_client_secret']
    save_config(config)
    return redirect(url_for('index'))

@app.route('/pair-device', methods=['POST'])
def pair_device():
    device_name = request.form['device_name']
    qr_content = request.form['qr_content']

    os.makedirs(os.path.dirname(IOT_DEVICES_FILE), exist_ok=True)
    if os.path.exists(IOT_DEVICES_FILE):
        with open(IOT_DEVICES_FILE, 'r') as f:
            devices = json.load(f)
    else:
        devices = {}

    devices[device_name] = qr_content
    with open(IOT_DEVICES_FILE, 'w') as f:
        json.dump(devices, f, indent=2)

    config = load_config()
    config['iot_devices'] = list(devices.keys())
    save_config(config)
    return redirect(url_for('index'))
