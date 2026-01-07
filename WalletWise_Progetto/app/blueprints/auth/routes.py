from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from ...repositories.user_repositories import UserRepository

def _user_repo() -> UserRepository:
    return UserRepository(current_app.config["DB_PATH"])

@auth_bp.get("/register")
def register_page():
    return render_template("auth/register.html")

@auth_bp.post("/register")
def register_action():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if len(username) < 3:
        flash("Username troppo corto (min 3).")
        return redirect(url_for("auth.register_page"))

    if len(password) < 4:
        flash("Password troppo corta (min 4).")
        return redirect(url_for("auth.register_page"))

    if _user_repo().get_by_username(username):
        flash("Username già esistente.")
        return redirect(url_for("auth.register_page"))

    pw_hash = generate_password_hash(password)
    uid = _user_repo().create(username, pw_hash)

    session["user_id"] = uid
    session["username"] = username
    return redirect(url_for("main.dashboard"))

@auth_bp.get("/login")
def login_page():
    return render_template("auth/login.html")

@auth_bp.post("/login")
def login_action():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = _user_repo().get_by_username(username)
    if (user is None) or (not check_password_hash(user["password_hash"], password)):
        flash("Credenziali non valide.")
        return redirect(url_for("auth.login_page"))

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return redirect(url_for("main.dashboard"))

@auth_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))
