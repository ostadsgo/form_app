import sqlite3

class Database:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        if self.connection:
            return # already connected 

        try:
            with sqlite3.connect(self.db_filename) as conn:
                self.connection = conn
                self.cursor = conn.cursor()
                print("Succesfuly connect to db.")
        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)


    def execute(self, query, params=()):
        if not self.connection:
            print("No database connection established")
            return

        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error executing query: {e}\nQuery: {query}")

    def fetch_all(self, query, params=()):
        if not self.connection:
            print("No database connection established")
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}\nQuery: {query}")

    def fetch_one(self, query, params=()):
        if not self.connection:
            print("No database connection established")
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}\nQuery: {query}")


class FormModel:
    def __init__(self):
        self.db = Database("forms.db")

    def field_types(self):
        sql = """ SELECT name FROM types; """
        types = self.db.fetch_all(sql)
        return [value for item in types for value in item]




class InfoModel:
    pass

class ReportModel:
    pass

