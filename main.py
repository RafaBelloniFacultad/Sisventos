from flask import Flask, render_template, request, redirect, jsonify, session
from flask_socketio import SocketIO, join_room, leave_room, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True)
app.secret_key = "hoy hace mucho frio"

#SECCIÓN DE FUNCIONES#
#dato -> columna del dato que se busca
#tabla -> tabla donde se busca
def select(dato, tabla):
  db = sqlite3.connect("BataData.db")
  cursor = db.cursor()
  cursor.execute(f"SELECT {dato} FROM {tabla}")
  datos = cursor.fetchall()
  db.close()
  return datos

#Añado condicion -> requisito que debe cumplir fila para devolverme el dato
def select_where(dato, tabla, condicion):
  db = sqlite3.connect("BataData.db")
  cursor = db.cursor()
  cursor.execute(f"SELECT {dato} FROM {tabla} WHERE {condicion}")
  datos = cursor.fetchall()
  db.close()
  return datos

def insert(tabla, columnas, valores):
  db = sqlite3.connect("BataData.db")
  cursor = db.cursor()
  cursor.execute(f"INSERT INTO {tabla} ({columnas}) VALUES ({valores});")
  db.commit()
  db.close()

def update(tabla, valores, condicion):
  db = sqlite3.connect("BataData.db")
  cursor = db.cursor()
  cursor.execute(f"UPDATE {tabla} SET {valores} WHERE {condicion};")
  db.commit()
  db.close()

def delete(tabla):
  db = sqlite3.connect("BataData.db")
  cursor = db.cursor()
  cursor.execute(f"DELETE FROM {tabla};")
  db.commit()
  db.close()

def delete_where(tabla, condicion):
  db = sqlite3.connect("BataData.db")
  cursor = db.cursor()
  cursor.execute(f"DELETE FROM {tabla} WHERE {condicion};")
  db.commit()
  db.close()

#RUTAS DE LA PAGINA#
@app.route("/")
def index():
  session["usuario"] = ""
  session["funcion"] = ""
  return render_template("index.html")

@app.route("/comprobar_usuario")
def comprobar_usuario():
  data = request.args
  print("LLEGUE")
  print(data)
  contra = select_where("contrasenia", "usuarios", f"id = '{data['usuario']}'")[0][0]
  if contra == data['contrasenia']:
    session['usuario'] = data['usuario']
    return jsonify(0)
  else:
    return jsonify(1)

@app.route("/redireccion")
def redireccion():
  if request.method == "GET":
    if session['usuario'] == "":
      return redirect("/")
    funcion = select_where("funcion", "usuarios", f"id = '{session['usuario']}'")[0][0]
    if funcion == "menu":
      return redirect("/menu")
    elif funcion == "caja":
      return redirect("/caja")
    elif funcion == "admin":
      return redirect("/admin")

@app.route("/menu", methods=["GET", "POST"])
def menu():
  if request.method == "GET":
    return render_template("menu.html")

@app.route("/caja")
def caja():
  return render_template("caja.html")

@app.route("/admin")
def admin():
  return render_template("administrador.html")

@app.route("/agregar-producto", methods=["GET", "POST"])
def agregar():
  if request.method == "POST":
    producto = request.form["id"]
    producto = producto.replace(" ", "_")
    stock = request.form["stock"]
    precio = request.form["precio"]
    costo = request.form["costo"]
    insert("productos", "id, precio, costo_compra, stock_inicial", f"'{producto}', {precio}, {costo}, {stock}")
    return redirect("/admin")

#PEDIDOS AJAX#
  #Ajax genericos
@app.route("/select")
def pedido_select():
  dato = request.args.get("dato")
  tabla = request.args.get("tabla")
  informacion = select(dato, tabla)
  return jsonify(informacion)

@app.route("/select-where")
def pedido_select_where():
  dato = request.args.get("dato")
  tabla = request.args.get("tabla")
  condicion = request.args.get("condicion")
  informacion = select_where(dato, tabla, condicion)
  return jsonify(informacion)

@app.route("/update", methods=["GET", "PUT"])
def pedido_update():
  if request.method == "PUT":
    tabla = request.form.get("tabla")
    valores = request.form.get("valores")
    condicion = request.form.get("condicion")
    update(tabla, valores, condicion)
    return jsonify(0)

