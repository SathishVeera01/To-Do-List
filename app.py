from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        current_task = request.form["content"]
        mytask = task(content=current_task)

        try:
            db.session.add(mytask)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR {e}"
    else:
        mytask = task.query.order_by(task.created).all()
        return render_template("index.html", tasks=mytask)

@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = task.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR {e}"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id: int):
    update_task = task.query.get_or_404(id)
    if request.method == "POST":
        update_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR {e}"
    else:
        return render_template("update.html", task=update_task)

