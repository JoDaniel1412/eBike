from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_cors import CORS, cross_origin
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

# -------------------------------------- Conexion con las bases de datos -----------------------------------------------
app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_BINDS'] = {
    'newyork':      "mssql+pyodbc://crisptofer12ff:*cristofer12ff*@13.66.5.40/NewYork?driver=SQL Server Native Client 11.0",
    'texas':        "mssql+pyodbc://crisptofer12ff:*cristofer12ff*@157.55.196.141/Texas?driver=SQL Server Native Client 11.0",
    'california':   "mssql+pyodbc://ezuniga97:@Esteban1497@13.85.159.205/California?driver=SQL Server Native Client 11.0"
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['CORS_EXPOSE_HEADERS'] = True

# -------------------------------------- Modelo de la base de California -----------------------------------------------
db_california = SQLAlchemy(app)

class categorias_california(db_california.Model):
    __bind_key__ = 'california'
    __tablename__ = 'categorias'
    __table_args__ = {"schema": "produccion"}
    idCategoria = db_california.Column(db_california.Integer, primary_key=True)
    descripcion = db_california.Column(db_california.String(255), nullable = False)

class productos_california(db_california.Model):
    __bind_key__ = 'california'
    __tablename__ = 'productos'
    __table_args__ = {"schema": "produccion"}
    idProducto = db_california.Column(db_california.Integer, primary_key=True)
    nomProducto = db_california.Column(db_california.String(255), nullable = False)
    idMarca = db_california.Column(db_california.Integer, nullable = False)
    idCategoria = db_california.Column(db_california.Integer, db_california.ForeignKey('produccion.categorias.idCategoria'), nullable = False)
    annoModelo = db_california.Column(db_california.Integer, nullable = False)
    precioVenta = db_california.Column(db_california.Integer, nullable = False)

class clientes_california(db_california.Model):
    __bind_key__ = 'california'
    __tablename__ = 'clientes'
    __table_args__ = {"schema": "ventas"}
    idCliente = db_california.Column(db_california.Integer, primary_key=True, autoincrement=True)
    nombre = db_california.Column(db_california.String(255), nullable = False)
    apellido = db_california.Column(db_california.String(255), nullable = False)
    telefono = db_california.Column(db_california.String(25), nullable = True)
    email = db_california.Column(db_california.String(255), nullable = False)
    calle = db_california.Column(db_california.String(255), nullable = True)
    ciudad = db_california.Column(db_california.String(50), nullable = True)
    estado = db_california.Column(db_california.String(25), nullable = True)
    codPostal = db_california.Column(db_california.String(5), nullable = True)

class detalleOrden_california(db_california.Model):
    __bind_key__ = 'california'
    __tablename__ = 'detalleOrden'
    __table_args__ = {"schema": "ventas"}
    idOrden = db_california.Column(db_california.Integer, db_california.ForeignKey('ventas.ordenes.idOrden'), primary_key=True, nullable = True)
    idItem = db_california.Column(db_california.Integer, nullable = True)
    idProducto = db_california.Column(db_california.Integer,db_california.ForeignKey('produccion.productos.idProducto'), primary_key=True, nullable = False)
    cantidad = db_california.Column(db_california.Integer, nullable = False)
    precioVenta = db_california.Column(db_california.Integer, nullable = False)
    descuento = db_california.Column(db_california.Integer, nullable = False, default=0)

class ordenes_california(db_california.Model):
    __bind_key__ = 'california'
    __tablename__ = 'ordenes'
    __table_args__ = {"schema": "ventas"}
    idOrden = db_california.Column(db_california.Integer, primary_key=True, autoincrement = False)
    idCliente = db_california.Column(db_california.Integer, db_california.ForeignKey('ventas.clientes.idCliente'), nullable = True)
    estadoOrden = db_california.Column(db_california.Integer, nullable = False)
    fechaOrden = db_california.Column(db_california.Date, nullable = False)
    required_date = db_california.Column(db_california.Date, nullable = False)
    fechaEnvio = db_california.Column(db_california.Date, nullable = True)
    idTienda = db_california.Column(db_california.Integer, nullable = False)
    idEmpleado = db_california.Column(db_california.Integer, nullable = False)

