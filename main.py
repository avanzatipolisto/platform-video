from flask import Flask, render_template, request, make_response, redirect, url_for, flash, session
from utils.utils import *
from data.sqliteClient import SqliteClient
from data.sqliteUsers import SqliteUsers
from data.sqliteContents import SqliteContents
from data.sqliteUsersContents import SqliteUsersContents
from math import floor
database=SqliteClient()
sqlite_users=SqliteUsers(database)
sqlite_contents=SqliteContents(database)
sqlite_users_contents=SqliteUsersContents(database)
app = Flask(__name__)
app.secret_key="My secret Key"

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
    page_films=int(page_films)
    page_series=int(page_series)
    films=sqlite_contents.get_all_films_order_by_clicks(page_films*4)
    series=sqlite_contents.get_all_series_order_by_clicks(page_series*4)
    return render_template("home.html", films=films, series=series, page_films=page_films, page_series=page_series)


@app.route("/show/<id>")
def show(id):
    content=sqlite_contents.get_content_by_field("id", id)
    return render_template("show.html", content=content)
@app.route("/show_content", methods = ["POST", "GET"])
def show_user_content():
    if request.method=="GET":
        id=request.args.get("id")
    elif request.method=="POST":
        id=request.form.get("id")
    content=sqlite_contents.get_content_by_field("id", id)
    return render_template("show.html", content=content)


@app.route("/films")
@app.route("/films/<page>")
@app.route("/films/<letter>/<page>")
def films(letter=None,page=None):
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
    return render_template("contact.html")

@app.route("/search", methods = ["POST"])
def search():
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
    """
    return render_template("auth/form_login.html")

@app.route("/login", methods = ["POST"])
def login():
    """
    Contiene la logica de login
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

#                          USERS
#####################################################################    
@app.route("/admin/users/showAll")
def show_all_user_admin():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
    users=sqlite_users.get_all_users()
    return render_template("admin/users/showAll.html",users=users)

@app.route("/admin/users/form_create")
def admin_form_create_user():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
    return render_template("admin/users/form_create.html")

@app.route("/admin/users/create", methods=["POST"])
def admin_create_user():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
    if request.method!="POST":
        return redirect("/login")
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
            return redirect("/login")
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
            return redirect("/login")

    if request.method!="POST":
        return redirect("/login")
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
            return redirect("/login")
    id= request.form.get("id")
    print("El id a borrar es ",id)
    sqlite_users.delete_user(id)
    
    return redirect("/admin/users/showAll")

#                          Contents
#####################################################################    
@app.route("/admin/contents/showAll")
def show_all_contents_admin():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
    contents=sqlite_contents.get_all_contents()
    return render_template("admin/contents/showAll.html",contents=contents)

@app.route("/admin/contents/form_create")
def admin_form_create_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
    return render_template("admin/contents/form_create.html")
@app.route("/admin/contents/delete", methods=["post"])
def admin_delete_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
    id= request.form.get("id")
    sqlite_users_contents.delete_user_content(id)
    flash("record deleted")
    return redirect("/admin/contents/showAll")


#                         Users Contents
#####################################################################    
@app.route("/admin/users_contents/showAll")
def show_all_users_contents_admin():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
    users_contents=sqlite_users_contents.get_all_users_contents()
    return render_template("admin/users_contents/showAll.html",users_contents=users_contents)

@app.route("/admin/users_contents/form_create")
def admin_form_create_user_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
    return render_template("admin/users_contents/form_create.html")
@app.route("/admin/users_contents/delete", methods=["post"])

def admin_delete_user_content():
    if 'name' not in session:
        if session["rol"] != "admin":
            return redirect("/login")
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
        if session["rol"] != "normal":
            flash("Log in as user")
            return redirect("/login")
    id=session["id"]
    users=sqlite_users.get_user_by_field("id", id)
    user=users[0]
    return render_template("users/settings.html", user=user)

@app.route("/users/settings_update", methods=["post"])
def user_settings_update():
    if 'name' not in session:
        if session["rol"] != "normal":
            flash("Log in as user")
            return redirect("/login")
    if request.method!="POST":
        return redirect("/login")
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
        if session["rol"] != "normal":
            flash("Log in as user")
            return redirect("/login")
    user_id=session["id"]   
    sqlite_users_contents.add_user_content(user_id,content_id )
    flash("Add to favorites")
    return redirect(url_for("show_user_content", id=content_id))

@app.route("/users/favorite_films")
def show_favorite_films_user():
    if 'name' not in session:
        if session["rol"] != "normal":
            flash("Log in as user")
            return redirect("/login")
    id=session["id"]
    films=sqlite_users_contents.get_user_favorite_films(id)
    return render_template("users/favorite_films.html", films=films)

@app.route("/users/favorite_series")
def show_favorite_series_user():
    if 'name' not in session:
        if session["rol"] != "normal":
            flash("Log in as user")
            return redirect("/login")
    id=session["id"]
    series=sqlite_users_contents.get_user_favorite_series(id)
    print("las series favoritas son ", series)
    print("El user id es ", id)
    return render_template("users/favorite_series.html", series=series)

@app.route("/users/favorite_films_delete", methods=["post"])
def favorite_film_delete():
    if 'name' not in session:
        if session["rol"] != "normal":
            flash("Log in as user")
            return redirect("/login")
    user_id=session["id"]
    content_id = request.form.get("content_id")
    sqlite_users_contents.delete_user_content_by_user_id_and_content_id(user_id, content_id)

    return redirect(url_for("show_favorite_films_user"))



# es posible arranca la aplicación esccribiendo en el terminal flask --app main run y comentando las 2 siguiente sentencias
if __name__=="__main__":
    #app.run(debug=True)
    #para render.com
    app.run(host="0.0.0.0", debug=True)
