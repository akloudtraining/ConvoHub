# File: app/services/youtube_service.py
# Description: Handles YouTube API calls
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
from flask import jsonify

def authorize_youtube_service():
    CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
    )
    flow.redirect_uri = 'http://localhost:5001/authorize-youtube/callback'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    # Update the redirect_uri in authorization_url to reflect port 5001
    authorization_url = authorization_url.replace('localhost:5000', 'localhost:5001')
    return jsonify({"authorization_url": authorization_url})

def handle_youtube_comments(data):
    action = data.get("action")
    video_id = data.get("video_id")
    comment_text = data.get("comment")

    CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')
    credentials = google_auth_oauthlib.flow.Credentials.from_authorized_user_file(os.getenv('YOUTUBE_CREDENTIALS_FILE'))
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )

    if action == "fetch":
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText"
        )
        response = request.execute()
        return jsonify(response)

    elif action == "post":
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        )
        response = request.execute()
        return jsonify(response)

    return jsonify({"message": "Invalid action specified."})