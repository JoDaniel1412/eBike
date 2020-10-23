from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_cors import CORS, cross_origin
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://sa:1234@DESKTOP-A1FP3OB\MSSQLSERVER01/database_central?driver=SQL Server"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class marcas(db.Model):
    __tablename__ = 'marcas'
    __table_args__ = {"schema": "produccion"}
    idMarca = db.Column(db.Integer, primary_key=True)
    nomMarca = db.Column(db.String(255), nullable = False)

class categorias(db.Model):
    __tablename__ = 'categorias'
    __table_args__ = {"schema": "produccion"}
    idCategoria = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable = False)

class tiendas(db.Model):
    __tablename__ = 'tiendas'
    __table_args__ = {"schema": "ventas"}
    idTienda = db.Column(db.Integer, primary_key=True, )
    nomTienda = db.Column(db.String(255), nullable = False)
    telefono = db.Column(db.String(255), nullable = True)
    email = db.Column(db.String(255), nullable = True)
    calle = db.Column(db.String(255), nullable = True)
    ciudad = db.Column(db.String(255), nullable = True)
    estado = db.Column(db.String(10), nullable = True)
    codPostal = db.Column(db.String(5), nullable = True)

class clientes(db.Model):
    __tablename__ = 'clientes'
    __table_args__ = {"schema": "ventas"}
    idCliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable = False)
    apellido = db.Column(db.String(255), nullable = False)
    telefono = db.Column(db.String(255), nullable = True)
    email = db.Column(db.String(255), nullable = False)
    calle = db.Column(db.String(255), nullable = True)
    ciudad = db.Column(db.String(50), nullable = True)
    estado = db.Column(db.String(25), nullable = True)
    codPostal = db.Column(db.String(5), nullable = True)

class empleados(db.Model):
    __tablename__ = 'empleados'
    __table_args__ = {"schema": "ventas"}
    idEmpleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable = False)
    apellido = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    telefono = db.Column(db.String(25), nullable = True)
    activo = db.Column(db.Integer, nullable = False)
    idTienda = db.Column(db.Integer, db.ForeignKey('ventas.tiendas.idTienda'), nullable = False)
    idJefe = db.Column(db.Integer, db.ForeignKey('ventas.empleados.idEmpleado'), nullable = True)

class ordenes(db.Model):
    __tablename__ = 'ordenes'
    __table_args__ = {"schema": "ventas"}
    idOrden = db.Column(db.Integer, primary_key=True)
    idCliente = db.Column(db.Integer, db.ForeignKey('ventas.clientes.idCliente'), nullable = False)
    estadoOrden = db.Column(db.Integer, nullable = False)
    fechaOrden = db.Column(db.Date, nullable = False)
    required_date = db.Column(db.Date, nullable = False)
    fechaEnvio = db.Column(db.Date, nullable = True)
    idTienda = db.Column(db.Integer, db.ForeignKey('ventas.tiendas.idTienda'), nullable = False)
    idEmpleado = db.Column(db.Integer, db.ForeignKey('ventas.empleados.idEmpleado'), nullable = False)
    children = db.relationship("clientes")
    children = db.relationship("tiendas")
    children = db.relationship("empleados")

#----------------------------- Admin View ----------------------------

# Testeo
@app.route('/marca', methods=['GET'])
def get_marca():

    all_marcas = marcas.query.with_entities(
        marcas.idMarca,
        marcas.nomMarca
    ).all()
    
    result = []

    for marca in all_marcas:
        new_marca = []

        for data in marca:
            new_marca.append(data)

        result.append(new_marca)

    return jsonify(result), 200

# Categories
@app.route('/categories', methods=['GET'])
def get_category():

    categories = categorias.query.with_entities(
        categorias.idCategoria,
        categorias.descripcion
    ).all()
    
    result = []

    for category in categories:
        new_category = []

        for data in category:
            new_category.append(data)

        result.append(new_category)

    return jsonify(result), 200

# Store names
@app.route('/stores', methods=['GET'])
def get_stores():

    stores = tiendas.query.with_entities(
        tiendas.idTienda,
        tiendas.nomTienda,
        tiendas.telefono,
        tiendas.email,
        tiendas.calle,
        tiendas.ciudad,
        tiendas.estado,
        tiendas.codPostal
    ).all()
    
    result = []

    for store in stores:
        new_store = []

        for data in store:
            new_store.append(data)

        result.append(new_store)

    return jsonify(result), 200

#Top clients
@app.route('/clients', methods=['GET'])
def get_clients():

    clients = clientes.query.with_entities(
        clientes.idCliente,
        clientes.nombre,
        clientes.apellido,
        clientes.telefono,
        clientes.email,
        clientes.calle,
        clientes.ciudad,
        clientes.estado,
        clientes.codPostal
    ).all()
    
    result = []

    for client in clients:
        new_client = []

        for data in client:
            new_client.append(data)

        result.append(new_client)

    return jsonify(result), 200


# Number of orders per client
@app.route('/orders/client', methods=['GET'])
def get_order_client():

    orders = ordenes.query.join(clientes).join(tiendas).join(empleados).with_entities(
        clientes.idCliente,
        clientes.nombre,
        clientes.apellido,
        clientes.telefono,
        clientes.email,
        clientes.calle,
        clientes.ciudad,
        clientes.estado,
        clientes.codPostal,
        ordenes.estadoOrden
    ).all()
    
    result = []

    for order in orders:
        to_send = []

        for data in order:
            to_send.append(data)

        result.append(to_send)

    return jsonify(result), 200

#----------------------------- Run  ----------------------------

if __name__ == "__main__":
    app.run(debug=True)