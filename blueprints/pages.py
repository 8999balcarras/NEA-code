from flask import Blueprint, get_flashed_messages, redirect, render_template, session, url_for, request
from scripts.isAuthorised import isAuthorised
from database import DatabaseHandler

pages = Blueprint("pages", __name__)

#runs the signin function when the url is visited
@pages.route("/")
def signin():
    if isAuthorised():
        return redirect(url_for("pages.dashboard"))
    #flashes the error message if signin is unsuccessful
    messages = get_flashed_messages()
    return render_template("signin.html", messages = messages)

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

@pages.route("/workout_templates")
def workout_templates():
    #signs out the user if they are not authorised
    if not isAuthorised():
        return redirect(url_for("pages.signin"))
    
    #retrieves the user's templates to be displayed
    db = DatabaseHandler()
    userID = db.getUserID(session["currentUser"])
    templates = db.getUserTemplates(userID)

    #renders the workout templates page with the user's templates
    currentUser = session["currentUser"]
    return render_template("workout_templates.html", currentUser = currentUser, templates = templates)

#handles the create template page and saving the template 
@pages.route("/create_template", methods=["GET", "POST"])
def create_template():
    db = DatabaseHandler()
    exercises = db.getExercises()

    #if the user submits the form, the template is created and the user is redirected
    if request.method == "POST":
        formDetails = request.form
        templateName = formDetails.get("templateName")
        exerciseIDs = formDetails.getlist("exerciseIDs")
        userID = db.getUserID(session["currentUser"])
        templateID = db.createTemplate(templateName, userID)
        db.addExercisesToTemplate(templateID, exerciseIDs)

        return redirect(url_for("pages.workout_templates"))
    return render_template('create_template.html', exercises=exercises)

@pages.route("/log_workout")
def log_workout():
    if not isAuthorised():
        return redirect(url_for("pages.signin"))
    currentUser = session["currentUser"]
    return render_template("log_workout.html", currentUser = currentUser)


