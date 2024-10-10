# File: app/services/credentials.py
# Description: Manages loading credentials for various APIs
import json

def load_credentials(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)