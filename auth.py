from flask import Blueprint, request, jsonify, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
from datetime import timedelta

# Definir el Blueprint de autenticación
auth_bp = Blueprint('auth', __name__)

# Database connection
engine = create_engine('postgresql://postgres:rafa123@localhost:5432/Sisventos - Valto')
db_session = scoped_session(sessionmaker(bind=engine))

# Función para manejar el login
@auth_bp.route('/auth_login', methods=['POST'])
def auth_login():
    data = request.json
    nombre = data.get('usuario')
    contraseña = data.get('contraseña')

    if not nombre or not contraseña:
        return jsonify({"success": False, "message": "Usuario y contraseña son requeridos."})

    query = text("SELECT * FROM Usuarios WHERE nombre = :nombre")
    user = db_session.execute(query, {"nombre": nombre}).fetchone()

    if user and check_password_hash(user[2], contraseña):
        session.permanent = True  # Habilitar expiración de sesión
        session['logged_in'] = True
        session['usuario'] = nombre
        session['user_id'] = user[0]
        return jsonify({"success": True, "redirect": url_for('admin')})
    else:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos."})

# Función para manejar el registro
@auth_bp.route('/auth_register', methods=['POST'])
def auth_register():
    data = request.json
    nombre = data['nombre']
    contraseña = data['contraseña']
    confirmar_contraseña = data['confirmarContraseña']
    rol = data['rol']
    clave_maestra = data['claveMaestra']  # Nueva campo para la clave maestra

    # Verificar la clave maestra
    if clave_maestra != "pediseloarafa":
        return jsonify({"success": False, "message": "Clave maestra incorrecta."})
    
    if not nombre or not contraseña or not confirmar_contraseña or not rol or not clave_maestra:
        return jsonify({"success": False, "message": "Todos los campos son requeridos."})

    if contraseña != confirmar_contraseña:
        return jsonify({"success": False, "message": "Las contraseñas no coinciden."})

    query = text("SELECT * FROM Usuarios WHERE nombre = :nombre")
    if db_session.execute(query, {"nombre": nombre}).fetchone():
        return jsonify({"success": False, "message": "Nombre de usuario ya registrado."})

    hashed_password = generate_password_hash(contraseña)
    insert_query = text("INSERT INTO Usuarios (nombre, contraseña, rol) VALUES (:nombre, :contraseña, :rol)")
    db_session.execute(insert_query, {"nombre": nombre, "contraseña": hashed_password, "rol": rol})
    db_session.commit()

    return jsonify({"success": True, "message": "Usuario registrado exitosamente."})

# Función para manejar el cierre de sesión
#def auth_logout():
#    session.clear()
#    return redirect(url_for('administrador'))

def auth_logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('usuario', None)
    session.clear()
    return jsonify({"success": True})

# Función para obtener el ID del usuario actual
@auth_bp.route('/auth_logout')
def get_current_user_id():
    return session.get('user_id')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or 'user_id' not in session:
            session.clear()
            return redirect(url_for('administrador'))
        return f(*args, **kwargs)
    return decorated_function