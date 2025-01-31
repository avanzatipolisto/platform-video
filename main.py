from flask import Flask, render_template, request, make_response, redirect, url_for, flash, session,jsonify
from utils.utils import *
from data.sqliteClient import SqliteClient
from data.sqliteUsers import SqliteUsers
from data.sqliteContents import SqliteContents
from data.sqliteUsersContents import SqliteUsersContents
from math import floor
from utils.file_manager import *
# https://github.com/flasgger/flasgger
from flasgger import Swagger

#Utilizamos el os en el delete content
import os
database=SqliteClient()
sqlite_users=SqliteUsers(database)
sqlite_contents=SqliteContents(database)
sqlite_users_contents=SqliteUsersContents(database)
app = Flask(__name__)
#Documentación
swagger = Swagger(app)
app.secret_key="My secret Key"
FILMS_IMAGES_FOLDER = "static/films"
app.config["FILMS_IMAGES_FOLDER"] = FILMS_IMAGES_FOLDER
SERIES_IMAGES_FOLDER = "static/series"
app.config["SERIES_IMAGES_FOLDER"] = SERIES_IMAGES_FOLDER



@app.before_request
def before_request_func():
    database.connect()

@app.after_request
def after_request_func(response):
    database.close()
    return response

@app.route("/")
@app.route("/<page_films>/<page_series>")
def home(page_films=0, page_series=0):
    """
    Ver las peículas y series con más clicks
    ---    
    parameters:
      - name: page_films
        in: path
        type: string
        default: 0
      - name: page_series
        in: path
        type: string
        default: 0
    responses:
      200:
        description: home.html
    """

    page_films=int(page_films)
    page_series=int(page_series)
    films=sqlite_contents.get_all_films_order_by_clicks(page_films*4)
    series=sqlite_contents.get_all_series_order_by_clicks(page_series*4)
    return render_template("home.html", films=films, series=series, page_films=page_films, page_series=page_series)

@app.route("/show/<id>")
def show(id):
    """
    Ver ficha de una película o serie
    ---    
    parameters:
      - name: id
        in: path
        type: string
        required: true
        default: 0

    responses:
      200:
        description: show.html
    """
    contents=sqlite_contents.get_content_by_field("id", id)
    content=contents[0]
    return render_template("show.html", content=content)

@app.route("/show_content", methods = ["POST", "GET"])
def show_user_content():
    """
    Ver ficha de una película o serie a través del método POST o GET
    ---    
    parameters:
      - name: id
        in: formData
        type: integer
        required: true


    responses:
        200:
            description: show.html
        405:
            description: Invalid input
    """
    if request.method=="GET":
        id=request.args.get("id")
    elif request.method=="POST":
        id=request.form.get("id")
    contents=sqlite_contents.get_content_by_field("id", id)
    content=contents[0]
    return render_template("show.html", content=content)


@app.route("/films")
@app.route("/films/<page>")
@app.route("/films/<letter>/<page>")
def films(letter=None,page=None):
    """
    Ver películas paginadas por letra 
    ---    
    parameters:
      - name: letter
        in: path
        type: integer
      - name: page
        in: path
        type: integer


    responses:
        200:
            description: films.html
        405:
            description: Invalid input
    """
    if page==None:
        page=0
    else:
        page=int(page)
    
    if (letter!=None):
        total_pages=sqlite_contents.get_count_films_by_letter(letter)
        last_page=floor(total_pages/14)
        films=sqlite_contents.get_all_films_by_letter(letter, page*14)
    else:
        total_pages=sqlite_contents.get_count_films()
        last_page=floor(total_pages/14)
        films=sqlite_contents.get_all_films(page*14)
    return render_template("films.html", films=films, page=page, last_page=last_page, letter=letter)




