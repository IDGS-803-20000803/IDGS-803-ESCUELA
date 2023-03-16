from flask import Blueprint
from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
import forms
from db import get_connection

alumnos = Blueprint('alumnos', __name__)

@alumnos.route('/getAlumnos', methods = ['GET', 'POST'])
def get_alumnos():
    alumno_form = forms.UserForm(request.form)
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_alumnos()')
            resulset = cursor.fetchall()
            return render_template('Tabla_Alumnos.html', form = alumno_form, resulset = resulset)
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('404.html', form = alumno_form)

@alumnos.route('/insertAlumno', methods=['GET','POST'])
#Método para insertar Alumno
def insertar_alumno():
    alumno_form = forms.UserForm(request.form)
    if request.method == 'POST':
        nombre = alumno_form.nombre.data
        apellidos = alumno_form.apellidos.data
        email = alumno_form.email.data

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_insertar_alumno(%s,%s,%s)',(nombre,apellidos,email))
                connection.commit()
                connection.close()
                flash("Registro guardado exitosamente")
        except Exception as ex:
            flash("No se encontro ningun registro en la BD: " + str(ex))
        return redirect(url_for('alumnos.get_alumnos'))
    return render_template('Alumnos.html', form = alumno_form)

@alumnos.route('/deleteAlumno', methods = ['GET', 'POST'])
def delete_alumno():
    alumno_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        nombre = request.args.get('nombre')
        apellidos = request.args.get('apellidos')
        email = request.args.get('email')
       
        return render_template('EliminarAlumno.html',form = alumno_form, id = id, nombre = nombre,apellidos = apellidos,  email = email)
    
    if request.method == 'POST':
        id = alumno_form.id.data
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_eliminar_alumno(%s)', (id,))
                connection.commit()
                connection.close()
                flash("Alumno Eliminado")
        except Exception as ex:
            flash("No se pudo elminar el registro: " + str(ex))
        return redirect(url_for('alumnos.get_alumnos'))
    return render_template('EliminarMaestros.html', form = alumno_form)

@alumnos.route('/updateAlumno', methods = ['GET', 'POST'])
def update_alumno():
    alumno_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        nombre = request.args.get('nombre')
        apellidos = request.args.get('apellidos')
        email = request.args.get('email')
        
        return render_template('Modificar_Alumnos.html',form = alumno_form, id = id, nombre = nombre, apellidos = apellidos, email = email)
    
    if request.method == 'POST':
        id = alumno_form.id.data
        nombre = alumno_form.nombre.data
        apellidos = alumno_form.apellidos.data
        email = alumno_form.email.data
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_modificar_alumno(%s, %s, %s,%s)', (id, nombre, apellidos, email))
                connection.commit()
                connection.close()
                flash("Alumno Actualizado")
        except Exception as ex:
            flash("No se pudo modificar el registro: " + str(ex))
        return redirect(url_for('alumnos.get_alumnos'))
    return render_template('Modificar_Alumnos.html', form = alumno_form)

@alumnos.route('/searchAlumno', methods = ['GET'])
def search_alumno():
    alumno_form = forms.UserForm(request.form)
    buscar = request.args.get('buscar')
    try:
        connection = get_connection()
        with connection.cursor () as cursor:
            cursor.execute('call sp_seleccionar_alumno(%s)', (buscar,))
            resulset = cursor.fetchall()
            if len(resulset) == 0:
                flash("No se encontraron resultados para su busqueda.")
    except Exception as ex:
        flash("No fue posible encotrar el registro: " + str(ex))
    return render_template('Tabla_Alumnos.html', form = alumno_form, resulset = resulset)