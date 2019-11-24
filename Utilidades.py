# -*- encoding: utf-8 -*-
import random
import string
import AccesoArchivo
from decimal import Decimal

def ValidarSoloNumeros(key):
	"""
	Función para validar que lo que ingresa el usuario es numero
	"""
	r = True
	try:
		key = int(key)
	except Exception as ex:
		r = False

	return r

def ValidarSoloDecimal(key):
	"""
	Función para validar que lo que ingresa el usuario es numero
	"""	
	r = True
	try:
		key = Decimal(key)
	except Exception as ex:
		r = False

	return r

def ValidarSoloLetras(key):
	"""
	Función para validar que lo que ingresa el usuario es letra
	"""
	key = str(key)
	if key.isalpha():
		print('es alpha')
		print(key)
		return True
	else:
		return False

def ValidarCamposVentas(formulario):
	r = True
	mensaje = ''
	vacio = ''
	coma = ', '
	Cliente = 'Cliente (solo letras)'
	Producto = 'Producto (solo letras)'
	Cantidad = 'Cantidad (solo números)'
	Precio = 'Precio (solo números)'

	try:
		if not ValidarSoloLetras(formulario.txtCliente.data):
			mensaje = Cliente if (mensaje == vacio) else mensaje + coma + Cliente
		if not ValidarSoloLetras(formulario.txtProducto.data):
			mensaje = Producto if (mensaje == vacio) else mensaje + coma + Producto
		if not ValidarSoloNumeros(formulario.txtCantidad.data):
			mensaje = Cantidad if (mensaje == vacio) else mensaje + coma + Cantidad
		if not ValidarSoloNumeros(formulario.txtPrecio.data):
			mensaje = Precio if (mensaje == vacio) else mensaje + coma + Precio
		if not mensaje == vacio:
			mensaje = 'Debe verificar lo siguiente:\n' + mensaje
			r = False
	except Exception as e:
		r = False

	return r, mensaje

def GenerarCodigoVenta():
	letrasCodigo = ''.join(random.choice(string.ascii_uppercase) for i in range(3))
	numerosCodigo = str(random.randint(000, 999))
	codigo = letrasCodigo + numerosCodigo
	while not VerificarCodigoVenta(codigo):
		letrasCodigo = ''.join(random.choice(string.ascii_uppercase) for i in range(3))
		numerosCodigo = str(random.randint(000, 999))

	return codigo

def VerificarCodigoVenta(codigo):
	ventas = AccesoArchivo.AbrirArchivoCSV('Ventas.csv')
	r = True
	for item in ventas:
		if item["CODIGO"] == codigo:
			r = False
	
	return r