@app.route("/series")
@app.route("/series/<page>")
@app.route("/series/<letter>/<page>")
def series(letter=None,page=None):
    """
    Ver series paginadas por letra 
    ---    
    parameters:
      - name: letter
        in: path
        type: integer

      - name: page
        in: path
        type: integer

    responses:
        200:
            description: series.html
        405:
            description: Invalid input
    """
    if page==None:
        page=0
    else:
        page=int(page)
    print("page ", page, " letter: ", letter)
    if (letter!=None):
        total_pages=sqlite_contents.get_count_series_by_letter(letter)
        last_page=floor(total_pages/14)
        series=sqlite_contents.get_all_series_by_letter(letter, page*14)
    else:
        total_pages=sqlite_contents.get_count_series()
        last_page=floor(total_pages/14)
        series=sqlite_contents.get_all_series(page*14)
    return render_template("series.html", series=series, page=page, last_page=last_page, letter=letter)





@app.route("/contact")
def contact():
    """
    Ver información de contacto
    ---    
    
    responses:
        200:
            description: films.html
        405:
            description: Invalid input
    """
    return render_template("contact.html")

@app.route("/search", methods = ["POST"])
def search():
    """
    Muestra una lista de películas que coincidan con la búsqueda
    ---    
    parameters:
      - name: title
        in: formData
        type: integer
        required: true

    responses:
        200:
            description: search.html
        405:
            description: Invalid input
    """
    if request.method == "POST":
        text_search = request.form.get("search")
        if check_empty(text_search):
            flash("No puede haber campos vacios")
            return redirect(url_for("home"))
        else:
            films=sqlite_contents.get_all_films_by_title_like(text_search)
            series=sqlite_contents.get_all_series_by_title_like(text_search)
            print("obtenidos ", len(films))
            return render_template("search.html", films=films, series=series)
    else:
        flash("La búsqueda es incorrecta ")
        return redirect(url_for("home"))















#####################################################################
#####################################################################
#####################################################################
#                          Rutas auth
#####################################################################
#####################################################################
#####################################################################
@app.route("/form_login")
def form_login():
    """
    Muestra un formaulario de login
    ---    
    
    responses:
        200:
            description: form_login.html
        405:
            description: Invalid input
    """
    return render_template("auth/form_login.html")

@app.route("/login", methods = ["POST"])
def login():
    """
    Contiene la logica de login
    ---

    parameters:
      - name: name_user
        in: formData
        type: string
        required: true

      - name: password
        in: formData
        type: string
        required: true
    responses:
        200:
            description: home.html
        405:
            description: Invalid input
    """
    if request.method != "POST":
        flash("Not allowed")
        return redirect(url_for("form_login"))
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        name=name.lower()
        if check_empty(name) or check_empty(password):
            flash("No puede haber campos vacios")
            return redirect(url_for("form_login"))
        lista_tuplas=sqlite_users.get_user_by_field("name", name)
        if (len(lista_tuplas)==0):
            flash("El usuario no existe")
            return redirect(url_for("form_login"))
        user=lista_tuplas[0]
        if password != user[2]:
            flash("La password es incorrecta ")
            return redirect(url_for("form_login"))
        else:
            session["id"] = user[0]
            session["name"] = name
            session["rol"] = user[5]
            print("autenticado como ", user[5], session["rol"])
            return redirect("/")

@app.route("/form_register")
def form_register():
    """
    Contiene la logica de logout para registrar un nuevo usuario
    """
    return render_template("auth/form_register.html")

@app.route("/register", methods = ["POST"])
def register():
    """
    Contiene la logica de logout para registrar un nuevo usuario
    """
    name = request.form.get("name")
    name=name.lower()
    password = request.form.get("password")
    password_repeat = request.form.get("password_repeat")

    lista_tuplas=sqlite_users.get_user_by_field("name", name)
    if (len(lista_tuplas)>0):
        flash("El usuario ya existe")
        return redirect(url_for("form_register"))

    if check_empty(name) or check_empty(password) :
        flash("No puede haber campos vacios")
        return redirect(url_for("form_register"))

    if len(password)<4: 
        flash("Las clave tiene que ser mayor de 3 caracteres")
        return redirect(url_for("form_register"))

    if password != password_repeat:
        flash("Las claves no son iguales")
        return redirect(url_for("form_register"))
    sqlite_users.add_user(name,  password)
    
    flash("Usuario registrado con exito")
    return redirect(url_for("form_login"))
    
