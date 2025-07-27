# src/routes/teams.py

from flask import Blueprint, render_template

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/teams')
def teams():
    return render_template('teams.html', current_page="teams")