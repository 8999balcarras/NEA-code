from flask import Blueprint, redirect, render_template, session, url_for
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
    return render_template("signup.html")

#runs the dashboard function when the "/dashboard" url is visited
@pages.route("/dashboard")
def dashboard():
    if not isAuthorised():
        return redirect(url_for("pages.signin"))
    currentUser = session["currentUser"]
    return render_template("dashboard.html", currentUser = currentUser)