@app.route("/delete", methods=["GET", "DELETE"])
def pedido_delete():
  if request.method == "DELETE":
    tabla = request.form.get("tabla")
    delete(tabla)
    return jsonify(0)

@app.route("/delete-where", methods=["GET", "DELETE"])
def pedido_delete_where():
  if request.method == "DELETE":
    tabla = request.form.get("tabla")
    condicion = request.form.get("condicion")
    delete_where(tabla, condicion)
    return jsonify(0)
  #Ajax pagina menu
@app.route("/numero-pedido")
def numero_pedido():
  n = select_where("MAX(id)", "pedidos", f"id_usuario = '{session['usuario']}'")[0][0]
  return jsonify(n)

@app.route("/stock-producto")
def calcular_stock():
  error = 0
  mensaje = ""
  productos = select("id", "productos")
  for i in productos:
    id_producto = i[0]
    cantidad = request.args.get(id_producto)
    stock = select_where("stock_inicial", "productos", f"id = '{id_producto}'")[0][0]
    vendidos = select_where("SUM(ventas)", "productos_por_pedido", f"id_producto = '{id_producto}'")[0][0]
    if vendidos == None:
      vendidos = 0
    if int(cantidad) > stock - vendidos:
      error = 1
      mensaje += f"Solo quedan {stock - vendidos} del producto '{id_producto}'"
  respuesta = {"error":error,"mensaje":mensaje}
  return jsonify(respuesta)

  #ajax pagina admin
@app.route("/historial")
def historial():
  db = sqlite3.connect("BataData.db")
  cursor = db.cursor()
  productos = select("id", "productos")
  data = []
  for i in productos:
    ventas = cursor.execute(f"""SELECT SUM(ventas)
    FROM productos_por_pedido
    INNER JOIN pedidos ON id_pedido = id
    WHERE entregado = 1 AND id_producto = '{i[0]}' AND productos_por_pedido.id_usuario = pedidos.id_usuario;""").fetchall()[0][0]
    print("VENTAS: ", ventas)
    if ventas == None:
      ventas = 0
    precio = select_where("precio", "productos", f"id = '{i[0]}'")[0][0]
    costo = select_where("costo_compra", "productos", f"id = '{i[0]}'")[0][0]
    stock_i = select_where("stock_inicial", "productos", f"id = '{i[0]}'")[0][0]
    stock = stock_i - ventas
    data.append({"producto":i[0], "ventas":ventas, "precio":precio, "costo":costo, "stock":stock})
  return jsonify(data)

@app.route("/historial-cajas")
def historial_cajas():
  db = sqlite3.connect("BataData.db")
  cursor = db.cursor()
  productos = select("id", "productos")
  usuarios = select_where("id", "usuarios", "funcion = 'menu'")
  data = []
  for i in usuarios:
    ganancia = 0
    for j in productos:
      ventas = cursor.execute(f"""SELECT SUM(ventas)
      FROM productos_por_pedido
      INNER JOIN pedidos ON productos_por_pedido.id_usuario = pedidos.id_usuario and id_pedido = id
      WHERE entregado = 1 and productos_por_pedido.id_usuario = '{i[0]}' and id_producto = '{j[0]}';""").fetchall()[0][0]
      if ventas == None:
        ventas = 0
      precio = select_where("precio", "productos", f"id = '{j[0]}'")[0][0]
      ganancia += ventas * precio
    data.append({"caja":i[0], "ganancia":ganancia})
  return jsonify(data)
  
#SOCKET
@socketio.on("unirse")
def socket_unirse():
  join_room(1)

@socketio.on("salir")
def socket_salir():
  leave_room(1)

@socketio.on("nuevo_pedido")
def actualizar_lista_pedidos(data):
  n_pedido = select_where("MAX(id)", "pedidos", f"id_usuario = '{session['usuario']}'")[0][0]
  if n_pedido == None:
    n_pedido = 0
  insert("pedidos", "id, id_usuario, aclaracion, entregado", f"{n_pedido + 1}, '{session['usuario']}', '{data[0]['observacion']}', 0")
  for i in data:
    if int(i["ventas"]) != 0:
      insert("productos_por_pedido", "id_producto, id_usuario, id_pedido, ventas", f"'{i['producto']}', '{session['usuario']}', {n_pedido + 1}, {i['ventas']}")
  emit("actualizar", to=1)
  
app.run(host='0.0.0.0', port=81)