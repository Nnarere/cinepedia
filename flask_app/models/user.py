from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Usuario:
    
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def save(cls, form):
        query = "insert into usuarios (nombre, apellido, email, contrasena) values (%(nombre)s, %(apellido)s, %(email)s, %(contrasena)s)"
        return connectToMySQL("cinepedia").query_db(query, form)
    
    @classmethod
    def get_by_email(cls, form):
        query = "select * from usuarios where email = %(email)s"
        result = connectToMySQL("cinepedia").query_db(query, form)

        if len(result) <1:
            return False
        else:
            user = cls(result[0])
            return user
        
    @staticmethod
    def validate_user(form):
        is_valid = True
        if len(form["nombre"])<2:
            flash("El nombre debe tener al menos dos caracteres", "registro") 
            is_valid = False
        
        if len(form["apellido"])<2:
            flash("El apellido debe tener al menos dos caracteres", "registro")
            is_valid = False

        if len(form["contrasena"])<6:
            flash("La contraseña debe tener al menos 6 caracteres", "registro")
            is_valid = False

        query = "select * from usuarios where email = %(email)s"
        result = connectToMySQL("cinepedia").query_db(query, form)
        if len(result) >=1:
            flash("E-mail ya está registrado", "registro")
            is_valid = False

        if form["contrasena"] != form["confirm"]: #de password lo cambie a contrasena por el name
            flash("Las contraseñas entregadas son diferentes", "registro")
            is_valid = False

        if not EMAIL_REGEX.match(form["email"]): #match empata una er con un texto, aca debe seguir el patron de correo
            flash("E-mail no es válido", "registro")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_by_id(cls, data): 
        query = "select * from usuarios where id = %(id)s"
        result = connectToMySQL("cinepedia").query_db(query, data)
        usuario = cls(result[0])
        return usuario
