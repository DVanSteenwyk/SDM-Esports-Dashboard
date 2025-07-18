# src/routes/schedule.py

from flask import Blueprint, render_template

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('/schedule')
def schedule():
    return render_template('schedule.html', current_page="schedule")