from flask import Flask, render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.user import Usuario
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentarios import Comentario

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/register", methods=["POST"])
def register():
    #validamos la info
    if not Usuario.validate_user(request.form):
        return redirect("/")
    
    #encriptar contraseña
    pass_hash = bcrypt.generate_password_hash(request.form["contrasena"])

    #creamos un diccionario con toda la info que recibidos del form, pero el passworrd llega haseado con el codigo de arriba
    form = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"], 
        "email": request.form["email"], 
        "contrasena": pass_hash
    }

    id = Usuario.save(form) #recibe el id del nuevo usario
    session["usuario_id"] = id #guardamos en sesion el id del usuario
    return redirect("/dice")

@app.route("/login", methods=["POST"])
def login():
    user = Usuario.get_by_email(request.form) 

    if not user: #
        flash("E-mail no encontrado", "login")
        return redirect ("/") 
    
    if not bcrypt.check_password_hash(user.contrasena, request.form["contrasena"]):
        flash("Contraseña incorrecta", "login")
        return redirect ("/")

    session["usuario_id"] = user.id
    return redirect("/cine") 

@app.route("/cine")
def dashboard():
    if "usuario_id" not in session:
        return redirect("/")
    
    dicc = {"id": session["usuario_id"]}
    usuario = Usuario.get_by_id(dicc) 
    peli = Pelicula.read_all()
    return render_template("dashboard.html", usuario = usuario, peli = peli)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")