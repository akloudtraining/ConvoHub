# File: app/__init__.py
# Description: Initializes the Flask application
from flask import Flask
from app.routes.youtube import youtube_bp
from app.routes.nlp import nlp_bp
from app.routes.analytics import analytics_bp
from app.routes.comments import comments_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(youtube_bp)
app.register_blueprint(nlp_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(comments_bp)

# Health check route
@app.route('/')
def health_check():
    return "ConvoHub is up and running!"