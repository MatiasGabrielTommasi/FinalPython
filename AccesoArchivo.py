# -*- encoding: utf-8 -*-
import csv

def AbrirArchivoCSV(strArchivo):
	"""
	Función para abrir archivos csv, se para la ruta como parametro,
	tomando como directorio raiz la ubicacion del archivo "AccesoArchivo.py"
	"""
	try:
		r = []
		with open(strArchivo, 'r', encoding='utf-8') as archivo2:
			archivo_csv = csv.DictReader(archivo2)
			#lon = len(archivo_csv)
			#if lon > 0:
			for item in archivo_csv:
				r.append(item)
	except FileNotFoundError as ex:
		raise Exception('No se encontró el archivo')
	except Exception as e:
		raise Exception('Problema al procesar el archivo. ' + strArchivo)	

	return r

def GuardarRegistroCSV(strArchivo, registro):
	"""
	Función para agregar un registro en archivos csv, se para la ruta como parametro,
	tomando como directorio raiz la ubicacion del archivo 'AccesoArchivo.py'
	"""
	print('GuardarRegistroCSV')
	print(registro)
	r = True
	mensaje = "Se registró la venta exitosamente."
	inicio = len(AbrirArchivoCSV(strArchivo))
	fin = 0
	try:
		with open(strArchivo, 'a+') as archivo:
			archivo_csv = csv.writer(archivo)
			archivo_csv.writerow(registro)
		
		fin = len(AbrirArchivoCSV(strArchivo))
		if inicio == fin:
			r = False
			mensaje = "No fue posible registrar la operación, vuelva a intentarlo en breve."
	except Exception as e:
		mensaje = 'Error inesperado al guardar el registro, ' + str(e)

	return r, mensaje

def ValidarUsuarioNuevo(registro):
	"""
	Función para validar si el usuario existe
	"""
	try:
		r = True
		listado = []
		usuarios = AbrirArchivoCSV('usuarios.csv')
		for item in usuarios:
			if registro[0] == item['Usuario']:
				r = False
				break
	except Exception as e:
		raise Exception('Problemas al validar el usuario.')

	return r