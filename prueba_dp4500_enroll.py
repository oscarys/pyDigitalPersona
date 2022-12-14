#!/usr/bin/python3

import os
import sys
import gi
import matplotlib.pyplot as plt
import numpy as np

# Directorios relevantes para acceder a la biblioteca
BUILDDIR='/home/pi/Desktop/INCICH/libfprint/bin'
LIBRARYPATH = BUILDDIR + '/libfprint/'
TYPELIBPATH = BUILDDIR + '/libfprint/'

# Truco para ejecutar el programa con las variables de entorno correctas
if 'RUNNING' not in os.environ:
	if 'LD_LIBRARY_PATH' not in os.environ:
		os.environ['LD_LIBRARY_PATH'] = LIBRARYPATH
	else:
		os.environ['LD_LIBRARY_PATH'] += ':' + LIBRARYPATH
	os.environ['GI_TYPELIB_PATH'] = TYPELIBPATH
	os.environ['FP_DEVICE_EMULATION'] = '1'
	os.environ['RUNNING'] = 'True'
	# Aquí el relanzamiento del programa
	os.execv(sys.argv[0], sys.argv)

# Levanta la interfaz GObject para la biblioteca libfprint
gi.require_version('FPrint', '2.0')
from gi.repository import FPrint, GLib

# Crea el contexto de la biblioteca y escanea por sensores
context = FPrint.Context()
context.enumerate()
devices = context.get_devices()

# Debe haber un solo sensor para este programa
if len(devices) > 1:
	raise ValueError('solo un dispositivo puede estar conectado')
if len(devices) == 0:
	raise ValueError('no hay dispositivo conectado')

# Recupera el sensor	
device = devices[0]

print(f'Número de pasos de enrollment: {device.get_nr_enroll_stages()}')
features = device.get_features()
print('Capacidades: ')
for feature in device.get_features().value_names:
	print(feature)

# Prepara un templete para el registro
fp = FPrint.Print.new(device)
fp.set_username('Oscar Yáñez Suárez')
fp.set_finger(FPrint.Finger.RIGHT_INDEX)
fp.set_description('Prueba de registro de huella')
fp.set_enroll_date(GLib.Date.new_dmy(day=1, month=1, year=2022))


print('PRE ' + '*'*20)
print(f'Driver: {fp.get_driver()}')
print(f'Device ID: {fp.get_device_id()}')
print(f'Device stored: {fp.get_device_stored()}')
print(f'Image: {fp.get_image()}')
print(f'Finger: {fp.get_finger()}')
print(f'Username: {fp.get_username()}')
print(f'Description: {fp.get_description()}')
date = fp.get_enroll_date()
print(f'Enroll date: {date.year}:{date.month}:{date.day}')
print(f'Compatible: {fp.compatible(device)}')
print('*'*20)

def enroll_cb(*args):
	print(f'Huella {args[1]}')
	
device.open_sync()
fp = device.enroll_sync(fp, progress_cb=enroll_cb)
if fp is not None:
	device.close_sync()

#print('POST ' + '*'*20)
#print(f'Driver: {fp.get_driver()}')
#print(f'Device ID: {fp.get_device_id()}')
#print(f'Device stored: {fp.get_device_stored()}')
#print(f'Image: {fp.get_image()}')
#print(f'Finger: {fp.get_finger()}')
#print(f'Username: {fp.get_username()}')
#print(f'Description: {fp.get_description()}')
#print(f'Enroll date: {fp.get_enroll_date()}')
#print(f'Compatible: {fp.compatible(device)}')
#print('*'*20)

# Cierra el dispositivo y el contexto de la biblioteca
#del device
#del context

