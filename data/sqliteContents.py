from data.sqliteClient import SqliteClient

class SqliteContents:
    def __init__(self, database=SqliteClient()):
        self.sqliteClient=database

    def get_all_contents(self):
        self.sqliteClient.cursor.execute("SELECT * FROM contents")
        return self.sqliteClient.cursor.fetchall()
    def get_all_films(self):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='pelicula' LIMIT 21")    
        return self.sqliteClient.cursor.fetchall()
    
    def get_all_series(self):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='serie' LIMIT 21")    
        return self.sqliteClient.cursor.fetchall()
    def get_all_films_order_by_clicks(self):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='pelicula' ORDER BY clicks DESC LIMIT 6")
        return self.sqliteClient.cursor.fetchall()
    def get_all_series_order_by_clicks(self):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='serie' ORDER BY clicks DESC LIMIT 6")
        return self.sqliteClient.cursor.fetchall()

    def get_content_by_field(self, field, value):
        self.sqliteClient.cursor.execute(f"SELECT * FROM contents WHERE {field}=?", (value,))
        return self.sqliteClient.cursor.fetchone