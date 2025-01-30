import sqlite3
import os
from utils.file_manager import copy_assets

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
            self.cursor.execute("PRAGMA foreign_keys=ON");
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
            self.copy_assets("assets", "static")
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
                ('admin','1234', 'admin@loretix.com', '1998-03-27', 'admin'),
                ('kalo','1234', 'kaloy@gmail.com', '1998-03-27', 'normal'),
                ('juan','1234', 'juan@gmail.com', '1977-12-12', 'normal')
            ]
        )  
        self.connection.commit()

    def create_table_contents(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type varchar(20),
                    genre varchar(20),
                    title varchar(255),
                    year integer,
                    image varchar(255),
                    clicks integer
            );         
            ''')
        self.connection.commit()

    def add_fake_contents(self):
        self.cursor.executemany("insert into contents (`type`, `genre`, `title`, `year`, `image`, `clicks`)values (?,?,?,?,?,?);",
            [        
                ('film','Acción','Mad Max: Furia en la carretera','2015','films/Mad_Max_Furia_en_la_carretera.jpg','0'),
                ('film','Comedia','La jungla de cristal','1988','films/La_jungla_de_cristal.jpg','4'),
                ('film','Acción','Matrix','1999','films/Matrix.jpg','0'),
                ('film','Acción','Gladiador','2000','films/Gladiador.jpg','5'),
                ('film','Acción','John Wick','2014','films/John_Wick.jpg','0'),
                ('film','Acción','Terminator 2: El juicio final','1991','films/Terminator_2_El_juicio_final.jpg','0'),
                ('film','Acción','Avengers: Endgame','2019','films/Avengers_Endgame.jpg','0'),
                ('film','Comedia','La vida de Brian','1979','films/La_vida_de_Brian.jpg','0'),
                ('film','Comedia','Superbad','2007','films/Superbad.jpg','0'),
                ('film','Comedia','Toy Story','1995','films/Toy_Story.jpg','3'),
                ('film','Comedia','Zombieland','2009','films/Zombieland.jpg','0'),
                ('film','Comedia','Un pez llamado Wanda','1988','films/Un_pez_llamado_Wanda.jpg','0'),
                ('film','Comedia','Despedida de soltero','1984','films/Despedida_de_soltero.jpg','0'),
                ('film','Comedia','Resacón en Las Vegas','2009','films/Resacon_en_Las_Vegas.jpg','0'),
                ('film','Comedia','El Gran Lebowski','1998','films/El_Gran_Lebows.jpg','0'),
                ('film','Drama','El Padrino','1972','films/El_Padrino.jpg','0'),
                ('film','Drama','Forrest Gump','1994','films/Forrest_Gump.jpg','0'),
                ('film','Drama','El Pianista','2002','films/El_Pianista.jpg','0'),
                ('film','Drama','Cadena perpetua','1994','films/Cadena_perpetua.jpg','0'),
                ('film','Drama','La lista de Schindler','1993','films/La_lista_de_Schindler.jpg','0'),
                ('film','Drama','12 años de esclavitud','2013','films/12_anos_de_esclavitud.jpg','0'),
                ('film','Drama','American Beauty','1999','films/American_Beauty.jpg','0'),
                ('film','Drama','El Indomable Will Hunting','1997','films/El_Indomable_Will_Hunting.jpg','0'),
                ('film','Fantasía','El Señor de los Anillos','2001','films/El_Senor_de_los_Anillos.jpg','0'),
                ('film','Fantasía','Harry Potter y la piedra filosofal','2001','films/Harry_Potter_y_la_piedra_filosofal.jpg','0'),
                ('film','Fantasía','Las Crónicas de Narnia','2005','films/Las_Cronicas_de_Narnia.jpg','0'),
                ('film','Fantasía','Alicia en el País de las Maravillas','2010','films/Alicia_en_el_Pais_de_las_Maravillas.jpg','0'),
                ('film','Fantasía','El Laberinto del Fauno','2006','films/El_Laberinto_del_Fauno.jpg','0'),
                ('film','Fantasía','Stardust: El misterio de la estrella','2007','films/Stardust_El_misterio_de_la_estrella.jpg','0'),
                ('film','Fantasía','Maléfica','2014','films/Malefica.jpg','0'),
                ('film','Fantasía','Willow','1988','films/Willow.jpg','0'),
                ('film','Terror','El Conjuro','2013','films/El_Conjuro.jpg','0'),
                ('film','Terror','El Exorcista','1973','films/El_Exorcista.jpg','0'),
                ('film','Terror','It','2017','films/It.jpg','0'),
                ('film','Terror','Psicosis','1960','films/Psicosis.jpg','0'),
                ('film','Terror','Paranormal Activity ','2007','films/Paranormal_Activity.jpg','0'),
                ('film','Terror','Hereditary','2018','films/Hereditary.jpg','0'),
                ('film','Terror','Insidious','2010','films/Insidious.jpg','0'),
                ('film','Terror','Un Lugar Tranquilo','2018','films/Un_Lugar_Tranquilo.jpg','0'),
                ('film','Romance','Titanic','1997','films/Titanic.jpg','0'),
                ('film','Romance','Orgullo y Prejuicio','2005','films/Orgullo_y_Prejuicio.jpg','0'),
                ('film','Romance','La La Land','2016','films/La_La_Land.jpg','0'),
                ('film','Romance','El Diario de una Pasión','2004','films/El_Diario_de_una_Pasion.jpg','0'),
                ('film','Romance','Romeo + Julieta','1996','films/Romeo_Julieta.jpg','0'),
                ('film','Romance','Amelie','2001','films/Amelie.jpg','0'),
                ('film','Romance','Un Lugar en el Tiempo','1980','films/Un_Lugar_en_el_Tiempo.jpg','0'),
                ('film','Romance','El Guardaespaldas','1992','films/El_Guardaespaldas.jpg','0'),
                ('film','Aventura','Jurassic Park','1993','films/Jurassic_Park.jpg','0'),
                ('film','Aventura','Indiana Jones: En busca del arca perdida','1981','films/Indiana_Jones_En_busca_del_arca_perdida.jpg','0'),
                ('film','Aventura','Piratas del Caribe: La maldición del Perla Negra','2003','films/Piratas_del_Caribe_La_maldicion_del_Perla_Negra.jpg','0'),
                ('film','Aventura','Avatar','2009','films/Avatar.jpg','0'),
                ('film','Aventura','La Isla del Tesoro','1950','films/La_Isla_del_Tesoro.jpg','0'),
                ('film','Aventura','El Libro de la Selva','2016','films/El_Libro_de_la_Selva.jpg','0'),
                ('film','Aventura','Up','2009','films/Up.jpg','0'),
                ('film','Aventura','La Odisea','1997','films/La_Odisea.jpg','0'),
                ('film','Thriller','El Silencio de los Corderos','1991','films/El_Silencio_de_los_Corderos.jpg','0'),
                ('film','Thriller','Seven','1995','films/Seven.jpg','0'),
                ('film','Thriller','Gone Girl','2014','films/Gone_Girl.jpg','0'),
                ('film','Thriller','Shutter Island','2010','films/Shutter_Island.jpg','0'),
                ('film','Thriller','El Maquinista','2004','films/El_Maquinista.jpg','0'),
                ('film','Thriller','El Cisne Negro','2010','films/El_Cisne_Negro.jpg','0'),
                ('film','Thriller','Prisioneros','2013','films/Prisioneros.jpg','0'),
                ('serie','Acción','24','2001','series/24.jpg','0'),
                ('serie','Acción','Arrow','2012','series/Arrow.jpg','0'),
                ('serie','Acción','The Punisher','2017','series/The_Punisher.jpg','0'),
                ('serie','Acción','Cobra Kai','2018','series/Cobra_Kai.jpg','0'),
                ('serie','Comedia','Friends','1994','series/Friends.jpg','0'),
                ('serie','Comedia','Brooklyn Nine-Nine','2013','series/Brooklyn_Nine-Nine.jpg','0'),
                ('serie','Comedia','The Office','2005','series/The_Office.jpg','0'),
                ('serie','Comedia','Parks and Recreation','2009','series/Parks_and_Recreation.jpg','0'),
                ('serie','Drama','Breaking Bad','2008','series/Breaking_Bad.jpg','0'),
                ('serie','Drama','Los Soprano','1999','series/Los_Soprano.jpg','0'),
                ('serie','Drama','The Crown','2016','series/The_Crown.jpg','0'),
                ('serie','Drama','This Is Us','2016','series/This_Is_Us.jpg','0'),
                ('serie','Fantasía','Game of Thrones','2011','series/Game_of_Thrones.jpg','0'),
                ('serie','Fantasía','The Witcher','2019','series/The_Witcher.jpg','0'),
                ('serie','Fantasía','His Dark Materials','2019','series/His_Dark_Materials.jpg','0'),
                ('serie','Fantasía','Merlín','2008','series/Merlin.jpg','0'),
                ('serie','Terror','Stranger Things','2016','series/Stranger_Things.jpg','0'),
                ('serie','Terror','The Haunting of Hill House','2018','series/The_Haunting_of_Hill_House.jpg','0'),
                ('serie','Terror','American Horror Story','2011','series/American_Horror_Story.jpg','0'),
                ('serie','Terror','Penny Dreadful','2014','series/Penny_Dreadful.jpg','0'),
                ('serie','Romance','Outlander','2014','series/Outlander.jpg','0'),
                ('serie','Romance','Bridgerton','2020','series/Bridgerton.jpg','0'),
                ('serie','Romance','Jane the Virgin','2014','series/Jane_the_Virgin.jpg','0'),
                ('serie','Romance','Poldark','2015','series/Poldark.jpg','0'),
                ('serie','Aventura','The Mandalorian','2019','series/The_Mandalorian.jpg','0'),
                ('serie','Aventura','The Walking Dead','2010','series/The_Walking_Dead.jpg','0'),
                ('serie','Aventura','Lost','2004','series/Lost.jpg','0'),
                ('serie','Aventura','Vikings','2013','series/Vikings.jpg','0'),
                ('serie','Thriller','Mindhunter','2017','series/Mindhunter.jpg','0'),
                ('serie','Thriller','Sherlock','2010','series/Sherlock.jpg','0'),
                ('serie','Thriller','True Detective','2014','series/True_Detective.jpg','0'),
                ('serie','Thriller','Dexter','2006','series/Dexter.jpg','0'),
                ('film','Thriller','No es país para viejos','2007','films/No_es_pais_para_viejos.jpg','0'),
                ('film','Acción','Rambo','1982','films/Rambo.jpg','0'),
                ('film','Acción','El Exorcista','1973','films/El_Exorcista.jpg','0')          
            ]
        )  
        self.connection.commit()


    def create_table_users_contents(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users_contents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content_id INTEGER,
            foreign key (user_id) references users(id) ON UPDATE CASCADE ON DELETE CASCADE,
            foreign key (content_id) references contents(id) ON UPDATE CASCADE ON DELETE CASCADE
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
    
