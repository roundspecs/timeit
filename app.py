from flask import Flask, request, url_for, render_template

app = Flask(__name__)

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
