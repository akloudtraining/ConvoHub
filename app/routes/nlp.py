# File: app/routes/nlp.py
# Description: NLP response generation route
from flask import Blueprint, request, jsonify
from app.services.nlp_service import generate_nlp_response

nlp_bp = Blueprint('nlp_bp', __name__)

# Route for NLP response generation
@nlp_bp.route('/api/v1/generate-response', methods=['POST'])
def generate_response():
    return generate_nlp_response(request.json)