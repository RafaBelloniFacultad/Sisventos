from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
from functools import wraps # Decoradores para requerir login

app = Flask(__name__)
app.secret_key = 'my_secret_key' # Necesario para usar sesiones

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Database connection
engine = create_engine('postgresql://postgres:rafa123@localhost:5432/Sisventos - Valto')
db_session = scoped_session(sessionmaker(bind=engine))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
    
# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            app.logger.debug(f"Acceso denegado: sesión no iniciada.")
            return redirect(url_for('administrador'))
        app.logger.debug(f"Acceso permitido: sesión iniciada.")
        return f(*args, **kwargs)
    return decorated_function


# Ruta principal que sirve la página del menú
@app.route('/')
def menu():
    return render_template('menu.html')

# Ruta para manejar redirecciones dinámicas según el tipo de usuario
@app.route('/login/<user_type>')
def login(user_type):
    if user_type == 'administrador':
        return redirect(url_for('administrador'))
    elif user_type == 'taquillero':
        return redirect(url_for('taquillero'))
    elif user_type == 'cocina':
        return redirect(url_for('encargado_cocina'))
    elif user_type == 'cajero':
        return redirect(url_for('cajero'))
    elif user_type == 'neverland':
        return redirect(url_for('neverland'))
    elif user_type == 'bingo':
        return redirect(url_for('bingo'))
    else:
        return 'Usuario no reconocido', 400

# Ruta para la página de login del administrador
@app.route('/login')
def administrador():
    return render_template('login.html')

# Ruta para la página principal del administrador después de un login exitoso
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# Rutas para cada tipo de usuario
@app.route('/taquillero')
def taquillero():
    return render_template('taquillero.html')

@app.route('/cajero')
def cajero():
    return render_template('cajero.html')

@app.route('/encargadoCocina')
def encargado_cocina():
    return render_template('encargadoCocina.html')

@app.route('/neverland')
def neverland():
    return render_template('neverland.html')

@app.route('/bingo')
def bingo():
    return render_template('bingo.html')


@app.route('/session-status')
def session_status():
    return jsonify(session=dict(session))

# Ruta para el cierre de sesión
@app.route('/logout', methods=['POST'])
def logout():
    app.logger.debug("Cerrando sesión para el usuario: %s", session.get('usuario'))
    session.clear()
    return redirect(url_for('administrador'))
    
# auth.py
@app.route('/auth/login', methods=['POST'])
def auth_login():
    data = request.json
    logging.debug(f"Received login data: {data}")
    
    nombre = data.get('usuario')
    contraseña = data.get('contraseña')
    
    if not nombre or not contraseña:
        return jsonify({"success": False, "message": "Usuario y contraseña son requeridos."})

    query = text("SELECT * FROM Usuarios WHERE nombre = :nombre")
    user = db_session.execute(query, {"nombre": nombre}).fetchone()
    
    logging.debug(f"Database query result: {user}")

    if user and check_password_hash(user[2], contraseña):
        session['logged_in'] = True
        session['usuario'] = nombre  # Guarda el nombre de usuario en la sesión
        return jsonify({"success": True, "redirect": url_for('admin')})  # Cambia el JSON response para redirigir a admin
    else:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos."})
    
#def login(jsonify):
#
#    return redirect(url_for('admin'))  # Redirige a la página de administrador

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        nombre = data['nombre']
        contraseña = data['contraseña']
        confirmar_contraseña = data['confirmarContraseña']
        rol = data['rol']
        
        # Validar campos faltantes
        if not nombre or not contraseña or not confirmar_contraseña or not rol:
            return jsonify({"success": False, "message": "Todos los campos son requeridos."})
        
        # Validar que coincidan las contraseñas
        if contraseña != confirmar_contraseña:
            return jsonify({"success": False, "message": "Las contraseñas no coinciden."})

        # Check if the username already exists
        query = text("SELECT * FROM Usuarios WHERE nombre = :nombre")
        if db_session.execute(query, {"nombre": nombre}).fetchone():
            return jsonify({"success": False, "message": "Nombre de usuario ya registrado."})

        # Insert new user into the database
        hashed_password = generate_password_hash(contraseña)
        insert_query = text("INSERT INTO Usuarios (nombre, contraseña, rol) VALUES (:nombre, :contraseña, :rol)")
        db_session.execute(insert_query, {"nombre": nombre, "contraseña": hashed_password, "rol": rol})
        db_session.commit()

        return jsonify({"success": True, "message": "Usuario registrado exitosamente."})
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True) 
