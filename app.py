from flask import Flask, render_template, redirect, url_for, jsonify, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager
from auth import auth_bp, auth_login, auth_register, auth_logout, db_session
from writeAdminBD import writeAdminBD, Usuario, Evento
from extensions import db
from functools import wraps
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rafa123@localhost:5432/Sisventos - Valto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de sesiones
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1, minutes=30)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Initialize SQLAlchemy
#db = SQLAlchemy(app)
db.init_app(app)


with app.app_context():
    db.create_all()

# Registrar Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(writeAdminBD)

# Decorador para rutas protegidas
#def login_required(f):
#    @wraps(f)
#    def decorated_function(*args, **kwargs):
#        if 'logged_in' not in session:
#            return redirect(url_for('administrador'))
#        return f(*args, **kwargs)
#    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not session.get('user_id'):
            return redirect(url_for('administrador'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def check_session():
    if request.endpoint and 'static' not in request.endpoint:
        if not session.get('logged_in') and request.endpoint not in ['administrador', 'login', 'index', 'preMenu', 'auth_login', 'auth_register', 'register']:
            session.clear()

# Ruta principal que sirve la página del menú
@app.route('/')
def index():
    return render_template('prelogin.html')
    #return render_template('menu.html')
    
@app.route('/preMenu')
def preMenu():
    return render_template('preMenu.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

# Ruta para manejar redirecciones dinámicas según el tipo de usuario
@app.route('/login/<user_type>')
def login(user_type):
    if user_type == 'administrador':
        return redirect(url_for('administrador'))
    elif user_type == 'taquillero':
        return redirect(url_for('taquillero'))
    elif user_type == 'cajero':
        return redirect(url_for('cajero'))
    elif user_type == 'cocina':
        return redirect(url_for('cocina'))
    elif user_type == 'neverland':
        return redirect(url_for('neverland'))
    elif user_type == 'bingo':
        return redirect(url_for('bingo'))
    else:
        return 'Tipo de usuario no válido', 400

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

@app.route('/cocina')
def cocina():
    return render_template('cocina.html')

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
    
@app.route('/verificar-evento', methods=['POST'])
def verificar_evento():
    try:
        data = request.json
        codigo = data.get('codigo')
        
        # Verificar si existe el evento con ese código
        evento = Evento.query.filter_by(id=codigo).first()
        
        return jsonify({
            'exists': evento is not None
        })
    except Exception as e:
        return jsonify({
            'exists': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)

