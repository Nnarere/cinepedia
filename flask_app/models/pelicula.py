from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

from datetime import datetime

from flask_app.models.comentarios import Comentario

class Pelicula:
    def __init__(self, data): 
        self.id = data["id"]
        self.nombre_pelicula = data["nombre_pelicula"]
        self.director = data["director"]
        self.fecha_estreno = data["fecha_estreno"]
        self.sinopsis = data["sinopsis"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuario_id = data["usuario_id"]

        self.user_name = data["user_name"] #agrego esto para colocar el nombre de quien publico el pelicula al realizar una consulta JOIN
        self.comentarios = []

    @classmethod
    def create(cls, form): 
        query = "insert into peliculas (nombre_pelicula, director, fecha_estreno, sinopsis, usuario_id) values (%(nombre_pelicula)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s)"
        return connectToMySQL("cinepedia").query_db(query, form)
    
    @classmethod
    def read_one(cls, data):
        query = "select peliculas.*, usuarios.nombre as user_name from peliculas join usuarios on peliculas.usuario_id = usuarios.id where peliculas.id = %(id)s"
        result = connectToMySQL("cinepedia").query_db(query, data)
        pelicula = cls(result[0])
        print(pelicula)
        return pelicula 
    

    @classmethod
    def read_all(cls):
        query = "select peliculas.*, usuarios.nombre as user_name from peliculas join usuarios on peliculas.usuario_id = usuarios.id ORDER BY fecha_estreno ASC"
        results = connectToMySQL("cinepedia").query_db(query) 
        peliculas = [] 
        for peli in results:
            pelicula = cls(peli)
            query_comments = "SELECT comentarios.*, usuarios.nombre as user_name FROM comentarios JOIN usuarios ON comentarios.usuario_id = usuarios.id WHERE pelicula_id = %(pelicula_id)s"
            data_comment = {"pelicula_id": peli["id"]}
            results_comentarios = connectToMySQL("cinepedia").query_db(query_comments, data_comment)
            comentarios = [] 
            for c in results_comentarios:
                comentarios.append(Comentario(c)) 
            pelicula.comentarios = comentarios
            peliculas.append(pelicula)
        return peliculas
    

    @staticmethod
    def validate_peli(form, ignore = False): 
        is_valid = True

        if len(form["nombre_pelicula"]) < 3:
            flash("El nombre de la pelicula debe tener al menos 3 caracteres", "pelicula")
            is_valid = False
        
        if len(form["director"]) < 3:
            flash("El nombre del director debe tener al menos 3 caracteres", "pelicula")
            is_valid = False

        if len(form["sinopsis"]) < 3:
            flash("Los detalles del pelicula debe tener al menos 3 caracteres", "pelicula")
            is_valid = False

        if form["fecha_estreno"] == "": #si del formulario date es igual igual a vacio
            flash("Ingrese una fecha", "pelicula")
            is_valid = False

        query = "select * from peliculas where nombre_pelicula = %(nombre_pelicula)s"
        result = connectToMySQL("cinepedia").query_db(query, form)

        if ignore:
            return is_valid

        if len(result) >=1:
            flash("El pelicula ya existe", "pelicula")
            is_valid = False
              


                     
 
        return is_valid
    
    @classmethod
    def updated(cls, form):
        query = "UPDATE peliculas SET nombre_pelicula = %(nombre_pelicula)s, director = %(director)s, fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s WHERE id = %(id)s"
        return connectToMySQL("cinepedia").query_db(query, form)

    @classmethod
    def delete(cls, data):
        query = "delete from peliculas where id = %(id)s"
        return connectToMySQL("cinepedia").query_db(query, data)