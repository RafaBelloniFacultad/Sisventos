#from flask import Flask, request, jsonify, render_template, session
#from werkzeug.security import generate_password_hash, check_password_hash
#from sqlalchemy import create_engine, text
#from sqlalchemy.orm import scoped_session, sessionmaker
#import logging
#
#app = Flask(__name__)
#
#
## Database connection
#engine = create_engine('postgresql://postgres:rafa123@localhost:5432/Sisventos - Valto')
#db_session = scoped_session(sessionmaker(bind=engine))
#
#@app.teardown_appcontext
#def shutdown_session(exception=None):
#    db_session.remove()
#
## Home route
#@app.route('/')
#def home():
#    return render_template('login.html')
#    
## Login route
#@app.route('/auth/login', methods=['POST'])
#def login():
#    data = request.json
#    nombre = data['usuario']
#    contraseña = data['contraseña']
#
#    query = text("SELECT * FROM Usuarios WHERE nombre = :nombre")
#    user = db_session.execute(query, {"nombre": nombre}).fetchone()
#
#    if user and check_password_hash(user[2], contraseña):
#        return jsonify({"success": True})
#    else:
#        return jsonify({"success": False})
#
## Register route
#@app.route('/register', methods=['GET', 'POST'])
#def register():
#    if request.method == 'POST':
#        data = request.json
#        nombre = data['nombre']
#        contraseña = data['contraseña']
#        confirmar_contraseña = data['confirmarContraseña']
#        rol = data['rol']
#        
#        # Validar campos faltantes
#        if not nombre or not contraseña or not confirmar_contraseña or not rol:
#            return jsonify({"success": False, "message": "Todos los campos son requeridos."})
#        
#        # Validar que coincidan las contraseñas
#        if contraseña != confirmar_contraseña:
#            return jsonify({"success": False, "message": "Las contraseñas no coinciden."})
#
#        # Check if the username already exists
#        query = text("SELECT * FROM Usuarios WHERE nombre = :nombre")
#        if db_session.execute(query, {"nombre": nombre}).fetchone():
#            return jsonify({"success": False, "message": "Nombre de usuario ya registrado."})
#
#        # Insert new user into the database
#        hashed_password = generate_password_hash(contraseña)
#        insert_query = text("INSERT INTO Usuarios (nombre, contraseña, rol) VALUES (:nombre, :contraseña, :rol)")
#        db_session.execute(insert_query, {"nombre": nombre, "contraseña": hashed_password, "rol": rol})
#        db_session.commit()
#
#        return jsonify({"success": True, "message": "Usuario registrado exitosamente."})
#    else:
#        return render_template('register.html')
#
#if __name__ == '__main__':
#    app.run(debug=True)
