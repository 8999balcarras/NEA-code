from flask import Blueprint, get_flashed_messages, redirect, render_template, session, url_for, request, flash
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

        # validation for the template creation
        if db.templateNameExists(templateName, userID):
            flash("failed to create template, template name already exists")
            return redirect(url_for("pages.create_template"))
        if templateName == None or len(templateName) == 0:
            flash("failed to create template, template name must not be left blank")
            return redirect(url_for("pages.create_template"))
        if len(templateName)>30:
            flash("failed to create template, template name must be 30 characters or less")
            return redirect(url_for("pages.create_template"))
        if len(exerciseIDs) == 0:
            flash("failed to create template, at least one exercise must be selected")
            return redirect(url_for("pages.create_template"))
        
        templateID = db.createTemplate(templateName, userID)
        db.addExercisesToTemplate(templateID, exerciseIDs)
        return redirect(url_for("pages.workout_templates"))
    
    messages = get_flashed_messages()
    return render_template('create_template.html', exercises=exercises, messages = messages)

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

        #creates an empty list to temporarily store workout data for each exercise
        workoutRows = []

        # saves the weight and reps for each exercise in the workout
        for exercise in exercises:
            exerciseID = exercise[0]
            order = exercise[2]
            weight = request.form.get("weight_" + str(order), "")
            reps = request.form.get("reps_" + str(order), "")

            # validation for the workout logging
            if reps == "":
                flash("failed to log workout, reps must not be left blank")
                return redirect(url_for("pages.log_workout", templateID=templateID))
            try:
                int(reps)
            except:
                flash("failed to log workout, reps must be a whole number")
                return redirect(url_for("pages.log_workout", templateID=templateID))
            if int(reps) < 1:
                flash("failed to log workout, reps must be at least 1")
                return redirect(url_for("pages.log_workout", templateID=templateID))
            if int(reps) > 100:
                flash("failed to log workout, reps must be 100 or less")
                return redirect(url_for("pages.log_workout", templateID=templateID))
            if weight == "" or int(weight) < 0:
                weight = 0
            if int(weight) > 1000:
                flash("failed to log workout, weight must be 1000 or less")
                return redirect(url_for("pages.log_workout", templateID=templateID))
            
            workoutRows.append((exerciseID, order, weight, reps))
        
        workoutID = db.createWorkout(userID, templateID, workoutDate, workoutTime, notes)
           
        # adds the workout data for each exercise in the workout to the database
        for exerciseID, order, weight, reps in workoutRows:
            db.addWorkoutData(workoutID, exerciseID, order, float(weight), int(reps))
           
        return redirect(url_for("pages.workout_history"))

    messages = get_flashed_messages()
    return render_template("log_workout.html", exercises = exercises, messages = messages)

@pages.route("/workout_history")
def workout_history():
    if not isAuthorised():
        return redirect(url_for("pages.signin"))

    # retrieves the user's workout history to be displayed on the workout history page
    db = DatabaseHandler()
    userID = db.getUserID(session["currentUser"])
    workouts = db.getUserWorkouts(userID)

    currentUser = session["currentUser"]
    return render_template("workout_history.html", currentUser = currentUser, workouts = workouts)

@pages.route("/delete_template/<int:templateID>", methods=["POST"])
def delete_template(templateID):
    if not isAuthorised():
        return redirect(url_for("pages.signin"))
    
    #deletes the template and redirects to workout templates page
    db = DatabaseHandler()
    db.deleteTemplate(templateID)
    return redirect(url_for("pages.workout_templates"))