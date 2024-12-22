# Script para implementar funcionamiento de subprocess lanzado en script principal
# Fecha: 20/12/2024

import sys
# módulo para verificar si un path existe
from pathlib import Path

# Módulo para bajer productos S2
sys.path.append(r'../utils')
import mod_dloader as mdl

# Para implementar funciones de snappy en módulo
import mod_snappy_S2 as msnap

# Conversión de argumentos
conf_dict_path = eval(sys.argv[1])
# develpment = bool(eval(sys.argv[2]))
# print(sys.argv[2])

# print(conf_dict_path, type(conf_dict_path), conf_dict_path['config'], sep = '\n')

conf_dict = msnap.read_conf_proc(conf_dict_path['config'], False)
print('Lectura de archivo de configuración correcta')

# root_folder = Path(conf_dict['FOLDERS']['output'])
# if development:
#     msnap.del_folder(root_folder, True)
# print(f'Apertura de carpeta de salida: {root_folder}')