# -------------------------------------- Modelo de la base de Texas -----------------------------------------------------
db_texas = SQLAlchemy(app)

class categorias_texas(db_texas.Model):
    __bind_key__ = 'texas'
    __tablename__ = 'categorias'
    __table_args__ = {"schema": "produccion"}
    idCategoria = db_texas.Column(db_texas.Integer, primary_key=True)
    descripcion = db_texas.Column(db_texas.String(255), nullable = False)

class productos_texas(db_texas.Model):
    __bind_key__ = 'texas'
    __tablename__ = 'productos'
    __table_args__ = {"schema": "produccion"}
    idProducto = db_texas.Column(db_texas.Integer, primary_key=True)
    nomProducto = db_texas.Column(db_texas.String(255), nullable = False)
    idMarca = db_texas.Column(db_texas.Integer, nullable = False)
    idCategoria = db_texas.Column(db_texas.Integer, db_texas.ForeignKey('produccion.categorias.idCategoria'), nullable = False)
    annoModelo = db_texas.Column(db_texas.Integer, nullable = False)
    precioVenta = db_texas.Column(db_texas.Integer, nullable = False)

class clientes_texas(db_texas.Model):
    __bind_key__ = 'texas'
    __tablename__ = 'clientes'
    __table_args__ = {"schema": "ventas"}
    idCliente = db_texas.Column(db_texas.Integer, primary_key=True, autoincrement=True)
    nombre = db_texas.Column(db_texas.String(255), nullable = False)
    apellido = db_texas.Column(db_texas.String(255), nullable = False)
    telefono = db_texas.Column(db_texas.String(25), nullable = True)
    email = db_texas.Column(db_texas.String(255), nullable = False)
    calle = db_texas.Column(db_texas.String(255), nullable = True)
    ciudad = db_texas.Column(db_texas.String(50), nullable = True)
    estado = db_texas.Column(db_texas.String(25), nullable = True)
    codPostal = db_texas.Column(db_texas.String(5), nullable = True)

class detalleOrden_texas(db_texas.Model):
    __bind_key__ = 'texas'
    __tablename__ = 'detalleOrden'
    __table_args__ = {"schema": "ventas"}
    idOrden = db_texas.Column(db_texas.Integer, db_texas.ForeignKey('ventas.ordenes.idOrden'), primary_key=True, nullable = True)
    idItem = db_texas.Column(db_texas.Integer, nullable = True)
    idProducto = db_texas.Column(db_texas.Integer,db_texas.ForeignKey('produccion.productos.idProducto'), primary_key=True, nullable = False)
    cantidad = db_texas.Column(db_texas.Integer, nullable = False)
    precioVenta = db_texas.Column(db_texas.Integer, nullable = False)
    descuento = db_texas.Column(db_texas.Integer, nullable = False, default=0)

class ordenes_texas(db_texas.Model):
    __bind_key__ = 'texas'
    __tablename__ = 'ordenes'
    __table_args__ = {"schema": "ventas"}
    idOrden = db_texas.Column(db_texas.Integer, primary_key=True, autoincrement = False)
    idCliente = db_texas.Column(db_texas.Integer, db_texas.ForeignKey('ventas.clientes.idCliente'), nullable = True)
    estadoOrden = db_texas.Column(db_texas.Integer, nullable = False)
    fechaOrden = db_texas.Column(db_texas.Date, nullable = False)
    required_date = db_texas.Column(db_texas.Date, nullable = False)
    fechaEnvio = db_texas.Column(db_texas.Date, nullable = True)
    idTienda = db_texas.Column(db_texas.Integer, nullable = False)
    idEmpleado = db_texas.Column(db_texas.Integer, nullable = False)

# -------------------------------------- Modelo de la base de New York -----------------------------------------------
db_newyork = SQLAlchemy(app)

class categorias_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'categorias'
    __table_args__ = {"schema": "produccion"}
    idCategoria = db_newyork.Column(db_newyork.Integer, primary_key=True)
    descripcion = db_newyork.Column(db_newyork.String(255), nullable = False)

