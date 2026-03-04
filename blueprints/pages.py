from flask import Blueprint, get_flashed_messages, redirect, render_template, session, url_for, request
from scripts.isAuthorised import isAuthorised
from database import DatabaseHandler
from datetime import datetime

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

@pages.route("/workouts")
def workouts():
    if not isAuthorised():
        return redirect(url_for("pages.signin"))
    
    # retrieves the user's workout templates to be displayed on the workouts page
    db = DatabaseHandler()
    userID = db.getUserID(session["currentUser"])
    templates = db.getUserTemplates(userID)

    currentUser = session["currentUser"]
    return render_template("workouts.html", currentUser = currentUser, templates = templates)

@pages.route("/log_workout/<int:templateID>", methods=["GET", "POST"])
def log_workout(templateID):
    if not isAuthorised():
        return redirect(url_for("pages.signin"))

    #retrieves userID and exercises for the selected template 
    db = DatabaseHandler()
    userID = db.getUserID(session["currentUser"])
    exercises = db.getTemplateExercises(templateID)

    # if the user submits the form the workout data is saved 
    if request.method == "POST":
        notes = request.form.get("notes", "")

        # gets the current date and time to be stored with the workout data
        now = datetime.now()
        workoutDate = now.strftime("%Y-%m-%d")
        workoutTime = now.strftime("%H:%M:%S")

        # creates the workout and retrieves the workoutID and for saving each exercise
        workoutID = db.createWorkout(userID, templateID, workoutDate, workoutTime, notes)

        # saves the weight and reps for each exercise in the workout
        for exercise in exercises:
            exerciseID = exercise[0]
            order = exercise[2]
            weight = request.form.get("weight_" + str(order), "")
            reps = request.form.get("reps_" + str(order), "")

            db.addWorkoutData(workoutID, exerciseID, order, float(weight), int(reps))
                    
        return redirect(url_for("pages.workouts"))

    return render_template("log_workout.html", exercises=exercises)



