from flask import Flask, render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.user import Usuario
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentarios import Comentario


@app.route("/nuevo/cine")
def nuevo():
    if "usuario_id" not in session:
        return redirect("/")
    
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    if "usuario_id" not in session:
        return redirect("/")

    session["sinopsis"] = request.form["sinopsis"]


    if not Pelicula.validate_peli(request.form):
        return redirect("/nuevo/cine")
  
    Pelicula.create(request.form)
    session.pop("sinopsis") 
    return redirect("/cine")

@app.route("/ver/<int:id>")
def read(id): #si en la url estoy recibiendo info, debo ponerlo en el metodo.
    if "usuario_id" not in session:
        return redirect ("/")
    dicc = {"id" : id}
    peli = Pelicula.read_one(dicc)
    return render_template("view.html", peli = peli)

@app.route("/borrar/<int:id>") #/borrar/2
def delete(id):
    if "usuario_id" not in session:
        return redirect("/")
    dicc = {"id": id} 
    Pelicula.delete(dicc)
    return redirect("/cine")

@app.route("/editar/<int:id>")
def edit(id):
    if "usuario_id" not in session:
        return redirect("/")

    dicc = {"id": id}
    peli = Pelicula.read_one(dicc)

    if session["usuario_id"] != peli.usuario_id:
        return redirect("/cine")
    
    
    return render_template("edit.html", peli = peli)

@app.route("/update", methods=['POST'])
def update():
    if "usuario_id" not in session:
        return redirect("/")
        
    if not Pelicula.validate_peli(request.form, ignore = True):
        return redirect("/edit/"+request.form["id"])

    #recibir request.form que es un diccionario con la informacion del formulario
    Pelicula.updated(request.form)
    return redirect("/cine")