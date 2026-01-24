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

    def createUser(self, username, password):
        with self.connect() as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()






