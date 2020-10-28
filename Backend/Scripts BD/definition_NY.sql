create database NewYork;

Use NewYork
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

CREATE TABLE produccion.marcas (
	idMarca INT IDENTITY(1,1) PRIMARY KEY,
	nomMarca VARCHAR (255) NOT NULL
);

CREATE TABLE produccion.productos (
	idProducto INT IDENTITY(1,1) PRIMARY KEY,
	nomProducto VARCHAR (255) NOT NULL,
	idMarca INT NOT NULL,
	idCategoria INT NOT NULL,
	annoModelo SMALLINT NOT NULL,
	precioVenta DECIMAL (10, 2) NOT NULL,
	FOREIGN KEY (idCategoria) REFERENCES produccion.categorias (idCategoria) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (idMarca) REFERENCES produccion.marcas (idMarca) ON DELETE CASCADE ON UPDATE CASCADE
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

CREATE TABLE ventas.tiendas (
	idTienda INT IDENTITY(1,1) PRIMARY KEY,
	nomTienda VARCHAR (255) NOT NULL,
	telefono VARCHAR (25),
	email VARCHAR (255),
	calle VARCHAR (255),
	ciudad VARCHAR (255),
	estado VARCHAR (10),
	codPostal VARCHAR (5)
);

CREATE TABLE ventas.empleados (
	idEmpleado INT IDENTITY(1,1) PRIMARY KEY,
	nombre VARCHAR (50) NOT NULL,
	apellido VARCHAR (50) NOT NULL,
	email VARCHAR (255) NOT NULL UNIQUE,
	telefono VARCHAR (25),
	activo tinyint NOT NULL,
	idTienda INT NOT NULL,
	idJefe INT,
	FOREIGN KEY (idTienda) REFERENCES ventas.tiendas (idTienda) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (idJefe) REFERENCES ventas.empleados (idEmpleado) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE ventas.ordenes (
	idOrden INT IDENTITY(1,1) PRIMARY KEY,
	idCliente INT,
	estadoOrden tinyint NOT NULL,
	-- Order status: 1 = Pending; 2 = Processing; 3 = Rejected; 4 = Completed
	fechaOrden DATE NOT NULL,
	required_date DATE NOT NULL,
	fechaEnvio DATE,
	idTienda INT NOT NULL,
	idEmpleado INT NOT NULL,
	FOREIGN KEY (idCliente) REFERENCES ventas.clientes (idCliente) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (idTienda) REFERENCES ventas.tiendas (idTienda) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (idEmpleado) REFERENCES ventas.empleados (idEmpleado) ON DELETE NO ACTION ON UPDATE NO ACTION
);

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

CREATE TABLE produccion.inventario (
	idTienda INT,
	idProducto INT,
	cantidad INT,
	PRIMARY KEY (idTienda, idProducto),
	FOREIGN KEY (idTienda) REFERENCES ventas.tiendas (idTienda) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (idProducto) REFERENCES produccion.productos (idProducto) ON DELETE CASCADE ON UPDATE CASCADE
);