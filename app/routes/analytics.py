# File: app/routes/analytics.py
# Description: Analytics routes
from flask import Blueprint, jsonify
from app.services.analytics_service import get_analytics_data

analytics_bp = Blueprint('analytics_bp', __name__)

# Route to fetch analytics data
@analytics_bp.route('/api/v1/analytics', methods=['GET'])
def get_analytics():
    return jsonify(get_analytics_data())