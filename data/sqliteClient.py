import sqlite3
import os

class SqliteClient:
    def __init__(self):
        self.connection=None
        self.cursor=None
        self.SQLITE_DB="database.db"

    def connect(self):
        incializar_bd=False
        if not os.path.exists(self.SQLITE_DB):
            incializar_bd=True
        try:
            self.connection=sqlite3.connect(self.SQLITE_DB, check_same_thread=False)
            self.cursor=self.connection.cursor()
            self.cursor("PRAGMA foreign_keys=ON")
            self.connection.commit()

        except Exception as e:
            print("Exception: ", e)
        if incializar_bd:
            self.create_table_users()
            self.create_table_contents()
            self.create_table_users_contents()
            self.add_fake_users()
            self.add_fake_contents()
            self.add_fake_users_contents()
    def close(self):
        if self.connection!=None:
            self.connection.close()

    def create_table_users(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name varchar(255),
                                    password varchar(255),
                                    email varchar(50),
                                    birddate date,
                                    rol varchar(20) default 'normal'
                            );   
                            
                            """)
        self.connection.commit()
    def add_fake_users(self):
        self.cursor.executemany("insert into users (`name`, `password`, 'email', `birddate`, `rol`)values (?,?,?,?,?);",
            [
                ('admin','1234', 'admin@loretix.com', '1998-03-27', '1'),
                ('Kalo','1234', 'kaloy@gmail.com', '1998-03-27', '0'),
                ('juan','1234', 'juan@gmail.com', '1977-12-12', '0')
            ]
        )  
        self.connection.commit()

    def create_table_contents(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type varchar(20),
                    genre varchar(20),
                    ti8le varchar(255),
                    year integer,
                    image varchar(255),
                    clicks integer
            );         
            ''')
        self.connection.commit()

    def add_fake_contents(self):
        self.cursor.executemany("insert into contents (`type`, `genre`, `ti8le`, `year`, `image`, `clicks`)values (?,?,?,?,?,?);",
            [        
                ('pelicula','Acción','Mad Max: Furia en la carretera','2015','Peliculas/accion_1.jpg','0'),
                ('pelicula','Comedia','La jungla de cristal','1988','Peliculas/accion_2.jpg','4'),
                ('pelicula','Acción','Matrix','1999','Peliculas/accion_4.jpg','0'),
                ('pelicula','Acción','Gladiador','2000','Peliculas/accion_5.jpg','5'),
                ('pelicula','Acción','John Wick','2014','Peliculas/accion_6.jpg','0'),
                ('pelicula','Acción','Terminator 2: El juicio final','1991','Peliculas/accion_7.jpg','0'),
                ('pelicula','Acción','Avengers: Endgame','2019','Peliculas/accion_8.jpg','0'),
                ('pelicula','Comedia','La vida de Brian','1979','Peliculas/comedia_1.jpg','0'),
                ('pelicula','Comedia','Superbad','2007','Peliculas/comedia_2.jpg','0'),
                ('pelicula','Comedia','Toy Story','1995','Peliculas/comedia_3.jpg','3'),
                ('pelicula','Comedia','Zombieland','2009','Peliculas/comedia_4.jpg','0'),
                ('pelicula','Comedia','Un pez llamado Wanda','1988','Peliculas/comedia_5.jpg','0'),
                ('pelicula','Comedia','Despedida de soltero','1984','Peliculas/comedia_6.jpg','0'),
                ('pelicula','Comedia','Resacón en Las Vegas','2009','Peliculas/comedia_7.jpg','0'),
                ('pelicula','Comedia','El Gran Lebowski','1998','Peliculas/comedia_8.jpg','0'),
                ('pelicula','Drama','El Padrino','1972','Peliculas/drama_1.jpg','0'),
                ('pelicula','Drama','Forrest Gump','1994','Peliculas/drama_2.jpg','0'),
                ('pelicula','Drama','El Pianista','2002','Peliculas/drama_3.jpg','0'),
                ('pelicula','Drama','Cadena perpetua','1994','Peliculas/drama_4.jpg','0'),
                ('pelicula','Drama','La lista de Schindler','1993','Peliculas/drama_5.jpg','0'),
                ('pelicula','Drama','12 años de esclavitud','2013','Peliculas/drama_6.jpg','0'),
                ('pelicula','Drama','American Beauty','1999','Peliculas/drama_7.jpg','0'),
                ('pelicula','Drama','El Indomable Will Hunting','1997','Peliculas/drama_8.jpg','0'),
                ('pelicula','Fantasía','El Señor de los Anillos','2001','Peliculas/fantasia_1.jpg','0'),
                ('pelicula','Fantasía','Harry Potter y la piedra filosofal','2001','Peliculas/fantasia_2.jpg','0'),
                ('pelicula','Fantasía','Las Crónicas de Narnia','2005','Peliculas/fantasia_3.jpg','0'),
                ('pelicula','Fantasía','Alicia en el País de las Maravillas','2010','Peliculas/fantasia_4.jpg','0'),
                ('pelicula','Fantasía','El Laberinto del Fauno','2006','Peliculas/fantasia_5.jpg','0'),
                ('pelicula','Fantasía','Stardust: El misterio de la estrella','2007','Peliculas/fantasia_6.jpg','0'),
                ('pelicula','Fantasía','Maléfica','2014','Peliculas/fantasia_7.jpg','0'),
                ('pelicula','Fantasía','Willow','1988','Peliculas/fantasia_8.jpg','0'),
                ('pelicula','Terror','El Conjuro','2013','Peliculas/terror_1.jpg','0'),
                ('pelicula','Terror','El Exorcista','1973','Peliculas/terror_2.jpg','0'),
                ('pelicula','Terror','It','2017','Peliculas/terror_3.jpg','0'),
                ('pelicula','Terror','Psicosis','1960','Peliculas/terror_4.jpg','0'),
                ('pelicula','Terror','Paranormal Activity ','2007','Peliculas/terror_5.jpg','0'),
                ('pelicula','Terror','Hereditary','2018','Peliculas/terror_6.jpg','0'),
                ('pelicula','Terror','Insidious','2010','Peliculas/terror_7.jpg','0'),
                ('pelicula','Terror','Un Lugar Tranquilo','2018','Peliculas/terror_8.jpg','0'),
                ('pelicula','Romance','Titanic','1997','Peliculas/romance_1.jpg','0'),
                ('pelicula','Romance','Orgullo y Prejuicio','2005','Peliculas/romance_2.jpg','0'),
                ('pelicula','Romance','La La Land','2016','Peliculas/romance_3.jpg','0'),
                ('pelicula','Romance','El Diario de una Pasión','2004','Peliculas/romance_4.jpg','0'),
                ('pelicula','Romance','Romeo + Julieta','1996','Peliculas/romance_5.jpg','0'),
                ('pelicula','Romance','Amelie','2001','Peliculas/romance_6.jpg','0'),
                ('pelicula','Romance','Un Lugar en el Tiempo','1980','Peliculas/romance_7.jpg','0'),
                ('pelicula','Romance','El Guardaespaldas','1992','Peliculas/romance_8.jpg','0'),
                ('pelicula','Aventura','Jurassic Park','1993','Peliculas/aventura_1.jpg','0'),
                ('pelicula','Aventura','Indiana Jones: En busca del arca perdida','1981','Peliculas/aventura_2.jpg','0'),
                ('pelicula','Aventura','Piratas del Caribe: La maldición del Perla Negra','2003','Peliculas/aventura_3.jpg','0'),
                ('pelicula','Aventura','Avatar','2009','Peliculas/aventura_4.jpg','0'),
                ('pelicula','Aventura','La Isla del Tesoro','1950','Peliculas/aventura_5.jpg','0'),
                ('pelicula','Aventura','El Libro de la Selva','2016','Peliculas/aventura_6.jpg','0'),
                ('pelicula','Aventura','Up','2009','Peliculas/aventura_7.jpg','0'),
                ('pelicula','Aventura','La Odisea','1997','Peliculas/aventura_8.jpg','0'),
                ('pelicula','Thriller','El Silencio de los Corderos','1991','Peliculas/thriller_1.jpg','0'),
                ('pelicula','Thriller','Seven','1995','Peliculas/thriller_2.jpg','0'),
                ('pelicula','Thriller','Gone Girl','2014','Peliculas/thriller_3.jpg','0'),
                ('pelicula','Thriller','Shutter Island','2010','Peliculas/thriller_4.jpg','0'),
                ('pelicula','Thriller','El Maquinista','2004','Peliculas/thriller_5.jpg','0'),
                ('pelicula','Thriller','El Cisne Negro','2010','Peliculas/thriller_6.jpg','0'),
                ('pelicula','Thriller','Prisioneros','2013','Peliculas/thriller_7.jpg','0'),
                ('serie','Acción','24','2001','Series/accion_1.jpg','0'),
                ('serie','Acción','Arrow','2012','Series/accion_2.jpg','0'),
                ('serie','Acción','The Punisher','2017','Series/accion_3.jpg','0'),
                ('serie','Acción','Cobra Kai','2018','Series/accion_4.jpg','0'),
                ('serie','Comedia','Friends','1994','Series/comedia_1.jpg','0'),
                ('serie','Comedia','Brooklyn Nine-Nine','2013','Series/comedia_2.jpg','0'),
                ('serie','Comedia','The Office','2005','Series/comedia_3.jpg','0'),
                ('serie','Comedia','Parks and Recreation','2009','Series/comedia_4.jpg','0'),
                ('serie','Drama','Breaking Bad','2008','Series/drama_1.jpg','0'),
                ('serie','Drama','Los Soprano','1999','Series/drama_2.jpg','0'),
                ('serie','Drama','The Crown','2016','Series/drama_3.jpg','0'),
                ('serie','Drama','This Is Us','2016','Series/drama_4.jpg','0'),
                ('serie','Fantasía','Game of Thrones','2011','Series/fantasia_1.jpg','0'),
                ('serie','Fantasía','The Witcher','2019','Series/fantasia_2.jpg','0'),
                ('serie','Fantasía','His Dark Materials','2019','Series/fantasia_3.jpg','0'),
                ('serie','Fantasía','Merlín','2008','Series/fantasia_4.jpg','0'),
                ('serie','Terror','Stranger Things','2016','Series/terror_1.jpg','0'),
                ('serie','Terror','The Haunting of Hill House','2018','Series/terror_2.jpg','0'),
                ('serie','Terror','American Horror Story','2011','Series/terror_3.jpg','0'),
                ('serie','Terror','Penny Dreadful','2014','Series/terror_4.jpg','0'),
                ('serie','Romance','Outlander','2014','Series/romance_1.jpg','0'),
                ('serie','Romance','Bridgerton','2020','Series/romance_2.jpg','0'),
                ('serie','Romance','Jane the Virgin','2014','Series/romance_3.jpg','0'),
                ('serie','Romance','Poldark','2015','Series/romance_4.jpg','0'),
                ('serie','Aventura','The Mandalorian','2019','Series/aventura_1.jpg','0'),
                ('serie','Aventura','The Walking Dead','2010','Series/aventura_2.jpg','0'),
                ('serie','Aventura','Lost','2004','Series/aventura_3.jpg','0'),
                ('serie','Aventura','Vikings','2013','Series/aventura_4.jpg','0'),
                ('serie','Thriller','Mindhunter','2017','Series/thriller_1.jpg','0'),
                ('serie','Thriller','Sherlock','2010','Series/thriller_2.jpg','0'),
                ('serie','Thriller','True Detective','2014','Series/thriller_3.jpg','0'),
                ('serie','Thriller','Dexter','2006','Series/thriller_4.jpg','0'),
                ('pelicula','Thriller','No es país para viejos','2007','Peliculas/peliculas_9.jpg','0'),
                ('pelicula','Acción','Rambo','1982','Peliculas/peliculas_11.jpg','0'),
                ('pelicula','Acción','El Exorcista','1973','Peliculas/peliculas_12.jpg','0')          
            ]
        )  
        self.connection.commit()

    def create_table_users_contents(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users_contents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content_id INTEGER
        );''')
        self.connection.commit()

    def add_fake_users_contents(self):
        self.cursor.executemany("insert into users_contents (`user_id`, `content_id`)values (?,?);",
                                    [
                                        (2, 3), 
                                        (2, 4)
                                    ]
                                )
        self.connection.commit()

"""
    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
"""    
    
