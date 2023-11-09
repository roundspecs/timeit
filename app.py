from datetime import datetime, timedelta

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(200),
        nullable=False,
    )
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stop_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Task: #{self.name}>"

    def get_duration(self) -> str:
        duration: timedelta = self.stop_time - self.start_time
        duration_in_seconds = int(duration.total_seconds())
        minutes = duration_in_seconds // 60
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours:02}h {minutes:02}m"


@app.get("/")
def home():
    tasks = []
    i = 1
    current_task = None
    for task in Task.query.order_by(Task.stop_time).all():
        if task.stop_time != None:
            tasks.append(
                {
                    "sl": i,
                    "id": task.id,
                    "name": task.name,
                    "duration": task.get_duration(),
                }
            )
            i += 1
        else:
            current_task = task
    return render_template(
        "index.html",
        tasks=tasks,
        theme=request.args.get("theme", "light"),
        current_task=current_task,
    )


@app.post("/stop/<int:id>")
def stop(id):
    task = Task.query.get(id)
    task.stop_time = datetime.utcnow()
    db.session.commit()
    return redirect(url_for("home") + "?theme=" + request.args.get("theme", "light"))


@app.get("/edit/<int:id>")
def edit(id):
    task = Task.query.get(id)
    return render_template(
        "edit.html",
        task=task,
        theme=request.args.get("theme", "light"),
    )


@app.post("/update/<int:id>")
def update(id):
    task = Task.query.get(id)
    task.name = request.form["name"]
    db.session.commit()
    return redirect(url_for("home") + "?theme=" + request.args.get("theme", "light"))


@app.get("/delete/<int:id>")
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home") + "?theme=" + request.args.get("theme", "light"))

@app.post("/add")
def add():
    for task in Task.query.all():
        if task.stop_time == None:
            task.stop_time = datetime.utcnow()
    task = Task(name=request.form["name"])
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("home") + "?theme=" + request.args.get("theme", "light"))