@app.route("/logout")
def form_logout():
    """
    Contiene la logica de logout para cerrar la sesión
    """
    # Clear the session
    session.clear()
    return redirect("/")

@app.route("/menu_admin")
def menu_admin():
    return render_template("admin/menu_.html")















#####################################################################
#####################################################################
#####################################################################
#                          Rutas admin
#####################################################################
#####################################################################
#####################################################################

@app.route("/admin/settings/form_reset")
def admin_form_settings():
    return render_template("admin/settings.html")
@app.route("/admin/csv_create_backup")
def adm_csv_crear_backup():
    if 'nombre' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    users=sqlite_users.get_all_users_without_page()
    contents=sqlite_contents.get_all_contents_without_page()
    users_contents=sqlite_users_contents.get_all_users_contents_without_page()

    write_csv_file(users, contents, users_contents)
    flash("File created successfully")
    return redirect(url_for("admin_form_settings"))

@app.route("/admin/csv_restore_backup", methods=["POST"])
def adm_csv_leer():
    if 'nombre' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    file=request.files["file_csv"] 
    file_name=file.filename
    file.save(file_name) 
    if (file_name.split(".")[-1] != "csv"):
        flash("The file must be of type csv")
        return redirect(url_for("admin_form_settings"))
    if (file==None):
        flash("LEl archivo no puede estar vacío")
        return redirect(url_for("admin_form_settings"))
    #obtenemos un diccionario con los usuarios, deportes, deportes_usuarios y días_prohibidos
    datos=restore_csv_backup(file_name)    
    users=datos["users"]
    if(len(users)!=0):
        sqlite_users.delete_all_users()
        for user in users:
            sqlite_users.add_user(user[1],user[2],user[3],user[4],user[5])
    contents=datos["contents"]
    if (len(contents)!=0):
        sqlite_contents.delete_all_contents()
    for content in contents:
        sqlite_contents.add_content(content[1],content[2],content[3],content[4],content[5],content[6])
    users_contents=datos["users_contents"]
    if( users_contents!=0):
        sqlite_users_contents.delete_all_users_contents()
        for user_content in users_contents:
            sqlite_users_contents.add_user_content(user_content[1],user_content[2])
    
    flash("File csv read successfully")
    return redirect(url_for("admin_form_settings"))

@app.route("/admin/settings/reset")
def admin_reset_all():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")

    
    delete_folder(app.config["FILMS_IMAGES_FOLDER"])
    delete_folder(app.config["SERIES_IMAGES_FOLDER"])
    copy_assets("assets", "static")
    database.get_connect().close()
    delete_file("database.db")
    return redirect(url_for("home")) 

 
#                          USERS
#####################################################################    
@app.route("/admin/users/showAll")
@app.route("/admin/users/showAll/<page>")
def show_all_user_admin(page=0):
    """
    Muestra todos los usuarios paginados
    ---    
    parameters:
      - name: page
        in: path
        type: integer
        required: false


    responses:
        200:
            description: admin/users/showAll.html
        405:
            description: Invalid input
    """
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    page=int(page)
    users=sqlite_users.get_all_users(page*10)
    total_pages=sqlite_users.get_count_users()
    last_page=floor(total_pages/10)
    return render_template("admin/users/showAll.html",users=users, page=page, last_page=last_page)

@app.route("/admin/users/form_create")
def admin_form_create_user():
    """
    Muestra el formulario para crear un usuario
    ---    


    responses:
        200:
            description: admin/users/form_create.html
        405:
            description: Invalid input
    """
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    return render_template("admin/users/form_create.html")

@app.route("/admin/users/create", methods=["POST"])
def admin_create_user():
    """
    crea un usuario
    ---    
    parameters:
      - name: name
        in: formData
        type: string
        required: true

      - name: email
        in: formData
        type: string
        required: true

      - name: password
        in: formData
        type: string
        required: true

      - name: password_repeat
        in: formData
        type: string
        required: true

      - name: birddate
        in: formData
        type: string
        required: true

      - name: rol
        in: formData
        type: string
        required: true

    responses:
        200:
            description: /admin/users/showAll
        405:
            description: Invalid input
    """
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    if request.method!="POST":
        return redirect("/form_login")
    else:
        #Obtenemos los datos
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")
        birddate = request.form.get("birddate")
        rol=request.form.get("rol")
        #validaciones
        if password != password_repeat:
            flash("Passwords are not the same")
            return redirect(url_for("admin_form_create_user"))
        if check_empty(name) or check_empty(password):
            flash("There can be no empty fields")
            return redirect(url_for("admin_form_create_user"))
        sqlite_users.add_user(name,password, email, birddate, rol)
        return redirect(url_for("show_all_user_admin"))

