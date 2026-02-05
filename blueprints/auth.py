from flask import Blueprint, flash, redirect, request, session, url_for

from database import DatabaseHandler

auth = Blueprint("auth", __name__, url_prefix = "/auth")

#signs in the user after they enter their username and password
@auth.route("/authoriseuser", methods = ["POST"])
def authoriseuser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")

    #redirects to /dashboard if sign in worked or /signin if sign in failed
    db = DatabaseHandler()
    success = db.authoriseUser(username, password)
    if success:
        session["currentUser"] = username
        return redirect(url_for("pages.dashboard"))
    else:
        return redirect(url_for("pages.signin"))


@auth.route("/createuser", methods = ["POST"] )
def createuser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")
    repassword = formDetails.get("repassword")
    
    #server side username validation
    if username == None:
        flash("failed to create username, you must enter a username")
        return redirect(url_for("pages.signup"))
    if len(username)>15:
        flash("failed to create user, username must be 15 characters or less")
        return redirect(url_for("pages.signup"))
    if not username.isalnum():
        flash("failed to create user, username must only contain letters and numbers")
        return redirect(url_for("pages.signup"))
    #client side password validation
    if password != repassword:
        flash("failed to create user, passwords do not match")
        return redirect(url_for("pages.signup"))
    if len(password)<5:
        flash("failed to create user, passwords must be a minimum of 5 characters")
        return redirect(url_for("pages.signup"))
    if password.isalpha() or password.isdigit():
        flash("failed to create user, passwords must be a mixture of letters and numbers")
        return redirect(url_for("pages.signup"))  

    #creates user if validation is successful
    else:
        db = DatabaseHandler()
        success = db.createUser(username, password)
        if success:
            return redirect(url_for("pages.dashboard"))
        else:
            flash("failed to create user, the username is not unique")
            return redirect(url_for("pages.signup"))

    return redirect(url_for("pages.signup"))

@auth.route("/signout")
def signOut():
    session.clear()
    return redirect(url_for("pages.signin"))