class marcas_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'marcas'
    __table_args__ = {"schema": "produccion"}
    idMarca = db_newyork.Column(db_newyork.Integer, primary_key=True)
    nomMarca = db_newyork.Column(db_newyork.String(255), nullable = False)

class productos_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'productos'
    __table_args__ = {"schema": "produccion"}
    idProducto = db_newyork.Column(db_newyork.Integer, primary_key=True)
    nomProducto = db_newyork.Column(db_newyork.String(255), nullable = False)
    idMarca = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('produccion.marcas.idMarca'), nullable = False)
    idCategoria = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('produccion.categorias.idCategoria'), nullable = False)
    annoModelo = db_newyork.Column(db_newyork.Integer, nullable = False)
    precioVenta = db_newyork.Column(db_newyork.Integer, nullable = False)

class clientes_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'clientes'
    __table_args__ = {"schema": "ventas"}
    idCliente = db_newyork.Column(db_newyork.Integer, primary_key=True, autoincrement=True)
    nombre = db_newyork.Column(db_newyork.String(255), nullable = False)
    apellido = db_newyork.Column(db_newyork.String(255), nullable = False)
    telefono = db_newyork.Column(db_newyork.String(25), nullable = True)
    email = db_newyork.Column(db_newyork.String(255), nullable = False)
    calle = db_newyork.Column(db_newyork.String(255), nullable = True)
    ciudad = db_newyork.Column(db_newyork.String(50), nullable = True)
    estado = db_newyork.Column(db_newyork.String(25), nullable = True)
    codPostal = db_newyork.Column(db_newyork.String(5), nullable = True)

class tiendas_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'tiendas'
    __table_args__ = {"schema": "ventas"}
    idTienda = db_newyork.Column(db_newyork.Integer, primary_key=True, autoincrement=True)
    nomTienda = db_newyork.Column(db_newyork.String(255), nullable = False)
    telefono = db_newyork.Column(db_newyork.String(25), nullable = True)
    email = db_newyork.Column(db_newyork.String(255), nullable = True)
    calle = db_newyork.Column(db_newyork.String(255), nullable = True)
    ciudad = db_newyork.Column(db_newyork.String(255), nullable = True)
    estado = db_newyork.Column(db_newyork.String(10), nullable = True)
    codPostal = db_newyork.Column(db_newyork.String(5), nullable = True)

class empleados_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'empleados'
    __table_args__ = {"schema": "ventas"}
    idEmpleado = db_newyork.Column(db_newyork.Integer, primary_key=True)
    nombre = db_newyork.Column(db_newyork.String(50), nullable = False)
    apellido = db_newyork.Column(db_newyork.String(50), nullable = False)
    email = db_newyork.Column(db_newyork.String(255), nullable = False, unique=True)
    telefono = db_newyork.Column(db_newyork.String(25), nullable = True)
    activo = db_newyork.Column(db_newyork.Integer, nullable = False)
    idTienda = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('ventas.tiendas.idTienda'), nullable = False)
    idJefe = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('ventas.empleados.idEmpleado'), nullable = True)

class ordenes_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'ordenes'
    __table_args__ = {"schema": "ventas"}
    idOrden = db_newyork.Column(db_newyork.Integer, primary_key=True)
    idCliente = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('ventas.clientes.idCliente'), nullable = True)
    estadoOrden = db_newyork.Column(db_newyork.Integer, nullable = False)
    fechaOrden = db_newyork.Column(db_newyork.Date, nullable = False)
    required_date = db_newyork.Column(db_newyork.Date, nullable = False)
    fechaEnvio = db_newyork.Column(db_newyork.Date, nullable = True)
    idTienda = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('ventas.tiendas.idTienda'), nullable = False)
    idEmpleado = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('ventas.empleados.idEmpleado'), nullable = False)