@app.route("/admin/users/form_update", methods=["POST", "GET"])
def admin_form_update_user():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    if (request.method == "GET"):
        id= request.args.get("id")
    elif (request.method == "POST"):
        id =request.form.get("id")
    print("El id es ",id)

    users=sqlite_users.get_user_by_field("id",id)
    user=users[0]
    return render_template("admin/users/form_update.html",user=user)

@app.route("/admin/users/update", methods=["POST"])
def admin_update_user():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")

    if request.method!="POST":
        return redirect("/form_login")
    else:
        #Obtenemos los datos
        id = request.form.get("id")
        name = request.form.get("name")
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")
        email = request.form.get("email")
        birddate = request.form.get("birddate")
        rol = request.form.get("rol")
        #validaciones
        if password != password_repeat:
            flash("Passwords are not the same")
            users=sqlite_users.get_user_by_field("id",id)
            user=users[0]
            return render_template("admin/users/form_update.html",user=user)
        if check_empty(name) or check_empty(password):
            flash("There can be no empty fields")
            users=sqlite_users.get_user_by_field("id",id)
            user=users[0]
            return render_template("admin/users/form_update.html",user=user)

        sqlite_users.update_user(id,name,password, email, birddate, rol)
        return redirect(url_for("show_all_user_admin"))

@app.route("/admin/users/delete", methods=["post"])
def admin_delete_user():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    id= request.form.get("id")
    print("El id a borrar es ",id)
    sqlite_users.delete_user(id)
    
    return redirect("/admin/users/showAll")

#                          Contents
#####################################################################    
@app.route("/admin/contents/showAll")
@app.route("/admin/contents/showAll/<page>")
def show_all_contents_admin(page=0):
    page=int(page)
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")

    contents=sqlite_contents.get_all_contents(page*10)
    total_pages=sqlite_contents.get_count_contents()
    last_page=floor(total_pages/10)
    return render_template("admin/contents/showAll.html",contents=contents, page=page, last_page=last_page)

@app.route("/admin/contents/form_create")
def admin_form_create_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    return render_template("admin/contents/form_create.html")

@app.route("/admin/contents/create", methods=["POST"])
def admin_create_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    if request.method!="POST":
        return redirect("/form_login")
    else:
        #Obtenemos los datos
        type = request.form.get("type")
        genre = request.form.get("genre")
        title = request.form.get("title")
        year = request.form.get("year")
        clicks=0
        image=request.files["image"] 
        file_name=image.filename
        extension=file_name.split(".")[-1]
        
        #validaciones
        if (extension != "png") and (extension != "jpg") and (extension != "jpeg"):
            flash("The file must be of type png, jpg or jpeg")
            return redirect(url_for("admin_form_create_content"))
        if (image==None):
            flash("The file cannot be empty")
            return redirect(url_for("admin_form_create_content"))
        if check_empty(type) or check_empty(genre) or check_empty(title) or check_empty(year):
            flash("There can be no empty fields")
            return redirect(url_for("admin_form_create_content"))
        # Comprobamos si ya existe ese título en la base de datos
        contents=sqlite_contents.get_content_by_field("title", title)
        if (len(contents)>0):
                flash("The content already exists")
                return redirect(url_for("admin_form_create_content"))
        if (type=="film"):
            image.save("static/films/"+file_name) 
            sqlite_contents.add_content(type,genre,title,year,"films/"+title+"."+extension,clicks)
        else:
            image.save("static/series/"+file_name)
            sqlite_contents.add_content(type,genre,title,year,"series/"+title+"."+extension,clicks)
        return redirect(url_for("show_all_contents_admin"))

