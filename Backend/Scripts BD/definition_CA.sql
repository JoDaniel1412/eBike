create database California;

Use California
-- create schemas
CREATE SCHEMA produccion
GO
CREATE SCHEMA ventas
GO

-- create tables
CREATE TABLE produccion.categorias (
	idCategoria INT IDENTITY(1,1)  PRIMARY KEY,
	descripcion VARCHAR (255) NOT NULL
);

CREATE TABLE produccion.productos (
	idProducto INT IDENTITY(1,1) PRIMARY KEY,
	nomProducto VARCHAR (255) NOT NULL,
	idMarca INT NOT NULL,
	idCategoria INT NOT NULL,
	annoModelo SMALLINT NOT NULL,
	precioVenta DECIMAL (10, 2) NOT NULL,
	FOREIGN KEY (idCategoria) REFERENCES produccion.categorias (idCategoria) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ventas.clientes (
	idCliente INT IDENTITY(1,1) PRIMARY KEY,
	nombre VARCHAR (255) NOT NULL,
	apellido VARCHAR (255) NOT NULL,
	telefono VARCHAR (25),
	email VARCHAR (255) NOT NULL,
	calle VARCHAR (255),
	ciudad VARCHAR (50),
	estado VARCHAR (25),
	codPostal VARCHAR (5)
);

-- Se queda
CREATE TABLE ventas.ordenes (
	idOrden INT PRIMARY KEY,
	idCliente INT,
	estadoOrden tinyint NOT NULL,
	-- Order status: 1 = Pending; 2 = Processing; 3 = Rejected; 4 = Completed
	fechaOrden DATE NOT NULL,
	required_date DATE NOT NULL,
	fechaEnvio DATE,
	idTienda INT NOT NULL,
	idEmpleado INT NOT NULL,
	FOREIGN KEY (idCliente) REFERENCES ventas.clientes (idCliente) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Se queda --
CREATE TABLE ventas.detalleOrden (
	idOrden INT,
	idItem INT,
	idProducto INT NOT NULL,
	cantidad INT NOT NULL,
	precioVenta DECIMAL (10, 2) NOT NULL,
	descuento DECIMAL (4, 2) NOT NULL DEFAULT 0,
	PRIMARY KEY (idOrden, idItem),
	FOREIGN KEY (idOrden) REFERENCES ventas.ordenes (idOrden) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (idProducto) REFERENCES produccion.productos (idProducto) ON DELETE CASCADE ON UPDATE CASCADE
);