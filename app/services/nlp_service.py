# File: app/services/nlp_service.py
# Description: Handles NLP processing logic
from transformers import pipeline
from flask import jsonify

# Load a pre-trained FLAN-T5 text generation model
nlp_model = pipeline('text2text-generation', model='google/flan-t5-base')

def generate_nlp_response(data):
    user_comment = data.get("comment")
    # Generate a response using the FLAN-T5 model
    generated_response = nlp_model(user_comment, max_length=50, num_return_sequences=1)[0]['generated_text']
    return jsonify({"response": generated_response})
