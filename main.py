from flask import Flask, render_template, request, flash, session, redirect, url_for
from utils.utils import *
from data.sqliteClient import SqliteClient
from data.sqliteUsers import SqliteUsers
from data.sqliteContents import SqliteContents
database=SqliteClient()
sqlite_users=SqliteUsers(database)
sqlite_contents=SqliteContents(database)
app = Flask(__name__)


@app.before_request
def before_request_func():
    database.connect()

@app.after_request
def after_request_func(response):
    database.close()
    return response

@app.route("/")
def home():
    films=sqlite_contents.get_all_films_order_by_clicks()
    series=sqlite_contents.get_all_series_order_by_clicks()
    return render_template("home.html", films=films, series=series)
@app.route("/films")
def films():
    films=sqlite_contents.get_all_films()
    return render_template("films/showAll.html", films=films)
@app.route("/series")
def series():
    series=sqlite_contents.get_all_series()
    return render_template("series/showAll.html", series=series)
@app.route("/contact")
def contact():
    return render_template("contact.html")








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
    name = request.form.get("name")
    clave = request.form.get("clave")
    name=name.lower()
    if check_empty(name) or check_empty(clave):
        flash("No puede haber campos vacios")
        return redirect(url_for("form_login"))
    lista_tuplas=sqlite_users.get_user_by_field("name", name)
    if (len(lista_tuplas)==0):
        print("El usuario no existe")
        flash("El usuario no existe")
        return redirect(url_for("form_login"))
    usuario=lista_tuplas[0]
    print (usuario)
    print("la clave es", clave)
    print("alacenada: ",usuario[2])
    if clave != usuario[2]:
        print("La clave no es correcta")
        flash("La clave es incorrecta ")
        return redirect(url_for("form_login"))
    else:
        print("La clave es correcta ", name)
        session["name"] = name
        session["rol"] = usuario[4]
        print("rol", usuario[4])
        if usuario[4] == "administrador":
            return redirect(url_for("menu_admin"))
        elif usuario[4] == "normal":
            return redirect(url_for("menu_usuario"))
        else:
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



# es posible arranca la aplicación esccribiendo en el terminal flask --app main run y comentando las 2 siguiente sentencias
if __name__=="__main__":
    app.run(debug=True)
