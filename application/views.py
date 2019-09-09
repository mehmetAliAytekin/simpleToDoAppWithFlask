from application import app
from flask import render_template, request, redirect, url_for, session
from application.models import User, ToDo, db
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        req = request.form
        user = User.query.filter_by(username=req.get("username"), password=req.get("password")).first()
        if user:
            session['user_id'] = user.id
            todo_list = ToDo.query.filter_by(userid=user.id)
            return render_template("todo.html", todos=todo_list)
        else:
            return render_template("signin.html")


@app.route("/complete/<todo_id>")
@login_required
def complete(todo_id):
    user_id = session['user_id']
    todo_updated = ToDo.query.filter_by(id=todo_id, userid=user_id).first()
    if todo_updated:
        todo_updated.complete = not todo_updated.complete
        db.session.commit()
    todo_list = ToDo.query.filter_by(userid=user_id)
    return render_template("todo.html", todos=todo_list)


@app.route("/delete/<todo_id>")
@login_required
def delete(todo_id):
    user_id = session['user_id']
    todo_deleted = ToDo.query.filter_by(id=todo_id, userid=user_id).first()
    if todo_deleted:
        db.session.delete(todo_deleted)
        db.session.commit()
    todo_list = ToDo.query.filter_by(userid=user_id)
    return render_template("todo.html", todos=todo_list)


@app.route("/add", methods=["POST"])
@login_required
def add():
    req = request.form
    user_id = session['user_id']
    todo = ToDo(userid=user_id, title=req.get("toDoTitle"), description=req.get("toDoDescription"), complete=False)
    db.session.add(todo)
    db.session.commit()
    todo_list = ToDo.query.filter_by(userid=user_id)
    return render_template("todo.html", todos=todo_list)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route("/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        req = request.form
        new_user = User(username=req.get("username"), password=req.get("password"))
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("login.html")
