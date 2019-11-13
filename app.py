#!/usr/bin/env python
import csv
import AccesoArchivo
import Utilidades
import string
from datetime import datetime
from decimal import Decimal

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap

from forms import LoginForm, SaludarForm, RegistrarForm, ClientesFiltroForm


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'


@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    print('ventas')
    iClientes = []
    iEncabezados = []    
    if 'username' in session:
        try:
            if not 'iClientes' in session:
                iClientes = AccesoArchivo.AbrirArchivoCSV('clientes.csv')
            else:
                iClientes = session['iClientes']
                
            iEncabezados = iClientes[0].keys()
            
        except Exception as e:
            flash('Error: ' + str(e))
        finally:
            return render_template('clientes.html', transacciones = iClientes, encabezados=iEncabezados)
    else:
        return ingresar()


@app.route('/clientesFiltro', methods=['GET', 'POST'])
def clientesFiltro():
    print('clientes filtro')
    iClientes = []
    iClientesResult = []
    iEncabezados = [] 
    formulario = ClientesFiltroForm()
    if 'username' in session:
        try:
            if not 'iClientes' in session:
                iClientes = AccesoArchivo.AbrirArchivoCSV('clientes.csv')
                iClientesResult = iClientes
            else:
                iClientes = session['iClientes']
                iClientesResult = iClientes

            iEncabezados = iClientes[0].keys()
            if formulario.is_submitted():  # Acá hice el POST si es True
                r = Utilidades.ValidarSoloLetras(formulario.txtPais.data)
                if r:
                    iClientesResult = []
                    for item in iClientes:
                        if formulario.txtPais.data == '' or str(item['País']).upper() == formulario.txtPais.data.upper():
                            iClientesResult.append(item)
                else:
                    flash('Debe ingresar un dato válido (sólo letras)')
        except Exception as e:
            print(e)
            flash('Error: ' + str(e))
        finally:
            return render_template('clientesFiltro.html', transacciones = iClientesResult, encabezados=iEncabezados, formulario=formulario)
    else:
        return ingresar()


@app.route('/saludar', methods=['GET', 'POST'])
def saludar():

    if 'username' in session:
        formulario = SaludarForm()
        if formulario.validate_on_submit():  # Acá hice el POST si es True
            return redirect(url_for('saludar_persona', usuario=formulario.usuario.data))
        return render_template('saludar.html', form=formulario)
    else:
        return ingresar()

@app.route('/sobre')
def sobre():

    if 'username' in session:
        return render_template('sobre.html')
    else:
        return ingresar()

@app.route('/saludar/<usuario>')
def saludar_persona(usuario):
    if 'username' in session:
        return render_template('usuarios.html', nombre=usuario)
    else:
        return ingresar()


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():

    if not 'username' in session:
        formulario = LoginForm()
        if formulario.validate_on_submit():
            with open('usuarios') as archivo:
                archivo_csv = csv.reader(archivo)
                registro = next(archivo_csv)
                while registro:
                    if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                        print('postback success')
                        flash('Bienvenido')
                        session['username'] = formulario.usuario.data
                        return render_template('ingresado.html')
                    registro = next(archivo_csv, None)
                else:
                    print('postback error')
                    flash('Revisá nombre de usuario y contraseña')
                    return redirect(url_for('ingresar'))
        return render_template('login.html', formulario=formulario)
    else:
        return index()


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
