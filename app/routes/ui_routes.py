from flask import render_template, Blueprint

ui_bp = Blueprint('ui_bp', __name__)

@ui_bp.route('/')
def home():
    return render_template('home.html')

@ui_bp.route('/comments')
def comments():
    return render_template('comments.html')

@ui_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')
