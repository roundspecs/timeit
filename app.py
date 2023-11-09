from flask import Flask, request, url_for, render_template
app = Flask(__name__)

tasks = [
  {"sl":1, "name":"Make a time tracker website", "duration": "1 hour"},
  {"sl":2, "name":"Make a sandwich", "duration": "30 min"},
]

current_task = "academics"

@app.get("/")
def home():
  dark_theme = request.args.get('theme', "light") == "dark"
  print(request.args.get('theme', "light"), dark_theme)
  return render_template("index.html", tasks=tasks, dark_theme=dark_theme, current_task=current_task)

@app.get("/edit/<int:id>")
def edit(id):
  dark_theme = request.args.get('theme', "light") == "dark"
  print(request.args.get('theme', "light"), dark_theme)
  return render_template("edit.html", tasks=tasks, dark_theme=dark_theme)