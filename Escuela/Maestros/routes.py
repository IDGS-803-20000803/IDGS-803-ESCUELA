from flask import Blueprint
from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
import forms
from db import get_connection

maestros = Blueprint('maestros', __name__)

@maestros.route('/getMaestro', methods = ['GET', 'POST'])
def get_maestros():
    maestro_form = forms.UserTeacherForm(request.form)
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_maestros()')
            resulset = cursor.fetchall()
            return render_template('Tabla_Maestros.html', form = maestro_form, resulset = resulset)
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('404.html', form = maestro_form)

@maestros.route('/insertMaestro', methods=['GET','POST'])
#Método para insertar maestro
def insertar_maestro():
    maestro_form = forms.UserTeacherForm(request.form)
    if request.method == 'POST':
        nombre = maestro_form.nombre.data
        materia = maestro_form.materia.data
        carrera = maestro_form.carrera.data
        celular = maestro_form.celular.data
        email = maestro_form.email.data

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_insertar_maestro(%s,%s,%s,%s,%s)',(nombre,materia,carrera, celular, email))
                connection.commit()
                connection.close()
                flash("Registro guardado exitosamente")
        except Exception as ex:
            flash("No se encontro ningun registro en la BD: " + str(ex))
        return redirect(url_for('maestros.get_maestros'))
    return render_template('Maestros.html', form = maestro_form)

@maestros.route('/deleteMaestro', methods = ['GET', 'POST'])
def delete_maestro():
    maestro_form = forms.UserTeacherForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                    cursor.execute('call buscar_id_maestro(%s)', (id,))
                    resulset = cursor.fetchall()
                    print(resulset)
                    return render_template('EliminarMaestros.html', form = maestro_form, id = id,resulset = resulset)
        except Exception as ex:
            flash("No se encontro ningun registro en la BD: " + str(ex))
        
    if request.method == 'POST':
        id = maestro_form.id.data
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_eliminar_maestro(%s)', (id,))
                connection.commit()
                connection.close()
                flash("Maestro Eliminado")
        except Exception as ex:
            flash("No se pudo elminar el registro: " + str(ex))
        return redirect(url_for('maestros.get_maestros'))
    return render_template('EliminarMaestros.html', form = maestro_form)

@maestros.route('/updateMaestro', methods = ['GET', 'POST'])
def update_maestro():
    maestro_form = forms.UserTeacherForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                    cursor.execute('call buscar_id_maestro(%s)', (id,))
                    resulset = cursor.fetchall()
                    print(resulset)
                    return render_template('Modificar_Maestros.html', form = maestro_form, id = id,resulset = resulset)
        except Exception as ex:
            flash("No se encontro ningun registro en la BD: " + str(ex))

        '''
        nombre = request.args.get('nombre')
        materia = request.args.get('materia')
        carrera = request.args.get('carrera')
        celular = request.args.get('celular')
        email = request.args.get('email')
       
        return render_template('Modificar_Maestros.html',form = maestro_form, id = id, nombre = nombre, materia = materia, carrera = carrera, email = email, celular = celular)
         '''
    if request.method == 'POST':
        id = maestro_form.id.data
        nombre = maestro_form.nombre.data
        materia = maestro_form.materia.data
        carrera = maestro_form.carrera.data
        celular = maestro_form.celular.data
        email = maestro_form.email.data
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_actualizar_maestro(%s, %s, %s, %s, %s, %s)', (id, nombre, materia, carrera, celular, email))
                connection.commit()
                connection.close()
                flash("Maestro Actualizado")
        except Exception as ex:
            flash("No se pudo modificar el registro: " + str(ex))
        return redirect(url_for('maestros.get_maestros'))
    return render_template('Modificar_Maestros.html', form = maestro_form)

@maestros.route('/searchMaestro', methods = ['GET'])
def search_maestro():
    maestro_form = forms.UserTeacherForm(request.form)
    buscar = request.args.get('buscar')
    print(buscar)
    try:
        connection = get_connection()
        with connection.cursor () as cursor:
            cursor.execute('call sp_seleccionar_maestro(%s)', (buscar,))
            resulset = cursor.fetchall()
            if len(resulset) == 0:
                flash("No se encontraron resultados para su busqueda.")
    except Exception as ex:
        flash("No fue posible encotrar el registro: " + str(ex))
    return render_template('Tabla_Maestros.html', form = maestro_form, resulset = resulset)