class detalleOrden_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'detalleOrden'
    __table_args__ = {"schema": "ventas"}
    idOrden = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('ventas.ordenes.idOrden'), primary_key=True, nullable = True)
    idItem = db_newyork.Column(db_newyork.Integer, nullable = True)
    idProducto = db_newyork.Column(db_newyork.Integer,db_newyork.ForeignKey('produccion.productos.idProducto'), primary_key=True, nullable = False)
    cantidad = db_newyork.Column(db_newyork.Integer, nullable = False)
    precioVenta = db_newyork.Column(db_newyork.Integer, nullable = False)
    descuento = db_newyork.Column(db_newyork.Integer, nullable = False, default=0)

class inventario_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'inventario'
    __table_args__ = {"schema": "produccion"}
    idTienda = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('ventas.tiendas.idTienda'),primary_key=True, nullable = True)
    idProducto = db_newyork.Column(db_newyork.Integer, db_newyork.ForeignKey('produccion.productos.idProducto'),primary_key=True, nullable = True)
    cantidad = db_newyork.Column(db_newyork.Integer, nullable = True)

# -------------------------------------------- Lógica del API --------------------------------------------------------
# En esta sección se presentan los web requests necesarios para la página.

# ------------------------- Admin View -------------------------
# Amount earned per store
@app.route('/amount', methods=['GET'])
def get_amount():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    sells = tiendas_newyork.query.join(ordenes_newyork).join(detalleOrden_newyork).with_entities(
        tiendas_newyork.idTienda,
        tiendas_newyork.nomTienda,
        ordenes_newyork.estadoOrden,
        ordenes_newyork.fechaOrden,
        detalleOrden_newyork.precioVenta
    )

    result = []
    for sell in sells:
        new_sell = []
        if sell[2] == 4:
            if startDate <= sell[3] <= endDate:
                new_sell.append(sell[0])
                new_sell.append(sell[1])
                new_sell.append(sell[4])
        if new_sell != []:
            result.append(new_sell)

    indices = []
    for x in result:
        if x[0] not in indices:
            indices.append(x[0])
    
    to_send = []
    for y in indices:
        prepare = []
        temp = []
        for x in result:
            if x[0] == y:
                temp.append(x)
                prepare = x
        valor = 0
        for z in temp:
            valor += z[2]
        prepare[2] = str(valor)
        to_send.append(prepare)

    return jsonify(to_send), 200

# Total sells per product of required store
@app.route('/sells', methods=['GET'])
def get_sells():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()
    store = data["store"]

    ordenes = detalleOrden_newyork.query.join(ordenes_newyork).join(productos_newyork).join(tiendas_newyork).with_entities(
        tiendas_newyork.nomTienda,
        productos_newyork.idProducto,
        productos_newyork.nomProducto,
        ordenes_newyork.estadoOrden,
        ordenes_newyork.fechaOrden,
        detalleOrden_newyork.precioVenta
    )

    result = []
    for order in ordenes:
        new_order = []
        if order[3] == 4:
            if startDate <= order[4] <= endDate:
                if order[0] == store:
                    new_order.append(order[1])      #idProducto
                    new_order.append(order[2])      #nomProducto
                    new_order.append(order[5])      #precioVenta
        if new_order != []:
            result.append(new_order)

    indices = []
    for x in result:
        if x[0] not in indices:
            indices.append(x[0])
    
    to_send = []
    for y in indices:
        prepare = []
        temp = []
        for x in result:
            if x[0] == y:
                temp.append(x)
                prepare = x
        cantidad = len(temp)
        precio = prepare[2]
        prepare = prepare[:len(prepare)-1]
        prepare.append(cantidad)
        prepare.append(str(cantidad*precio))
        to_send.append(prepare)

    return jsonify(to_send), 200

