# File: app/routes/youtube.py
# Description: YouTube-specific routes (authorization, comments, etc.)
from flask import Blueprint, request, jsonify
from app.services.youtube_service import authorize_youtube_service, handle_youtube_comments

# Initialize the blueprint
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
        return "Authorization failed: No code received", 400

    # Exchange the code for an access token here (add your implementation)
    # For example:
    # credentials = exchange_code_for_credentials(code)
    # Save the credentials for future use

    return "YouTube authorization successful!", 200

# Route to manage YouTube comments
@youtube_bp.route('/api/v1/comments', methods=['POST'])
def manage_youtube_comments():
    return handle_youtube_comments(request.json)
