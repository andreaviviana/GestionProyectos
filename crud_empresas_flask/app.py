import os # Importar el módulo OS para acceder a variables de entorno
from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_app

app = Flask(__name__)


app.secret_key = os.getenv('SECRET_KEY')

if not app.secret_key:
    # Esta excepción asegura que la aplicación no se ejecute en producción sin una clave configurada.
    raise RuntimeError("La variable de entorno 'SECRET_KEY' no está configurada. Por favor, establécela para la seguridad de la aplicación.")

# Inicializar MySQL
mysql = init_app(app)

# LISTAR EMPRESAS

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EMPRESAS ORDER BY id_empresa DESC")
    empresas = cur.fetchall()
    return render_template('index.html', empresas=empresas)

# FORMULARIO: CREAR EMPRESA

@app.route('/create')
def create():
    return render_template('create.html')

# GUARDAR NUEVA EMPRESA

@app.route('/store', methods=['POST'])
def store():
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    correo = request.form['correo']
    nit = request.form['nit']

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO EMPRESAS (nombre, direccion, telefono, correo, nit)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, direccion, telefono, correo, nit))
    mysql.connection.commit()

    flash("Empresa creada correctamente", "success")
    return redirect(url_for('index'))

# FORMULARIO: EDITAR EMPRESA

@app.route('/edit/<int:id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EMPRESAS WHERE id_empresa = %s", (id,))
    empresa = cur.fetchone()
    return render_template('edit.html', empresa=empresa)

# ACTUALIZAR EMPRESA

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    correo = request.form['correo']
    nit = request.form['nit']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE EMPRESAS SET nombre=%s, direccion=%s, telefono=%s, correo=%s, nit=%s
        WHERE id_empresa=%s
    """, (nombre, direccion, telefono, correo, nit, id))
    mysql.connection.commit()

    flash("Empresa actualizada correctamente", "info")
    return redirect(url_for('index'))

# VER EMPRESA

@app.route('/view/<int:id>')
def view(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EMPRESAS WHERE id_empresa = %s", (id,))
    empresa = cur.fetchone()
    return render_template('view.html', empresa=empresa)

# ELIMINAR EMPRESA

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM EMPRESAS WHERE id_empresa = %s", (id,))
    mysql.connection.commit()

    flash("Empresa eliminada correctamente", "danger")
    return redirect(url_for('index'))

# INICIAR SERVIDOR

if __name__ == '__main__':
    app.run(debug=True)
