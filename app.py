# Flask App
from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient

app = Flask(__name__)
uri = "mongodb+srv://Vishnusiva:vishnusiva@cluster0.fcphozc.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["flask_database"]
todos = db["todos"]

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        todo = request.form['todo']
        degree = request.form['degree']
        todos.insert_one({"todo": todo, "degree": degree})
        return redirect(url_for("index"))
    
    all_todos = list(todos.find())
    return render_template("index.html", all_todos=all_todos)

@app.route("/del/<name>", methods=['GET', 'POST'])
def delete(name):
    todos.delete_one({"todo": name})
    return redirect(url_for("index"))

@app.route("/update/<name>", methods=['GET', 'POST'])
def update(name):
    if request.method == 'POST':
        new_todo = request.form['todo']
        new_degree = request.form['degree']
        todos.update_one({"todo": name}, {"$set": {"todo": new_todo, "degree": new_degree}})
        return redirect(url_for("index"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
