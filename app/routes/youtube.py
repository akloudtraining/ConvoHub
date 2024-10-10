# File: app/routes/youtube.py
# Description: YouTube-specific routes (authorization, comments, etc.)
from flask import Blueprint, request, jsonify
from app.services.youtube_service import authorize_youtube_service, handle_youtube_comments

youtube_bp = Blueprint('youtube_bp', __name__)

# Route to authorize YouTube
@youtube_bp.route('/authorize-youtube', methods=['GET'])
def authorize_youtube():
    return authorize_youtube_service()

# Route to manage YouTube comments
@youtube_bp.route('/api/v1/comments', methods=['POST'])
def manage_youtube_comments():
    return handle_youtube_comments(request.json)