# File: run.py
# Description: Script to run the Flask app
from dotenv import load_dotenv
import os
from app import app

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)