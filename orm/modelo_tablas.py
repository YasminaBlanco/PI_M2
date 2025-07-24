from sqlalchemy import (Column, 
                        Integer, 
                        String, 
                        DateTime, 
                        ForeignKey, 
                        Numeric, 
                        Text, 
                        func)

from sqlalchemy.orm import relationship
from db_conector import Base

# Tabla usuarios
class Usuarios(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    dni = Column(String(20), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    contraseña = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=func.now())

    ordenes = relationship('Ordenes', back_populates='usuario')
    direcciones = relationship('DireccionesEnvio', back_populates='usuario')
    carrito = relationship('Carrito', back_populates='usuario')
    reseñas = relationship('ReseñasProductos', back_populates='usuario')

# Tabla categorias
class Categorias(Base):
    __tablename__ = 'categorias'

    categoria_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255))

    productos = relationship('Productos', back_populates='categoria')

# Tabla productos
class Productos(Base):
    __tablename__ = 'productos'

    producto_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.categoria_id'))

    categoria = relationship('Categorias', back_populates='productos')
    detalle_ordenes = relationship('DetalleOrdenes', back_populates='producto')
    carrito = relationship('Carrito', back_populates='producto')
    reseñas = relationship('ReseñasProductos', back_populates='producto')

# Tabla ordenes
class Ordenes(Base):
    __tablename__ = 'ordenes'

    orden_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    fecha_orden = Column(DateTime, default=func.now())
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(50), default='Pendiente')

    usuario = relationship('Usuarios', back_populates='ordenes')
    detalles = relationship('DetalleOrdenes', back_populates='orden')
    pagos = relationship('OrdenesMetodosPago', back_populates='orden')
    historial_pagos = relationship('HistorialPagos', back_populates='orden')

# Tabla detalle_ordenes
class DetalleOrdenes(Base):
    __tablename__ = 'detalle_ordenes'

    detalle_id = Column(Integer, primary_key=True, autoincrement=True)
    orden_id = Column(Integer, ForeignKey('ordenes.orden_id'))
    producto_id = Column(Integer, ForeignKey('productos.producto_id'))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    orden = relationship('Ordenes', back_populates='detalles')
    producto = relationship('Productos', back_populates='detalle_ordenes')

# Tabla direcciones_envio
class DireccionesEnvio(Base):
    __tablename__ = 'direcciones_envio'

    direccion_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    calle = Column(String(255), nullable=False)
    ciudad = Column(String(100), nullable=False)
    departamento = Column(String(100))
    provincia = Column(String(100))
    distrito = Column(String(100))
    estado = Column(String(100))
    codigo_postal = Column(String(20))
    pais = Column(String(100), nullable=False)

    usuario = relationship('Usuarios', back_populates='direcciones')

# Tabla carrito
class Carrito(Base):
    __tablename__ = 'carrito'

    carrito_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    producto_id = Column(Integer, ForeignKey('productos.producto_id'))
    cantidad = Column(Integer, nullable=False)
    fecha_agregado = Column(DateTime, default=func.now())

    usuario = relationship('Usuarios', back_populates='carrito')
    producto = relationship('Productos', back_populates='carrito')

# Tabla metodos_pago
class MetodosPago(Base):
    __tablename__ = 'metodos_pago'

    metodo_pago_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))

    ordenes_pago = relationship('OrdenesMetodosPago', back_populates='metodo_pago')
    historial_pagos = relationship('HistorialPagos', back_populates='metodo_pago')

# Tabla ordenes_metodos_pago
class OrdenesMetodosPago(Base):
    __tablename__ = 'ordenes_metodos_pago'

    orden_metodo_id = Column(Integer, primary_key=True, autoincrement=True)
    orden_id = Column(Integer, ForeignKey('ordenes.orden_id'))
    metodo_pago_id = Column(Integer, ForeignKey('metodos_pago.metodo_pago_id'))
    monto_pagado = Column(Numeric(10, 2), nullable=False)

    orden = relationship('Ordenes', back_populates='pagos')
    metodo_pago = relationship('MetodosPago', back_populates='ordenes_pago')

# Tabla reseñas_productos
class ReseñasProductos(Base):
    __tablename__ = 'reseñas_productos'

    reseña_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    producto_id = Column(Integer, ForeignKey('productos.producto_id'))
    calificacion = Column(Integer, nullable=False)
    comentario = Column(Text)
    fecha = Column(DateTime, default=func.now())

    usuario = relationship('Usuarios', back_populates='reseñas')
    producto = relationship('Productos', back_populates='reseñas')

# Tabla historial_pagos
class HistorialPagos(Base):
    __tablename__ = 'historial_pagos'

    pago_id = Column(Integer, primary_key=True, autoincrement=True)
    orden_id = Column(Integer, ForeignKey('ordenes.orden_id'))
    metodo_pago_id = Column(Integer, ForeignKey('metodos_pago.metodo_pago_id'))
    monto = Column(Numeric(10, 2), nullable=False)
    fecha_pago = Column(DateTime, default=func.now())
    estado_pago = Column(String(50), default='Procesando')

    orden = relationship('Ordenes', back_populates='historial_pagos')
    metodo_pago = relationship('MetodosPago', back_populates='historial_pagos')
