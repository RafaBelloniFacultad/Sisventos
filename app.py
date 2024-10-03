from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True) 
