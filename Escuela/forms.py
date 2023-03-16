from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    id = IntegerField('Id')
    nombre = StringField('Nombre')
    apellidos = StringField('Apellidos')
    email = EmailField('Correo')

class UserTeacherForm(Form):
    id = IntegerField('Id')
    nombre = StringField('Nombre')
    materia = StringField('Materia')
    carrera = StringField('Carrera')
    email = EmailField('Correo')
    celular = StringField('Celular')
   







