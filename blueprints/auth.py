from flask import Blueprint, redirect, request, session, url_for

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
        return "failed to create user, you must enter a username"
    if len(username)>15:
        return "faile d to create user, username must be 15 characters or less"
    if not username.isalnum():
        return "failed to create user, username must only contain letters and numbers"
    
    #client side password validation
    if password != repassword:
        return "failed to create user, passwords do not match"
    if len(password)<5:
        return "failed to create user, passwords must be a minimum of 5 characters"
    if password.isalpha() or password.isdigit():
        return "failed to create user, passwords must be a mixture of letters and numbers"

    #creates user if validation is successful
    else:
        db = DatabaseHandler()
        success = db.createUser(username, password)
        if success:
            return redirect(url_for("pages.dashboard"))
        else:
            return "failed to create user, the username is not unique"

    return redirect(url_for("pages.signup"))

@auth.route("/signout")
def signOut():
    session.clear()
    return redirect(url_for("pages.signin"))