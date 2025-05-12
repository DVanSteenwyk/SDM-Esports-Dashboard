from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db = SQLAlchemy(app)

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # Optional, useful for labeling recurrence series


# Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.Date)
    description = db.Column(db.Text)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=True)
    team = db.Column(db.String(50))  # Team Code
    color = db.Column(db.String(20))  # Color Code

    series = db.relationship('Series', backref='events')



with app.app_context():
    db.create_all()

@app.route("/")
def index():
    events = Event.query.all()
    event_dicts = [
        {
            "title": f"{e.team}" if e.team else e.title,
            "start": e.date.strftime("%Y-%m-%d"),
            "description": e.description,
            "color": e.color
        } for e in events
    ]
    return render_template("index.html", events=events, events_json=event_dicts)

@app.route("/add", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        title = request.form["title"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        description = request.form["description"]
        recurrence = request.form.get("recurrence")
        recurrence_end_raw = request.form.get("recurrence_end")
        recurrence_end = (
            datetime.strptime(recurrence_end_raw, "%Y-%m-%d").date()
            if recurrence_end_raw
            else None
        )

        team_colors = {
            'League of Legends':'#c89b3c',
            'Rocket League':'#068efc',
            'Valorant':'#bd3944',
            'Overwatch 2':'#f99e1a',
            'Super Smash Bros. Ultimate':'#dddddd',
            'Apex Legends':'#a4373d',
            'Rainbow Six Siege':'#39af31'
        }

        team = request.form.get("team")
        color = team_colors.get(team, '#A9A9A9')

        # Create a Series if it's a recurring event
        series = None
        if recurrence:
            series = Series()
            db.session.add(series)
            db.session.flush()  # Makes series.id available before committing

        # Function to create individual Event instances
        def add_single_event(d):
            e = Event(
                title=title,
                date=d,
                description=description,
                series_id=series.id if series else None,
                color=color,
                team=team
            )
            db.session.add(e)

        # Add the first event
        add_single_event(date)

        # Add recurring events if applicable
        if recurrence and recurrence_end:
            current = date
            if recurrence == "daily":
                delta = timedelta(days=1)
            elif recurrence == "weekly":
                delta = timedelta(weeks=1)
            elif recurrence == "monthly":
                delta = relativedelta(months=1)
            else:
                delta = None

            while delta and current + delta <= recurrence_end:
                current += delta
                add_single_event(current)

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("add_event.html")


@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == "POST":
        scope = request.form.get('scope')
        title = request.form['title']
        date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        description = request.form['description']

        if scope == 'all' and event.series_id:
            series = Event.query.filter_by(series_id = event.series_id).all()
            for e in series:
                e.title = title
                e.description = description
            db.session.commit()
        else:
            event.title = title
            event.date = date
            event.description = description
            db.session.commit()

        return redirect(url_for("index"))
    
    return render_template("edit_event.html", event=event)

@app.route('/delete/<int:event_id>', methods=['GET', 'POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        scope = request.form.get('scope')

        if scope == 'all' and event.series_id:
            events_to_delete = Event.query.filter_by(series_id=event.series_id).all()
            for e in events_to_delete:
                db.session.delete(e)
        else:
            db.session.delete(event)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('delete_event.html', event=event)



@app.route("/reset")
def reset_db():
    db.drop_all()
    db.create_all()
    return "Database reset!"

if __name__ == "__main__":
    app.run(debug=True)
