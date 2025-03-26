import json
import os

CONFIG_PATH = "config/config.json"
DEFAULT_CONFIG_PATH = "config_default.json"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("[CONFIG] config.json missing, copying default...")
        os.makedirs("config", exist_ok=True)
        if os.path.exists(DEFAULT_CONFIG_PATH):
            with open(DEFAULT_CONFIG_PATH, "r") as default_file:
                default_data = json.load(default_file)
            save_config(default_data)
        else:
            print("[CONFIG] No default config found!")
            return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
