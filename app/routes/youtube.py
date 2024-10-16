# File: app/routes/youtube.py
# Description: YouTube-specific routes (authorization, comments, etc.)
import os
import json
import logging
from flask import Blueprint, request, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from app.services.youtube_service import authorize_youtube_service, handle_youtube_comments

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

youtube_bp = Blueprint('youtube_bp', __name__)

# Route to authorize YouTube
@youtube_bp.route('/authorize-youtube', methods=['GET'])
def authorize_youtube():
    return authorize_youtube_service()

# Route to handle the YouTube OAuth callback
@youtube_bp.route('/authorize-youtube/callback', methods=['GET'])
def youtube_callback():
    # Retrieve the authorization code from the callback URL
    code = request.args.get('code')
    if not code:
        logger.error("Authorization failed: No code received")
        return "Authorization failed: No code received", 400

    # Load the client secrets file and set up the OAuth flow
    CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')
    logger.info(f"Using client secrets file: {CLIENT_SECRETS_FILE}")
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
    )
    flow.redirect_uri = 'http://localhost:5001/authorize-youtube/callback'

    try:
        # Exchange the authorization code for an access token
        logger.info(f"Attempting to exchange authorization code: {code}")
        flow.fetch_token(code=code)

        # Save the credentials to a file
        credentials = flow.credentials
        credentials_data = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }

        # Save the credentials to youtube_credentials.json
        credentials_file = os.getenv('YOUTUBE_CREDENTIALS_FILE', '/Users/armand/DevOps-Project/ConvoHub/youtube_credentials.json')
        logger.info(f"Saving credentials to file: {credentials_file}")
        
        with open(credentials_file, 'w') as file:
            json.dump(credentials_data, file)

        logger.info("YouTube authorization successful!")
        return "YouTube authorization successful!", 200

    except Exception as e:
        logger.error(f"An error occurred during OAuth: {str(e)}")
        return f"An error occurred: {str(e)}", 500

# Route to manage YouTube comments
@youtube_bp.route('/api/v1/comments', methods=['POST'])
def manage_youtube_comments():
    return handle_youtube_comments(request.json)