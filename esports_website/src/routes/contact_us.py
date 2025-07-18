# src/routes/contact_us.py

from flask import Blueprint, render_template

contact_us_bp = Blueprint('contact_us', __name__)

@contact_us_bp.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', current_page="contact")