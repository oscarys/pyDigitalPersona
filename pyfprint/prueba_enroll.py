#!/usr/bin/env python

import os
import sys
import io
import pyfprint

# Carpeta que almacena huellas
PRINTSPATH = './prints/'

# Asegura que hay usuario en la linea de comandos
if len(sys.argv) != 2:
    raise ValueError(f'{sys.argv[0]} "nombre de usuario"')

# Calcula el hash para el usuario y crea su carpeta
hash_usuario = sum(index * ord(character) for index, character in enumerate(sys.argv[1], start=1))
if not os.path.exists(f'{PRINTSPATH}{hash_usuario}'):
    os.mkdir(f'{PRINTSPATH}{hash_usuario}')

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

# Recupera el número de scans para enrollment
enrollments = device.nr_enroll_stages()

# Enrollment
print(f'Debes escanear tu dedo INDICE DERECHO {enrollments} veces')
fprint, img = device.enroll_finger()

# Almacena la información
if fprint is not None:
    # Guarda huella
    fprint.save_to_disk(pyfprint.Fingers['RIGHT_INDEX']) # OJO: OBSOLETA
    with open(f'{PRINTSPATH}{hash_usuario}/{pyfprint.Fingers["RIGHT_INDEX"]}.bin', 'wb') as f:
        f.write(fprint.data().encode(encoding='utf-8', errors='surrogateescape'))
if img is not None:
    # Guarda imagen
    img.save_to_file(f'{PRINTSPATH}{hash_usuario}/{pyfprint.Fingers["RIGHT_INDEX"]}.pgm')
    
# Detiene dispositivo
device.close()

# Detiene al manejador
pyfprint.fp_exit()
