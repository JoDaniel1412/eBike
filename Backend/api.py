from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_cors import CORS, cross_origin
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://crisptofer12ff:*cristofer12ff*@13.66.5.40/NewYork?driver=SQL Server Native Client 11.0"
app.config['SQLALCHEMY_BINDS'] = {
    'newyork':      "mssql+pyodbc://crisptofer12ff:*cristofer12ff*@13.66.5.40/NewYork?driver=SQL Server Native Client 11.0",
    'texas':        "mssql+pyodbc://crisptofer12ff:*cristofer12ff*@157.55.196.141/Texas?driver=SQL Server Native Client 11.0",
    'california':   "mssql+pyodbc://ezuniga97:@Esteban1497@13.85.159.205/California?driver=SQL Server Native Client 11.0"
}
#app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://crisptofer12ff:*cristofer12ff*@157.55.196.141/Texas?driver=SQL Server Native Client 11.0"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://ezuniga97:@Esteban1497@13.85.159.205/California?driver=SQL Server Native Client 11.0"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db_california = SQLAlchemy(app)

class categorias_california(db_california.Model):
    __bind_key__ = 'california'
    __tablename__ = 'categorias'
    __table_args__ = {"schema": "produccion"}
    idCategoria = db_california.Column(db_california.Integer, primary_key=True)
    descripcion = db_california.Column(db_california.String(255), nullable = False)

db_texas = SQLAlchemy(app)

class categorias_texas(db_texas.Model):
    __bind_key__ = 'texas'
    __tablename__ = 'categorias'
    __table_args__ = {"schema": "produccion"}
    idCategoria = db_texas.Column(db_texas.Integer, primary_key=True)
    descripcion = db_texas.Column(db_texas.String(255), nullable = False)

db_newyork = SQLAlchemy(app)

class categorias_newyork(db_newyork.Model):
    __bind_key__ = 'newyork'
    __tablename__ = 'categorias'
    __table_args__ = {"schema": "produccion"}
    idCategoria = db_newyork.Column(db_newyork.Integer, primary_key=True)
    descripcion = db_newyork.Column(db_newyork.String(255), nullable = False)

#----------------------------- Admin View ----------------------------

# Categories
@app.route('/categories', methods=['GET'])
def get_category():
    print("RACSO")

    categories = categorias_newyork(__bind_key__ = 'newyork').query.with_entities(
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

# Categories
@app.route('/este', methods=['GET'])
def get_este():
    print("RACSO")

    categories = categorias_california(__bind_key__ = 'california').query.with_entities(
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

#----------------------------- Run  ----------------------------

if __name__ == "__main__":
    app.run(debug=True)