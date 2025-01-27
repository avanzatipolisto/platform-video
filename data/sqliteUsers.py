from data.sqliteClient import SqliteClient

class SqliteUsers:
    def __init__(self, database=SqliteClient()):
        self.sqliteClient=database
    def get_user_by_field(self, field, value):
        print ("pasado el valor ", field, value)
        self.sqliteClient.cursor.execute(f"SELECT * FROM users WHERE {field}='{value}'")
        tupla=self.sqliteClient.cursor.fetchall()
        return tupla
    def get_all_users(self):
        self.sqliteClient.cursor.execute("SELECT * FROM users")
        return self.sqliteClient.cursor.fetchall()
    def add_user(self, name, password, email, birddate, rol):
        self.sqliteClient.cursor.execute("insert into users (name, password, email, birddate, rol) values (?, ?, ?, ?,?)", (name, password, email, birddate, rol))
        self.sqliteClient.connection.commit()
    def update_user(self, id, name, password, email, birdate, rol):
        self.sqliteClient.cursor.execute(f"update users set name='{name}',password ='{password}', email='{email}', birddate='{birdate}', rol='{rol}'  where id = '{id}'")
        self.sqliteClient.connection.commit()
    def delete_user(self, id):
        self.sqliteClient.cursor.execute(f"delete from users where id = '{id}'")
        self.sqliteClient.connection.commit()
    def delete_all_users(self):
        self.sqliteClient.cursor.execute(f"delete from users")
        self.sqliteClient.connection.commit()
    