@app.route("/admin/contents/form_update", methods=["POST", "GET"])
def admin_form_update_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    #if (request.method == "GET"):
    #    id= request.args.get("id")
    if (request.method == "POST"):
        id =request.form.get("id")
    print("El id es ",id)
    contents=sqlite_contents.get_content_by_field("id",id)
    content=contents[0]
    print ("El contenido es ", content)
    return render_template("admin/contents/form_update.html",content=content)

@app.route("/admin/contents/update", methods=["POST"])
def admin_update_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")

    if request.method!="POST":
        return redirect("/form_login")
    else:
        #Obtenemos los datos
        id = request.form.get("id")
        type = request.form.get("type")
        genre = request.form.get("genre")
        title = request.form.get("title")
        year = request.form.get("year")
        clicks = request.form.get("clicks")
        image=request.files["image"] 
        print("la lista de imagenes es ",image)
        path_image=request.form.get("path_image")
        #validaciones
        #Si la imiagen no es nula es que has pichado en el input file y has elegido una imagen
        if image.filename != "": 
            file_name=image.filename
            extension=file_name.split(".")[-1]
            if ( extension!= "png") and (extension != "jpg") and (extension != "jpeg"):
                flash("El archivo debe ser de tipo png, jpg o jpeg")
                return redirect(url_for("admin_form_create_content"))        
            if(type=="film"):
                image.save("static/films/"+title+"."+extension) 
                path_image="films/"+title+"."+extension
            elif(type=="serie"):
                image.save("static/series/"+title+"."+extension) 
                path_image="series/"+title+"."+extension
        
        if check_empty(type) or check_empty(genre) or check_empty(title) or check_empty(year):
            flash("There can be no empty fields")
            contents=sqlite_contents.get_content_by_field("id",id)
            content=contents[0]
            return render_template("admin/contents/form_update.html",content=content)
       
        sqlite_contents.update_content(id,type,genre,title,year,path_image,clicks)
        return redirect(url_for("show_all_contents_admin"))

@app.route("/admin/contents/delete", methods=["post"])
def admin_delete_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    id= request.form.get("id")
    #borramos la imagen
    content=sqlite_contents.get_content_by_field("id",id)
    content=content[0]
    if os.path.exists("static/"+content[3]):
        os.remove("static/"+content[3])
    print ("vamos a borrar a ", id)
    sqlite_contents.delete_content(id)
    flash("record deleted")
    return redirect("/admin/contents/showAll")


#                         Users Contents
#####################################################################    
@app.route("/admin/users_contents/showAll")
@app.route("/admin/users_contents/showAll/<page>")
def show_all_users_contents_admin(page=0):
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    page=int(page)
    users_contents=sqlite_users_contents.get_all_users_contents(page*10)
    total_pages=sqlite_users_contents.get_count_users_contents()
    last_page=floor(total_pages/10)
    return render_template("admin/users_contents/showAll.html",users_contents=users_contents, sqlite_users=sqlite_users, sqlite_contents=sqlite_contents, page=page, last_page=last_page)

@app.route("/admin/users_contents/form_create")
def admin_form_create_user_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    # Le pasamos a la vista los usuarios y los contenidos
    users=sqlite_users.get_all_users_without_page()
    contents=sqlite_contents.get_all_contents_without_page()
    return render_template("admin/users_contents/form_create.html", users=users, contents=contents)



@app.route("/admin/users_contents/create", methods=["POST"])
def admin_create_user_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    if request.method!="POST":
        return redirect("/form_login")
    else:
        #Obtenemos los datos
        user_id = request.form.get("user_id")
        content_id = request.form.get("content_id")
       
        #validaciones
        if not user_id or not content_id:
            flash("There can be no empty fields")
            return redirect(url_for("admin_form_create_user_content"))
        sqlite_users_contents.add_user_content(user_id, content_id)
        return redirect(url_for("show_all_users_contents_admin"))
    
