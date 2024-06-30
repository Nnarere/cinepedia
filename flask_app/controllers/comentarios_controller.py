from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

from flask_app.models.user import Usuario
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentarios import Comentario

@app.route("/posts/<int:pelicula_id>/comments", methods=['POST'])
def create_comment(pelicula_id):
    if 'usuario_id' not in session:
        return redirect('/')

    if not Comentario.validate_comment(request.form):
        return redirect('/cine')

    data = {
        'comentario': request.form['comentario'],
        'pelicula_id': request.form['pelicula_id'], 
        'usuario_id': session['usuario_id']
    }

    Comentario.save(data)
    return redirect('/cine')
