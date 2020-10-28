use NewYork

insert into [157.55.196.141].Texas.ventas.ordenes
	select idOrden, idCliente, estadoOrden, fechaOrden, required_date, fechaEnvio, ventas.ordenes.idTienda, idEmpleado
		from ventas.ordenes inner join ventas.tiendas 
		on ventas.ordenes.idTienda = ventas.tiendas.idTienda
		where ventas.ordenes.idTienda = (select idTienda from ventas.tiendas where ventas.tiendas.nomTienda = 'Rowlett Bikes');

insert into [157.55.196.141].Texas.ventas.detalleOrden
	select ventas.detalleOrden.idOrden, idItem, idProducto, cantidad, precioVenta, descuento
		from ventas.detalleOrden inner join ventas.ordenes
		on ventas.detalleOrden.idOrden = ventas.ordenes.idOrden
		where ventas.ordenes.idTienda = (select idTienda from ventas.tiendas where ventas.tiendas.nomTienda = 'Rowlett Bikes');