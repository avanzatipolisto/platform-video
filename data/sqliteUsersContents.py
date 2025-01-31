from data.sqliteClient import SqliteClient

class SqliteUsersContents:
    def __init__(self, database=SqliteClient()):
        self.sqliteClient=database
    def get_user_content_by_field(self, field, value):
        print ("pasado el valor ", field, value)
        self.sqliteClient.cursor.execute(f"SELECT * FROM users_contents WHERE {field}='{value}'")
        tupla=self.sqliteClient.cursor.fetchall()
        return tupla
    def get_all_users_contents(self, page):
        self.sqliteClient.cursor.execute("SELECT * FROM users_contents LIMIT ?, 10", (page,))  
        return self.sqliteClient.cursor.fetchall()
    def get_all_users_contents_without_page(self):
        self.sqliteClient.cursor.execute("SELECT * FROM users_contents ")  
        return self.sqliteClient.cursor.fetchall()
    def get_count_users_contents(self)->int:
        self.sqliteClient.cursor.execute("SELECT count(*) FROM users_contents")      
        count=self.sqliteClient.cursor.fetchall()[0][0]
        return count
    def get_user_favorite_films(self, user_id):
        self.sqliteClient.cursor.execute(f"""
                                        select uc.id, uc.user_id, uc.content_id, co.id, co.type, co.genre, co.title, co.year, co.image, co.clicks
                                        from contents co 
                                        inner join users_contents uc on co.id=uc.content_id
                                        where co.type ='film'
                                        and uc.user_id={user_id}
                                         """)
        return self.sqliteClient.cursor.fetchall()
    def get_user_favorite_series(self, user_id):
        self.sqliteClient.cursor.execute(f"""
                                        select uc.id, uc.user_id, uc.content_id, co.id, co.type, co.genre, co.title, co.year, co.image, co.clicks
                                        from contents co  
                                        inner join users_contents uc on co.id=uc.content_id 
                                        where co.type ='serie'
                                        and uc.user_id={user_id}
                                         """)
        return self.sqliteClient.cursor.fetchall()
    def add_user_content(self, user_id, content_id):
        self.sqliteClient.cursor.execute("insert into users_contents (user_id, content_id) values (?, ?)", (user_id, content_id))
        self.sqliteClient.connection.commit()
    def update_user_content(self, id, user_id, content_id):
        self.sqliteClient.cursor.execute(f"update users_contents set user_id='{user_id}',content_id ='{content_id}' where id = '{id}'")
        self.sqliteClient.connection.commit()
    def delete_user_content(self, id):
        self.sqliteClient.cursor.execute(f"delete from users_contents where id = '{id}'")
        self.sqliteClient.connection.commit()
    def delete_user_content_by_user_id_and_content_id(self, user_id, content_id):
        #print("borrado el usersids ", user_id, "content id ", content_id)
        self.sqliteClient.cursor.execute(f"delete from users_contents where user_id = '{user_id}' and content_id = '{content_id}' ")
        self.sqliteClient.connection.commit()
    def delete_all_users_contents(self):
        self.sqliteClient.cursor.execute(f"delete from users_contents")
        self.sqliteClient.connection.commit()