# src/routes/home.py

from flask import Blueprint, render_template
import pandas as pd
from src.models.fetch_schedule import fetch_schedule

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    df = fetch_schedule()

    if df.empty:
        return render_template('home.html', current_page="home", schedule=[])

    def is_completed(row):
        return pd.notna(row['HomeScore']) and pd.notna(row['AwayScore'])
    
    df['Completed'] = df.apply(is_completed, axis=1)
    print(df)

    completed = df[df['Completed']].sort_values(by='Round')
    upcoming = df[~df['Completed']].sort_values(by='Round')

    if len(upcoming) == 0:
        display_matches = completed.tail(6)
    else:
        completed_top = completed.tail(4)
        num_upcoming_needed = 6 - len(completed_top)
        upcoming_top = upcoming.head(num_upcoming_needed)
        display_matches = pd.concat([completed_top, upcoming_top]).sort_values(by='Round')

    return render_template('home.html', current_page="home", schedule=display_matches.to_dict(orient='records'))
