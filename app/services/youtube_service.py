# File: app/services/youtube_service.py
# Description: Handles YouTube API calls

import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
from flask import jsonify
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from app.services.nlp_service import generate_nlp_response
import logging

# Set up logging to get more detailed output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    comment_id = data.get("comment_id")  # The ID of the comment being replied to
    comment_text = data.get("comment")
    page_token = data.get("page_token", None)  # Optional, for pagination

    CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')
    credentials_file = os.getenv('YOUTUBE_CREDENTIALS_FILE')

    # Load credentials from the credentials file
    try:
        logger.info("Loading credentials from file...")
        credentials = Credentials.from_authorized_user_file(credentials_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
        logger.info("Credentials loaded successfully.")
    except FileNotFoundError:
        logger.error("YouTube credentials file not found.")
        return jsonify({"error": "YouTube credentials file not found."}), 404
    except Exception as e:
        logger.error(f"An error occurred while loading credentials: {str(e)}")
        return jsonify({"error": f"An error occurred while loading credentials: {str(e)}"}), 500

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )

    try:
        if action == "fetch":
            logger.info(f"Fetching comments for video: {video_id}")
            # Add pageToken for pagination if provided
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                pageToken=page_token  # Include the page token if provided
            )
            response = request.execute()
            logger.info("Comments fetched successfully.")
            return jsonify(response)

        elif action == "post":
            logger.info(f"Posting comment on video: {video_id}")
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
            logger.info("Comment posted successfully.")
            return jsonify(response)

        elif action == "reply":
            logger.info(f"Replying to comment: {comment_id}")
            # Generate a response using the NLP model
            nlp_response = generate_nlp_response({"comment": comment_text}).json["response"]
            logger.info(f"NLP response generated: {nlp_response}")

            # Use the YouTube API to reply to the comment
            request = youtube.comments().insert(
                part="snippet",
                body={
                    "snippet": {
                        "parentId": comment_id,
                        "textOriginal": nlp_response
                    }
                }
            )
            response = request.execute()
            logger.info("Reply posted successfully.")
            return jsonify(response)

    except HttpError as e:
        # Handle specific YouTube API errors
        error_content = e.content.decode("utf-8")
        logger.error(f"YouTube API error: {error_content}")
        return jsonify({"error": "YouTube API error", "details": error_content}), 400
    except Exception as e:
        # Handle other errors
        logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

    return jsonify({"message": "Invalid action specified."}), 400