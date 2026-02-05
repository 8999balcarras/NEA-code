from flask import Blueprint, get_flashed_messages, redirect, render_template, session, url_for
from scripts.isAuthorised import isAuthorised

pages = Blueprint("pages", __name__)

#runs the signin function when the url is visited
@pages.route("/")
def signin():
    if isAuthorised():
        return redirect(url_for("pages.dashboard"))
    #connects the route to the template
    return render_template("signin.html")

#runs the signup function when the "/signup" url is visited
@pages.route("/signup")
def signup():
    messages = get_flashed_messages()
    return render_template("signup.html", messages = messages)


#runs the dashboard function when the "/dashboard" url is visited
@pages.route("/dashboard")
def dashboard():
    if not isAuthorised():
        return redirect(url_for("pages.signin"))
    currentUser = session["currentUser"]
    return render_template("dashboard.html", currentUser = currentUser)