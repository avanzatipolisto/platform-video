
from data.sqliteClient import SqliteClient

class SqliteContents:
    def __init__(self, database=SqliteClient()):
        self.sqliteClient=database

    def get_all_contents(self, page=0):
        self.sqliteClient.cursor.execute("SELECT * FROM contents ORDER BY id DESC LIMIT ?, 10", (page,))   
        return self.sqliteClient.cursor.fetchall()
    def get_all_contents_without_page(self):
        self.sqliteClient.cursor.execute("SELECT * FROM contents ORDER BY title")   
        return self.sqliteClient.cursor.fetchall()
    def get_count_contents(self)->int:
        self.sqliteClient.cursor.execute("SELECT count(*) FROM contents")      
        count=self.sqliteClient.cursor.fetchall()[0][0]
        return count
    def get_all_films(self, page):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='film' ORDER BY title LIMIT ?, 14", (page,))      
        tuple=self.sqliteClient.cursor.fetchall()
        return tuple
    def get_count_films(self)->int:
        self.sqliteClient.cursor.execute("SELECT count(*) FROM contents WHERE type='film' ")      
        count=self.sqliteClient.cursor.fetchall()[0][0]
        return count
    def get_all_films_order_by_clicks(self, page):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='film' ORDER BY clicks DESC LIMIT ?, 4", (page,))   
        return self.sqliteClient.cursor.fetchall()
    def get_all_films_by_title_like(self,title):
        self.sqliteClient.cursor.execute("select * from contents where type='film' AND title LIKE ?", ('%'+title+'%',))
        return self.sqliteClient.cursor.fetchall()
    def get_all_films_by_letter(self,letter,page):
        if (letter.isdigit()):
            self.sqliteClient.cursor.execute("select * from contents where type='film' AND title LIKE '0%' OR title LIKE '1%' OR title LIKE '2%' OR title LIKE '3%' OR title LIKE '4%' OR title LIKE '5%' OR title LIKE '6%' OR title LIKE '7%' OR title LIKE '8%' OR title LIKE '9%' LIMIT ?,14", (page, ))
        else:
            self.sqliteClient.cursor.execute("select * from contents where type='film' AND title LIKE ? LIMIT ?,14", (letter+'%', page))
        return self.sqliteClient.cursor.fetchall()
    def get_count_films_by_letter(self, letter)->int:
        self.sqliteClient.cursor.execute("SELECT count(*) FROM contents WHERE type='film' AND title LIKE ?", (letter+'%',))     
        count=self.sqliteClient.cursor.fetchall()[0][0]
        return count
        contents


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
    def get_all_series_order_by_clicks(self, page):
        self.sqliteClient.cursor.execute("SELECT * FROM contents WHERE type='serie' ORDER BY clicks DESC LIMIT ?, 4", (page,))   
        return self.sqliteClient.cursor.fetchall()
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
    

    def get_content_by_field(self, field, value):
        self.sqliteClient.cursor.execute(f"SELECT * FROM contents WHERE {field}='{value}'")
        tupla=self.sqliteClient.cursor.fetchall()
        return tupla
    
    def add_content(self, type, genre, title, year, image, clicks):
        self.sqliteClient.cursor.execute("insert into contents (type, genre, title, year, image, clicks) values (?, ?, ?, ?, ?, ?)", (type, genre, title, year, image, clicks))
        self.sqliteClient.connection.commit()
    def update_content(self, id, type, genre, title, year, image, clicks):
        print("vamos a actualizar: ",id, type, genre, title, year, image, clicks)
        self.sqliteClient.cursor.execute(f"update contents set type='{type}', genre ='{genre}', title='{title}', year='{year}', image='{image}', clicks='{clicks}' where id = '{id}'")
        self.sqliteClient.connection.commit()
    def delete_content(self, id):
        self.sqliteClient.cursor.execute(f"delete from contents where id = '{id}'")
        self.sqliteClient.connection.commit()
    def delete_all_contents(self):
        self.sqliteClient.cursor.execute(f"delete from contents")
        self.sqliteClient.connection.commit()
        