@app.route("/admin/users_contents/form_update", methods=["POST", "GET"])
def admin_form_update_user_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    if (request.method == "POST"):
        id =request.form.get("id")
    users_contents=sqlite_users_contents.get_user_content_by_field("id",id)
    user_content=users_contents[0]
    users=sqlite_users.get_all_users_without_page()
    contents=sqlite_contents.get_all_contents_without_page()
    return render_template("admin/users_contents/form_update.html",user_content=user_content, users=users, contents=contents, sqlite_users=sqlite_users, sqlite_contents=sqlite_contents)

@app.route("/admin/users_contents/update", methods=["POST"])
def admin_update_user_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")

    if request.method!="POST":
        return redirect("/form_login")
  
    #Obtenemos los datos
    id = request.form.get("id")
    user_id = request.form.get("user_id")
    content_id = request.form.get("content_id")
    if user_id==None or content_id==None:
        flash("There can be no empty fields")
        return redirect(url_for("show_all_users_contents_admin"))
    sqlite_users_contents.update_user_content(id,user_id,content_id)
    return redirect(url_for("show_all_users_contents_admin"))

@app.route("/admin/users_contents/delete", methods=["POST"])
def admin_delete_user_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/form_login")
    id= request.form.get("id")
    print("El id a borrar es ",id)
    sqlite_users_contents.delete_user_content(id)
    flash("record deleted")
    return redirect("/admin/users_contents/showAll")



















#####################################################################
#####################################################################
#####################################################################
#                          Rutas user
#####################################################################
#####################################################################
#####################################################################
@app.route("/users/settings")
def show_settings_user():
    if 'name' not in session:
        flash("Log in as user")
        return redirect("/form_login")
    id=session["id"]
    users=sqlite_users.get_user_by_field("id", id)
    user=users[0]
    return render_template("users/settings.html", user=user)

@app.route("/users/settings_update", methods=["post"])
def user_settings_update():
    if 'name' not in session:
        flash("Log in as user")
        return redirect("/form_login")
    if request.method!="POST":
        return redirect("/form_login")
    else:
        id = request.form.get("id")
        name = request.form.get("name")
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")
        email = request.form.get("email")
        birddate = request.form.get("birddate")
        rol = request.form.get("rol")
        #validaciones
        if password != password_repeat:
            flash("Passwords are not the same")
            return redirect(url_for("show_settings_user"))
        if check_empty(name) or check_empty(password):
            flash("There can be no empty fields")
            return redirect(url_for("show_settings_user"))
        sqlite_users.update_user(id,name,password, email, birddate, rol)
        flash("update user")
        return redirect(url_for("show_settings_user"))
    
@app.route("/users/add_user_content/<content_id>")
def add_user_content(content_id):
    if 'name' not in session:
        flash("Log in as user")
        return redirect("/form_login")
    user_id=session["id"]   
    sqlite_users_contents.add_user_content(user_id,content_id )
    flash("Add to favorites")
    return redirect(url_for("show_user_content", id=content_id))

@app.route("/users/favorite_films")
def show_favorite_films_user():
    if 'name' not in session:
        flash("Log in as user")
        return redirect("/form_login")
    id=session["id"]
    films=sqlite_users_contents.get_user_favorite_films(id)
    return render_template("users/favorite_films.html", films=films)

@app.route("/users/favorite_series")
def show_favorite_series_user():
    if 'name' not in session:
        flash("Log in as user")
        return redirect("/form_login")
    id=session["id"]
    series=sqlite_users_contents.get_user_favorite_series(id)
    print("las series favoritas son ", series)
    print("El user id es ", id)
    return render_template("users/favorite_series.html", series=series)

@app.route("/users/favorite_films_delete", methods=["post"])
def favorite_film_delete():
    if 'name' not in session:
        flash("Log in as user")
        return redirect("/form_login")
    user_id=session["id"]
    content_id = request.form.get("content_id")
    sqlite_users_contents.delete_user_content_by_user_id_and_content_id(user_id, content_id)

    return redirect(url_for("show_favorite_films_user"))



# es posible arranca la aplicación esccribiendo en el terminal flask --app main run y comentando las 2 siguiente sentencias
if __name__=="__main__":
    #app.run(debug=True)
    #para render.com
    app.run(host="0.0.0.0", debug=False)
