from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

class Comentario:
    def __init__(self, data):
        #data = {diccionario con la info de mi BD}
        self.id = data["id"]
        self.comentario = data["comentario"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuario_id = data["usuario_id"]
        self.pelicula_id = data["pelicula_id"]

        self.user_name = data["user_name"] #lo sacamos del alia que declaramos en un join

    @classmethod
    def save(cls, form):
        query = "INSERT INTO comentarios (comentario, usuario_id, pelicula_id) VALUES (%(comentario)s, %(usuario_id)s, %(pelicula_id)s)"
        return connectToMySQL("cinepedia").query_db(query, form)
    
    @staticmethod
    def validate_comment(form):
        is_valid = True

        if len(form["comentario"]) < 3:
            flash("Escriba al menos 3 caracteres", "comentarios")
            is_valid = False
        return is_valid
    
        #Metodo para obtener los comentarios de un Post
    @classmethod
    def get_by_post_id(cls, pelicula_id):
        query = """
                SELECT usuarios.nombre, comentarios.created_at, comentarios.comentario
                FROM comentarios
                JOIN usuarios ON comentarios.usuario_id = usuario.id
                WHERE comentarios.pelicula_id = %(pelicula_id)s
                ORDER BY created_at DESC
                """
        results = connectToMySQL("cinepedia").query_db(query, (pelicula_id))
        return results
  