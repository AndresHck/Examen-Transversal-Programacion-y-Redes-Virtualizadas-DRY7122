# Script que crea un servidor web para gestionar usuarios y contraseñas seguras.

import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# --- Configuración de la Aplicación Flask ---
app = Flask(__name__)
DATABASE_NAME = 'usuarios.db'

# --- Funciones de la Base de Datos ---

def get_db_connection():
    """Crea una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    # Permite acceder a las filas por nombre de columna
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos y crea la tabla de usuarios si no existe."""
    conn = get_db_connection()
    # Leemos el schema.sql para crear la tabla
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

# --- Rutas de la API ---

@app.route('/')
def index():
    """Página de inicio para verificar que el servidor funciona."""
    return "Servidor de gestión de claves está en funcionamiento. Usa /signup para registrar."

@app.route('/signup', methods=['POST'])
def signup():
    """Ruta para registrar un nuevo usuario."""
    # Obtenemos el nombre y la contraseña del formulario de la solicitud
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return jsonify({'error': 'Faltan el nombre de usuario o la contraseña'}), 400

    # Creamos un hash seguro de la contraseña
    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    try:
        # Insertamos el nuevo usuario en la base de datos
        conn.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # Esto ocurre si el usuario ya existe (debido a la restricción UNIQUE)
        conn.close()
        return jsonify({'error': 'El nombre de usuario ya existe'}), 409
    finally:
        conn.close()
        
    return jsonify({'success': f'Usuario {username} creado exitosamente'}), 201

@app.route('/login', methods=['POST'])
def login():
    """Ruta para validar las credenciales de un usuario."""
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    # Buscamos al usuario en la base de datos
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    # Si no se encuentra el usuario o la contraseña no coincide
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Credenciales incorrectas'}), 401
    
    return jsonify({'success': f'Bienvenido {username}!'}), 200


# --- Punto de Entrada del Script ---
if __name__ == '__main__':
    # Antes de iniciar el servidor, creamos el archivo schema.sql
    with open('schema.sql', 'w') as f:
        f.write("""
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
        """)
    # Inicializamos la base de datos
    init_db()
    # Ejecutamos la aplicación Flask en el puerto 5800
    app.run(host='0.0.0.0', port=5800, debug=True)
