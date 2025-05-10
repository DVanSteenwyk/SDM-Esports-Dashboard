from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory list to store events
events = []

@app.route("/")
def index():
    return render_template("index.html", events=events)

@app.route("/add", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        description = request.form["description"]
        events.append({
            "title": title, 
            "date": date, 
            "description": description})
        return redirect(url_for("index"))
    return render_template("add_event.html")

if __name__ == "__main__":
    app.run(debug=True)
