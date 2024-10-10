# File: config.py
# Description: Application configuration settings
import os

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    YOUTUBE_CLIENT_SECRETS_FILE = "client_secrets.json"