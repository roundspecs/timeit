from datetime import datetime
from flask import Flask, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, )
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stop_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Task: #{self.name}"

tasks = [
    {"sl": 1, "id":123, "name": "Make a time tracker website", "duration": "1 hour"},
    {"sl": 2, "id":122, "name": "Make a sandwich", "duration": "30 min"},
]

current_task = "academics"


@app.get("/")
def home():
    return render_template(
        "index.html",
        tasks=tasks,
        theme=request.args.get("theme", "light"),
        current_task=current_task,
    )


@app.get("/edit/<int:id>")
def edit(id):
    return render_template(
        "edit.html", tasks=tasks, theme=request.args.get("theme", "light")
    )
