import flask 
from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
import forms
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models import db
from models import Alumnos
from models import Maestros

from Alumnos.routes import alumnos
from Maestros.routes import maestros

app = flask.Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


@app.route("/", methods = ['GET','POST'])
def index():
    return render_template('index.html')

app.register_blueprint(alumnos)
app.register_blueprint(maestros)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=5000)