from flask import Flask, render_template, redirect, url_for, session, jsonify
from functools import wraps
from auth import auth_bp, auth_login, auth_register, auth_logout, db_session

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Registrar el Blueprint de autenticación
app.register_blueprint(auth_bp, url_prefix='/auth')

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('administrador'))
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
    # Rutas para otros tipos de usuarios
    # ...

# Ruta para la página de login del administrador
@app.route('/login')
def administrador():
    return render_template('login.html')

# Ruta para la página principal del administrador
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# Rutas para otros tipos de usuario
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

# Ruta para ir a la pantalla de registro
@app.route('/register')
def show_register():
    return render_template('register.html')

# Ruta para ver el estado de la sesión
@app.route('/sessionstatus')
def session_status():
    return jsonify(session=dict(session))

# Ruta para el cierre de sesión
@app.route('/logout', methods=['POST'])
def logout():
    return auth_logout()

# Ruta para el registro de sesión
@app.route('/register', methods=['POST'])
def register():
    return auth_register()

# Cerrar sesión y limpiar al terminar la app
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)

