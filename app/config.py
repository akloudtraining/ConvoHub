# File: config.py
# Description: Application configuration settings
import os

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    YOUTUBE_CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')