# File: run.py
# Description: Script to run the Flask app
from dotenv import load_dotenv
import os
from flask import Flask, render_template
from app import app

# Load environment variables
load_dotenv()

# Serve the index.html from the 'templates' directory
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Serving static files like CSS, JS, and images
    app.run(debug=True, host='0.0.0.0', port=5001)