
from data.sqliteClient import SqliteClient

class SqliteContents:
    def __init__(self, database=SqliteClient()):
        self.sqliteClient=database

    def get_all_contents(self):
        self.sqliteClient.cursor.execute("SELECT * FROM contents")
        return self.sqliteClient.cursor.fetchall()
    def get_all_films(self, page):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='pelicula' ORDER BY title LIMIT ?, 14", (page,))      
        tuple=self.sqliteClient.cursor.fetchall()
        return tuple
    def get_count_films(self)->int:
        self.sqliteClient.cursor.execute("SELECT count(*) FROM contents WHERE type='pelicula' ")      
        count=self.sqliteClient.cursor.fetchall()[0][0]
        return count
    def get_all_films_by_title_like(self,title):
        self.sqliteClient.cursor.execute("select * from contents where type='pelicula' AND title LIKE ?", ('%'+title+'%',))
        return self.sqliteClient.cursor.fetchall()
    def get_all_films_by_letter(self,letter,page):
        if (letter.isdigit()):
            self.sqliteClient.cursor.execute("select * from contents where type='pelicula' AND title LIKE '0%' OR title LIKE '1%' OR title LIKE '2%' OR title LIKE '3%' OR title LIKE '4%' OR title LIKE '5%' OR title LIKE '6%' OR title LIKE '7%' OR title LIKE '8%' OR title LIKE '9%' LIMIT ?,14", (page, ))
        else:
            self.sqliteClient.cursor.execute("select * from contents where type='pelicula' AND title LIKE ? LIMIT ?,14", (letter+'%', page))
        return self.sqliteClient.cursor.fetchall()
    def get_count_films_by_letter(self, letter)->int:
        self.sqliteClient.cursor.execute("SELECT count(*) FROM contents WHERE type='pelicula' AND title LIKE ?", (letter+'%',))     
        count=self.sqliteClient.cursor.fetchall()[0][0]
        return count
    def get_all_series_by_title_like(self,title):
        self.sqliteClient.cursor.execute("select * from contents where type='serie' AND title LIKE ?", ('%'+title+'%',))
        return self.sqliteClient.cursor.fetchall()
    def get_all_series(self, page):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='serie' ORDER BY title LIMIT ?, 14", (page,))      
        return self.sqliteClient.cursor.fetchall()
    def get_count_series(self)->int:
        self.sqliteClient.cursor.execute("SELECT count(*) FROM contents WHERE type='serie' ")      
        count=self.sqliteClient.cursor.fetchall()[0][0]
        return count
    def get_all_films_order_by_clicks(self, page):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='pelicula' ORDER BY clicks DESC LIMIT ?, 4", (page,))   
        return self.sqliteClient.cursor.fetchall()
    def get_all_series_order_by_clicks(self, page):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='serie' ORDER BY clicks DESC LIMIT ?, 4", (page,))   
        return self.sqliteClient.cursor.fetchall()
    def get_content_by_field(self, field, value):
        self.sqliteClient.cursor.execute(f"SELECT * FROM contents WHERE {field}={value}")
        return self.sqliteClient.cursor.fetchone()
    def get_all_series_by_letter(self,letter,page):
        if (letter.isdigit()):
            self.sqliteClient.cursor.execute("select * from contents where type='serie' AND title LIKE '0%' OR title LIKE '1%' OR title LIKE '2%' OR title LIKE '3%' OR title LIKE '4%' OR title LIKE '5%' OR title LIKE '6%' OR title LIKE '7%' OR title LIKE '8%' OR title LIKE '9%' LIMIT ?,14", (page, ))
        else:
            self.sqliteClient.cursor.execute("select * from contents where type='serie' AND title LIKE ? LIMIT ?,14", (letter+'%', page))
        return self.sqliteClient.cursor.fetchall()
    def get_count_series_by_letter(self, letter)->int:
        self.sqliteClient.cursor.execute("SELECT count(*) FROM contents WHERE type='serie' AND title LIKE ?", (letter+'%',))     
        count=self.sqliteClient.cursor.fetchall()[0][0]
        return count