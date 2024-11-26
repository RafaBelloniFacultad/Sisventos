from flask import Flask, Blueprint, request, session, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_login import UserMixin, current_user
from extensions import db
from auth import get_current_user_id, login_required

writeAdminBD = Blueprint('writeAdminBD', __name__)
#db = SQLAlchemy()s

# Models
class Evento(db.Model):
    __tablename__ = 'evento'
    id = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String)
    fecha = db.Column(db.Date)
    stock_anticipadas = db.Column(db.Integer)
    precioanticipada = db.Column(db.Float)
    preciopuerta = db.Column(db.Float)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

class Comidas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String)
    especial = db.Column(db.Boolean)

class Stock(db.Model):
    id = db.Column(db.String, primary_key=True)
    comidas_id = db.Column(db.Integer, db.ForeignKey('comidas.id'))
    evento_id = db.Column(db.BigInteger, db.ForeignKey('evento.id'))
    inversion = db.Column(db.Float)
    detalles = db.Column(db.String)
    stock_inicial = db.Column(db.Integer)
    precio = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True)
    contraseña = db.Column(db.String)
    rol = db.Column(db.String)

@writeAdminBD.route('/submit-buffet', methods=['POST'])
@login_required
def submit_buffet():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Usuario no autenticado'}), 401
    try:
        data = request.json
        print("Received data:", data)
        
        # Extract event data
        event_type = data['eventType']
        event_date = datetime.strptime(data['eventDate'], '%Y-%m-%d').date()
        event_id = int(event_date.strftime('%Y%m%d'))
        
        # Create new event
        new_event = Evento(
            id=event_id,
            nombre=event_type,
            fecha=event_date,
            stock_anticipadas=0,  # You might want to add this to your form
            precioanticipada=None,  # You might want to add this to your form
            preciopuerta=None,
            idusuario= 5 #get_current_user_id()  # Implement this function to get the current user's ID
        )
        db.session.add(new_event)
        
        # Process foods
        for food in data['foods']:
            # Create or get existing food
            comida = Comidas.query.filter_by(nombre=food['name']).first()
            if not comida:
                comida = Comidas(
                    nombre=food['name'],
                    especial=(event_type == 'Feria de Comida')
                )
                db.session.add(comida)
                db.session.flush()  # This will assign an ID to the new comida
            
            # Create stock entry
            stock = Stock(
                id=f"{event_id}_{comida.id}",
                comidas_id=comida.id,
                evento_id=event_id,
                inversion=float(food['totalCost']),
                detalles=food['comments'],
                stock_inicial=int(food['quantity']),
                precio=float(food['unitPrice'])
            )
            db.session.add(stock)
        
        db.session.commit()
        print("Buffet saved successfully")  # Log success
        return jsonify({'success': True, 'message': 'Buffet cargado exitosamente'}), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print("SQLAlchemy error:", str(e))  # Log SQLAlchemy errors
        return jsonify({'success': False, 'message': str(e)}), 500
    except Exception as e:
        db.session.rollback()
        print("Unexpected error:", str(e))  # Log unexpected errors
        return jsonify({'success': False, 'message': 'Error inesperado'}), 500

def get_current_user_id():
    return current_user.id if current_user.is_authenticated else None

# Make sure to initialize the blueprint and SQLAlchemy in your main app file
# app.register_blueprint(writeAdminBD)
# db.init_app(app)