# Store names
@app.route('/stores', methods=['GET'])
def get_stores():

    stores = tiendas_newyork.query.with_entities(
        tiendas_newyork.idTienda,
        tiendas_newyork.nomTienda,
        tiendas_newyork.telefono,
        tiendas_newyork.email,
        tiendas_newyork.calle,
        tiendas_newyork.ciudad,
        tiendas_newyork.estado,
        tiendas_newyork.codPostal
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

    clients = clientes_newyork.query.with_entities(
        clientes_newyork.idCliente,
        clientes_newyork.nombre,
        clientes_newyork.apellido,
        clientes_newyork.telefono,
        clientes_newyork.email,
        clientes_newyork.calle,
        clientes_newyork.ciudad,
        clientes_newyork.estado,
        clientes_newyork.codPostal
    ).all()
    
    result = []

    for client in clients:
        new_client = []

        for data in client:
            new_client.append(data)

        result.append(new_client)

    return jsonify(result), 200


# ------------------------- Store View -------------------------
# Categories
@app.route('/categories/newyork', methods=['GET'])
def get_category_newyork():

    categories = categorias_newyork.query.with_entities(
        categorias_newyork.idCategoria,
        categorias_newyork.descripcion
    ).all()
    
    result = []

    for category in categories:
        new_category = []

        for data in category:
            new_category.append(data)

        result.append(new_category)

    return jsonify(result), 200


@app.route('/categories/texas', methods=['GET'])
def get_category_texas():

    categories = categorias_texas.query.with_entities(
        categorias_texas.idCategoria,
        categorias_texas.descripcion
    ).all()
    
    result = []

    for category in categories:
        new_category = []

        for data in category:
            new_category.append(data)

        result.append(new_category)

    return jsonify(result), 200

@app.route('/categories/california', methods=['GET'])
def get_category_california():

    categories = categorias_california.query.with_entities(
        categorias_california.idCategoria,
        categorias_california.descripcion
    ).all()
    
    result = []

    for category in categories:
        new_category = []

        for data in category:
            new_category.append(data)

        result.append(new_category)

    return jsonify(result), 200


#Total sells of the store

@app.route('/sells/newyork', methods=['GET'])
def get_sells_newyork():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    sells = detalleOrden_newyork.query.join(ordenes_newyork).join(tiendas_newyork).with_entities(
        ordenes_newyork.estadoOrden,
        ordenes_newyork.fechaOrden,
        detalleOrden_newyork.precioVenta,
        tiendas_newyork.estado
    ).all()
    
    result = []
    amount = 0
    for sell in sells:
        if sell[0] == 4:
            if startDate <= sell[1] <= endDate:
                if sell[3] == "NY":
                    amount += sell[2]

    result.append(str(amount))
    result.append(data["startDate"])
    result.append(data["endDate"])

    return jsonify(result), 200

@app.route('/sells/texas', methods=['GET'])
def get_sells_texas():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    sells = detalleOrden_texas.query.join(ordenes_texas).with_entities(
        ordenes_texas.estadoOrden,
        ordenes_texas.fechaOrden,
        detalleOrden_texas.precioVenta,
        ordenes_texas.idOrden
    ).all()
    
    result = []
    amount = 0
    for sell in sells:
        if sell[0] == 4:
            if startDate <= sell[1] <= endDate:
                amount += sell[2]

    result.append(str(amount))
    result.append(data["startDate"])
    result.append(data["endDate"])

    return jsonify(result), 200


@app.route('/sells/california', methods=['GET'])
def get_sells_california():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    sells = detalleOrden_california.query.join(ordenes_california).with_entities(
        ordenes_california.estadoOrden,
        ordenes_california.fechaOrden,
        detalleOrden_california.precioVenta,
        ordenes_california.idOrden
    ).all()
    
    result = []
    amount = 0
    for sell in sells:
        if sell[0] == 4:
            if startDate <= sell[1] <= endDate:
                amount += sell[2]

    result.append(str(amount))
    result.append(data["startDate"])
    result.append(data["endDate"])

    return jsonify(result), 200

# Number of orders per client
@app.route('/orders/client/newyork', methods=['GET'])
def get_orders_clients_newyork():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    clients = ordenes_newyork.query.join(clientes_newyork).join(tiendas_newyork).with_entities(
        clientes_newyork.nombre,
        clientes_newyork.apellido,
        tiendas_newyork.estado,
        clientes_newyork.idCliente,
        ordenes_newyork.idOrden,
        ordenes_newyork.fechaOrden
    ).all()
    
    indices = []
    for client in clients:
        if client[2] == "NY":
            if startDate <= client[5] <= endDate:
                if client[3] not in indices:
                    indices.append(client[3])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        temp = []
        for client in clients:
            if client[3] == y:
                cantidad += 1
                temp = client
        new_result.append(temp[3])
        new_result.append(temp[0]+' '+temp[1])
        new_result.append(cantidad)
        result.append(new_result)
            
    return jsonify(result), 200


@app.route('/orders/client/texas', methods=['GET'])
def get_orders_clients_texas():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    clients = ordenes_texas.query.join(clientes_texas).with_entities(
        clientes_texas.nombre,
        clientes_texas.apellido,
        clientes_texas.idCliente,
        ordenes_texas.idOrden,
        ordenes_texas.fechaOrden
    ).all()
    
    indices = []
    for client in clients:
        if startDate <= client[4] <= endDate:
            if client[2] not in indices:
                indices.append(client[2])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        temp = []
        for client in clients:
            if client[2] == y:
                cantidad += 1
                temp = client
        new_result.append(temp[2])
        new_result.append(temp[0]+' '+temp[1])
        new_result.append(cantidad)
        result.append(new_result)
            
    return jsonify(result), 200


@app.route('/orders/client/california', methods=['GET'])
def get_orders_clients_california():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    clients = ordenes_california.query.join(clientes_california).with_entities(
        clientes_california.nombre,
        clientes_california.apellido,
        clientes_california.idCliente,
        ordenes_california.idOrden,
        ordenes_california.fechaOrden
    ).all()
    
    indices = []
    for client in clients:
        if startDate <= client[4] <= endDate:
            if client[2] not in indices:
                indices.append(client[2])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        temp = []
        for client in clients:
            if client[2] == y:
                cantidad += 1
                temp = client
        new_result.append(temp[2])
        new_result.append(temp[0]+' '+temp[1])
        new_result.append(cantidad)
        result.append(new_result)
            
    return jsonify(result), 200

# Average amount $ bought per client
@app.route('/amount/client/newyork', methods=['GET'])
def get_amount_clients_newyork():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    clients = ordenes_newyork.query.join(clientes_newyork).join(tiendas_newyork).join(detalleOrden_newyork).with_entities(
        clientes_newyork.nombre,
        clientes_newyork.apellido,
        tiendas_newyork.estado,
        clientes_newyork.idCliente,
        ordenes_newyork.idOrden,
        detalleOrden_newyork.precioVenta,
        ordenes_newyork.estadoOrden,
        ordenes_newyork.fechaOrden
    ).all()
    
    indices = []
    for client in clients:
        if startDate <= client[7] <= endDate:
            if client[6] == 4:
                if client[2] == "NY":
                    if client[3] not in indices:
                        indices.append(client[3])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        temp = []
        for client in clients:
            if client[3] == y:
                cantidad += client[5]
                temp = client
        new_result.append(temp[3])
        new_result.append(temp[0]+' '+temp[1])
        new_result.append(str(cantidad))
        result.append(new_result)
            
    return jsonify(result), 200

@app.route('/amount/client/texas', methods=['GET'])
def get_amount_clients_texas():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    clients = ordenes_texas.query.join(clientes_texas).join(detalleOrden_texas).with_entities(
        clientes_texas.nombre,
        clientes_texas.apellido,
        clientes_texas.idCliente,
        ordenes_texas.idOrden,
        detalleOrden_texas.precioVenta,
        ordenes_texas.estadoOrden,
        ordenes_texas.fechaOrden
    ).all()
    
    indices = []
    for client in clients:
        if client[5] == 4:
            if startDate <= client[6] <= endDate:
                if client[2] not in indices:
                    indices.append(client[2])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        temp = []
        for client in clients:
            if client[2] == y:
                cantidad += client[4]
                temp = client
        new_result.append(temp[2])
        new_result.append(temp[0]+' '+temp[1])
        new_result.append(str(cantidad))
        result.append(new_result)
            
    return jsonify(result), 200


@app.route('/amount/client/california', methods=['GET'])
def get_amount_clients_california():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    clients = ordenes_california.query.join(clientes_california).join(detalleOrden_california).with_entities(
        clientes_california.nombre,
        clientes_california.apellido,
        clientes_california.idCliente,
        ordenes_california.idOrden,
        detalleOrden_california.precioVenta,
        ordenes_california.estadoOrden,
        ordenes_california.fechaOrden
    ).all()
    
    indices = []
    for client in clients:
        if client[5] == 4:
            if startDate <= client[6] <= endDate:
                if client[2] not in indices:
                    indices.append(client[2])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        temp = []
        for client in clients:
            if client[2] == y:
                cantidad += client[4]
                temp = client
        new_result.append(temp[2])
        new_result.append(temp[0]+' '+temp[1])
        new_result.append(str(cantidad))
        result.append(new_result)
            
    return jsonify(result), 200


# Total sells per product by category
@app.route('/sells/category/newyork', methods=['GET'])
def get_sells_category_newyork():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    products = detalleOrden_newyork.query.join(productos_newyork).join(ordenes_newyork).join(tiendas_newyork).with_entities(
        productos_newyork.idProducto,
        productos_newyork.nomProducto,
        tiendas_newyork.estado,
        detalleOrden_newyork.precioVenta,
        ordenes_newyork.estadoOrden,
        ordenes_newyork.fechaOrden
    ).all()
    
    indices = []
    for product in products:
        if startDate <= product[5] <= endDate:
            if product[4] == 4:
                if product[2] == "NY":
                    if product[0] not in indices:
                        indices.append(product[0])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        venta = 0
        temp = []
        for product in products:
            if product[0] == y:
                venta += product[3]
                cantidad += 1
                temp = product
        new_result.append(temp[0])
        new_result.append(temp[1])
        new_result.append(cantidad)
        new_result.append(str(venta))
        result.append(new_result)
            
    return jsonify(result), 200


@app.route('/sells/category/texas', methods=['GET'])
def get_sells_category_texas():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    products = detalleOrden_texas.query.join(productos_texas).join(ordenes_texas).with_entities(
        productos_texas.idProducto,
        productos_texas.nomProducto,
        detalleOrden_texas.precioVenta,
        ordenes_texas.estadoOrden,
        ordenes_texas.fechaOrden
    ).all()

    indices = []
    for product in products:
        if startDate <= product[4] <= endDate:
            if product[3] == 4:
                if product[0] not in indices:
                    indices.append(product[0])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        venta = 0
        temp = []
        for product in products:
            if product[0] == y:
                venta += product[2]
                cantidad += 1
                temp = product
        new_result.append(temp[0])
        new_result.append(temp[1])
        new_result.append(cantidad)
        new_result.append(str(venta))
        result.append(new_result)
            
    return jsonify(result), 200


@app.route('/sells/category/california', methods=['GET'])
def get_sells_category_california():

    data = request.get_json()
    startDate = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d').date()

    products = detalleOrden_california.query.join(productos_california).join(ordenes_california).with_entities(
        productos_california.idProducto,
        productos_california.nomProducto,
        detalleOrden_california.precioVenta,
        ordenes_california.estadoOrden,
        ordenes_california.fechaOrden
    ).all()

    indices = []
    for product in products:
        if startDate <= product[4] <= endDate:
            if product[3] == 4:
                if product[0] not in indices:
                    indices.append(product[0])

    result = [] 
    for y in indices:
        new_result = []
        cantidad = 0
        venta = 0
        temp = []
        for product in products:
            if product[0] == y:
                venta += product[2]
                cantidad += 1
                temp = product
        new_result.append(temp[0])
        new_result.append(temp[1])
        new_result.append(cantidad)
        new_result.append(str(venta))
        result.append(new_result)
            
    return jsonify(result), 200


# Products of a store
@app.route('/productos', methods=['GET'])
def get_productos():

    data = request.get_json()
    result = []
    
    if data["storeName"] == "newyork":
        productos = productos_newyork.query.with_entities(
            productos_newyork.nomProducto,
            productos_newyork.precioVenta,
        ).all()

        for producto in productos:
            new_producto = []
            new_producto.append(producto[0])
            new_producto.append(float(producto[1]))
            result.append(new_producto)

    if data["storeName"] == "texas":
        productos = productos_texas.query.with_entities(
            productos_texas.nomProducto,
            productos_texas.precioVenta,
        ).all()

        for producto in productos:
            new_producto = []
            new_producto.append(producto[0])
            new_producto.append(float(producto[1]))
            result.append(new_producto)

    if data["storeName"] == "california":
        productos = productos_california.query.with_entities(
            productos_california.nomProducto,
            productos_california.precioVenta,
        ).all()

        for producto in productos:
            new_producto = []
            new_producto.append(producto[0])
            new_producto.append(float(producto[1]))
            result.append(new_producto)

    return jsonify(result), 200

# Insert new Order
@app.route('/order', methods=['POST'])
def create_order():
    
    data = request.get_json()

    store = tiendas_newyork.query.filter(tiendas_newyork.nomTienda.like(data["storeName"])).first()

    ordenes = ordenes_newyork.query.with_entities(
        ordenes_newyork.idOrden
    )
    new_id = 0
    for orden in ordenes:
        new_id += 1
    new_id = new_id + 2

    print(new_id)

    new_order = ordenes_newyork(
        idOrden = new_id,
        idCliente = data["clientId"],
        estadoOrden = 1,
        fechaOrden = data["orderDate"],
        required_date = data["requiredDate"],
        fechaEnvio = None,
        idTienda = store.idTienda,
        idEmpleado = data["employeeId"]
    ) 
    db_newyork.session.add(new_order)
    db_newyork.session.commit()

    product = productos_newyork.query.filter(productos_newyork.nomProducto.like(data["productName"])).first()

    new_detail_order = detalleOrden_newyork(
        idOrden = new_id,
        idItem = 1,
        idProducto = product.idProducto,
        cantidad = data["quantity"],
        precioVenta = product.precioVenta,
        descuento = 0,
    )

    db_newyork.session.add(new_detail_order)
    db_newyork.session.commit()

    if data["storeName"] == "Santa Cruz Bikes":

        store = tiendas_newyork.query.filter(tiendas_newyork.nomTienda.like(data["storeName"])).first()

        new_order = ordenes_california(
            idOrden = new_id,
            idCliente = data["clientId"],
            estadoOrden = 1,
            fechaOrden = data["orderDate"],
            required_date = data["requiredDate"],
            fechaEnvio = None,
            idTienda = store.idTienda,
            idEmpleado = data["employeeId"]
        ) 
        db_california.session.add(new_order)
        db_california.session.commit()

        product = productos_california.query.filter(productos_california.nomProducto.like(data["productName"])).first()

        new_detail_order = detalleOrden_california(
            idOrden = new_id,
            idItem = 1,
            idProducto = product.idProducto,
            cantidad = data["quantity"],
            precioVenta = product.precioVenta,
            descuento = 0,
        )

        db_california.session.add(new_detail_order)
        db_california.session.commit()

    if data["storeName"] == "Rowlett Bikes":

        store = tiendas_newyork.query.filter(tiendas_newyork.nomTienda.like(data["storeName"])).first()

        new_order = ordenes_texas(
            idOrden = new_id,
            idCliente = data["clientId"],
            estadoOrden = 1,
            fechaOrden = data["orderDate"],
            required_date = data["requiredDate"],
            fechaEnvio = None,
            idTienda = store.idTienda,
            idEmpleado = data["employeeId"]
        ) 
        db_texas.session.add(new_order)
        db_texas.session.commit()

        product = productos_texas.query.filter(productos_texas.nomProducto.like(data["productName"])).first()

        new_detail_order = detalleOrden_texas(
            idOrden = new_id,
            idItem = 1,
            idProducto = product.idProducto,
            cantidad = data["quantity"],
            precioVenta = product.precioVenta,
            descuento = 0,
        )

        db_texas.session.add(new_detail_order)
        db_texas.session.commit()

    response = jsonify({'message' : 'New order created!'})
    return response

#----------------------------- Run  ----------------------------
if __name__ == "__main__":
    app.run(debug=True)