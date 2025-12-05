from flask_mysqldb import MySQL

def init_app(app):
    # Configuración de la base de datos MySQL
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''  
    app.config['MYSQL_DB'] = 'gestion_proyectos'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # devuelve diccionarios

    return MySQL(app)
