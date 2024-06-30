#pipenv install flask pymysql flask-bcrypt

from flask_app import app

from flask_app.controllers import users_controlller
from flask_app.controllers import peliculas_controller
from flask_app.controllers import comentarios_controller

if __name__== "__main__":
    app.run(debug=True)