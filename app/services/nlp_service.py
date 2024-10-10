# File: app/services/nlp_service.py
# Description: Handles NLP processing logic
from transformers import pipeline
from flask import jsonify

# Load a pre-trained text-generation model
nlp_model = pipeline('text-generation', model='gpt2')

def generate_nlp_response(data):
    user_comment = data.get("comment")
    generated_response = nlp_model(user_comment, max_length=30, num_return_sequences=1)[0]['generated_text']
    return jsonify({"response": generated_response})