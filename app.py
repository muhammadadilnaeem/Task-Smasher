# Importing Libraries
from flask import Flask
from flask import render_template
from flask import request , redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Setting up Flask App
app = Flask(__name__)


# Setting up Flask-Scss Extension
Scss(app)


# Setting Up Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask-database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # this will tell SQLAlchemy not to track modifications(only for deployment)
db = SQLAlchemy(app)  # initializing SQLAlchemy instance


# Setting Up Database Table
class Task(db.Model):  # these are all required by SQLAlchemy for the database
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    content = db.Column(db.String(200), nullable=False)  # these are all required by SQLAlchemy for the database which are not nullable
    completed = db.Column(db.Integer, default=0)  # this will be set to 0 by default to indicate that task is not completed
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # this will be automatically set to the current time when task is created

    # __repr__ method to show the content of the task
    def __repr__(self) -> str:
        return f"Task {self.id}"  # this will return the id of the task

# This will create the database table if it doesn't exist(Active this if you are using it locally)
with app.app_context():
    db.create_all()   

# Setting Up HomePage
@app.route("/", methods=["GET", "POST"])
def index():

    # Adding Task
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
        
    # See all current tasks
    else:
        tasks = Task.query.order_by(Task.date_created).all() # this will order the tasks by date created
        return render_template("index.html", tasks=tasks) # this will render the index.html template


# Deleting Task
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

# Edit the  Task
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"

    else:
        return render_template("update.html", task=task)





if __name__ == "__main__":  # this will run the app if this file is run directly
    # with app.app_context():
    #     db.create_all()     # Active this if you are using it locally
        app.run(debug=True)