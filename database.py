import sqlite3 as sql

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
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                         userID INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT NOT NULL UNIQUE,
                         password TEXT NOT NULL
                         );""")

    #insert sign up details entered by the user into the database
    def createUser(self, username, password):
        try:
            with self.connect() as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            return True
        except:
            return False

    #Checks that the sign in details entered by the user match details in the database
    def authoriseUser(self, username, password):
        try:
            with self.connect() as conn:
                results = conn.execute("SELECT userID FROM users WHERE username = ? AND password = ?", (username, password))
                userDetails = results.fetchone()
                if userDetails != None:
                    return True
                else:
                    return False

        except:
            return False
