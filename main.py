from flask import Flask, render_template, request
from database import DatabaseHandler
app = Flask(__name__)

#runs the signin function when the url is visited
@app.route("/")
def signin():
    #connects the route to the template
    return render_template("signin.html")

#runs the signup function when the "/signup" url is visited
@app.route("/signup")
def signup():
    return render_template("signup.html")

#runs the dashboard function when the "/dashboard" url is visited
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/auth/createuser", methods = ["POST"] )
def createuser():
    formDetails = request.form
    username = formDetails.get("username")
    password = formDetails.get("password")
    repassword = formDetails.get("repassword")

    #server side username validation
    if username == None:
        return "failed to create user, you must enter a username"
    if len(username)>15:
        return "failed to create user, username must be 15 characters or less"
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
        db.createUser(username, password)
        return "creating user for " + username + password + repassword


app.run(debug = True)