from exerciselist import defaultExercises
import sqlite3 as sql
from werkzeug.security import check_password_hash, generate_password_hash

#creates a class for database connections
class DatabaseHandler:
    def __init__(self, dbName = "appData.db"):
        self.dbName = dbName

    #creates a connection to the database so that operations can be carried out
    def connect(self):
        return sql.connect(self.dbName)
    
    #creates a table with all the necessary attributes for a user
    def createTables(self):
        with self.connect() as conn:
            #creates the users table
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                         userID INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT NOT NULL UNIQUE,
                         password TEXT NOT NULL
                         );""")
            
            #creates the exercises table, which contains necessary information about exercises
            conn.execute("""CREATE TABLE IF NOT EXISTS exercises (
	                    exerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
                        exerciseName TEXT NOT NULL UNIQUE,
	                    muscleGroup TEXT NOT NULL,
	                    description TEXT
                        );""")
            
            #creates the templates table, which holds the information about a template
            conn.execute("""CREATE TABLE IF NOT EXISTS templates (
                        templateID INTEGER PRIMARY KEY AUTOINCREMENT,
                        templateName TEXT NOT NULL,
                        userID INTEGER NOT NULL,
                        FOREIGN KEY (userID) REFERENCES users(userID)
                        );""")
            
            #creates the templateExercises table, which holds the exercises and order of the exercises in each template
            conn.execute("""CREATE TABLE IF NOT EXISTS templateExercises (
                        templateExerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
                        templateID INTEGER NOT NULL,
                        exerciseID INTEGER NOT NULL,
                        exerciseOrder INTEGER NOT NULL,
                        FOREIGN KEY (templateID) REFERENCES templates(templateID),
                        FOREIGN KEY (exerciseID) REFERENCES exercises(exerciseID)			
                    );""")
            
            #creates the workouts table, which holds the information about a workout when it is started
            conn.execute("""CREATE TABLE IF NOT EXISTS workouts ( 
                        workoutID INTEGER PRIMARY KEY AUTOINCREMENT,
                        userID INTEGER NOT NULL,
                        templateID INTEGER,
                        workoutDate TEXT NOT NULL,
                        workoutTime TEXT NOT NULL,
                        notes TEXT,
                        FOREIGN KEY (userID) REFERENCES users(userID),
                        FOREIGN KEY (templateID) REFERENCES templates(templateID) 
                        );""")
            
            #creates the workoutData table, which holds the information about each set of a workout
            conn.execute("""CREATE TABLE IF NOT EXISTS workoutData ( 
                        setID INTEGER PRIMARY KEY AUTOINCREMENT,
                        workoutID INTEGER NOT NULL, 
                        exerciseID INTEGER NOT NULL, 
                        setNumber INTEGER NOT NULL, weight REAL NOT NULL, 
                        reps INTEGER NOT NULL, 
                        FOREIGN KEY (workoutID) REFERENCES workouts(workoutID), 
                        FOREIGN KEY (exerciseID) REFERENCES exercises(exerciseID)
                        );""")

    #inserts user details into users database
    def createUser(self, username, password):
        try:
            #generates a hashed password
            hashed_password = generate_password_hash(password)
            with self.connect() as conn:
                #inserts the username and hashed password into the database
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username.lower(), hashed_password))
                conn.commit()
            return True
        except:
            return False

    #Checks that the sign in details entered by the user match details in the database
    def authoriseUser(self, username, password):
        try:
            with self.connect() as conn:
                #checks that the password entered matches the stored hashed password
                results = conn.execute("SELECT password FROM users WHERE username = ?", (username.lower(), ))
                stored_hash = results.fetchone()[0]
                return check_password_hash(stored_hash, password)
        except:
            return False
    
    #inserts the exercises from exerciselist.py into the exercises table
    def populateExercises(self):
        with self.connect() as conn:
            for exercise in defaultExercises:
                conn.execute("INSERT OR IGNORE INTO exercises (exerciseName, muscleGroup, description) VALUES (?, ?, ?)", exercise)


