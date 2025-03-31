from flask import Flask
from os import path
import mysql.connector
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='joemama'
    from .views import views
    from .auth import auth
    from .database import database
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(database,url_prefix="/")
    return app