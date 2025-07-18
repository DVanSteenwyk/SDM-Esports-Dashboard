# src/routes/sponsors.py

from flask import Blueprint, render_template

sponsors_bp = Blueprint('sponsors', __name__)

@sponsors_bp.route('/sponsors')
def sponsors():
    return render_template('sponsors.html')