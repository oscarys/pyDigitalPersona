#!/usr/bin/env python

import os
import sys
import pyfprint

# Carpeta que almacena huellas
PRINTSPATH = './prints/'

# Asegura que hay usuario en la linea de comandos
if len(sys.argv) != 2:
    raise ValueError(f'{sys.argv[0]} "nombre de usuario"')

# Calcula el hash para el usuario y verifica que exista su carpeta
hash_usuario = sum(index * ord(character) for index, character in enumerate(sys.argv[1], start=1))
if not os.path.exists(f'{PRINTSPATH}{hash_usuario}'):
    raise ValueError(f'El usuario {sys.argv[1]} no está en el sistema')

# Inicializando el manejador
pyfprint.fp_init()

# Busca dispositivos
devices = pyfprint.discover_devices()
if len(devices) == 0:
    raise ValueError('No hay dispositivos lectores disponibles')
elif len(devices) > 1:
    raise ValueError('Solo puede haber un lector conectado') 
    
# Recupera y activa el dispositivo conectado
device = devices[0]
device.open()

# Recupera huella del disco
with open(f'{PRINTSPATH}{hash_usuario}/{pyfprint.Fingers["RIGHT_INDEX"]}.bin', 'rb') as f:
    rdata = f.read().decode('utf-8', 'surrogateescape')
#    fprint = pyfprint.Fprint(serial_data=data)
fprint = device.load_print_from_disk(pyfprint.Fingers['RIGHT_INDEX'])
print(fprint.data()==rdata)

# Verifica huella y anuncia resultado
verified, img = device.verify_finger(fprint)
if verified:
    print(f'{sys.argv[1]} OK')
else:
    print(f'{sys.argv[1]} NO COINCIDE')

# Detiene dispositivo
device.close()

# Detiene al manejador
pyfprint.fp_exit()

