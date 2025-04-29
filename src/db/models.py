import sqlite3


class Database:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        if self.connection:
            return  # already connected

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
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error executing query: {e}\nQuery: {query}")

    def executemany(self, query, params=()):
        if not self.connection:
            print("No database connection established")
            return

        try:
            self.cursor.executemany(query, params)
            self.connection.commit()
            return self.cursor.rowcount
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

    def save_form(self, name, rows):
        # Save table name - form name
        sql = """INSERT INTO forms(name) VALUES (?)"""
        tid = self.db.execute(sql, (name,))

        sql = """ INSERT INTO fields (name, type, form_id) VALUES (?, ?, ?)"""
        rows = [(*row, tid) for row in rows]
        self.db.executemany(sql, rows)
        print(f"Table {name} with id {tid} stored with fields succussfully.")

    def get_form_names(self):
        sql = """ SELECT name FROM forms; """
        names = self.db.fetch_all(sql)
        return [name for row in names for name in row]

    def get_form_fields(self, fid):
        sql = """ SELECT * FROM fields WHERE form_id = (?); """
        fields = self.db.fetch_all(sql, (fid,))
        # Field name and field type
        return [(field[1], field[2]) for field in fields]

    def get_form_fields_with_id(self, fid):
        sql = """ SELECT * FROM fields WHERE form_id = (?); """
        fields = self.db.fetch_all(sql, (fid,))
        # Field name and field type
        return fields

    def get_forms(self):
        sql = """ SELECT * FROM forms; """
        fidname = self.db.fetch_all(sql)
        return fidname

    def update_form_name(self, fid, new_name):
        sql = """ UPDATE forms SET name = ? WHERE id = ?;""" 
        self.db.execute(sql, (new_name, fid))
        print("form name updated successfuly.")
        return True

    def update_form_fields(self, fields):
        sql = """ UPDATE fields 
                  SET name = ?, type = ?
                  WHERE id = ?;""" 
        self.db.executemany(sql, fields)
        print("form name updated successfuly.")
        return True


class DataModel:
    def __init__(self):
        self.db = Database("forms.db")

    def get_form_names(self):
        sql = """ SELECT name FROM forms; """
        names = self.db.fetch_all(sql)
        return [name for row in names for name in row]
    
    def get_form_id(self, name):
        sql = """ SELECT id FROM forms WHERE name = (?); """
        fid = self.db.fetch_one(sql, (name,))
        return fid[0]

    def get_form_name(self, fid):
        sql = """ SELECT name FROM forms WHERE id = (?); """
        form_name = self.db.fetch_one(sql, (fid,))
        return form_name[0]


    def get_form_fields(self, fid):
        sql = """ SELECT * FROM fields WHERE form_id = (?); """
        fields = self.db.fetch_all(sql, (fid,))
        # Field name and field type
        return [(field[1], field[2]) for field in fields]

