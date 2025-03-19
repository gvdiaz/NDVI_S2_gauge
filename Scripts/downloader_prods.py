# Script para bajar productos de a uno, paso el nombre del producto por argumento
# Fecha: 04/03/2025

# Módulo para ingresar módulo desarrollado sin importar snappy (para hacerlo más liviano)
import sys
# Módulo para función 1B
# módulo para verificar si un path existe
from pathlib import Path

# Módulo para guardar lista de productos a bajar
import os

# Módulo con funciones desarrolladas.
# Módulo para bajer productos S2
sys.path.append(r'../utils')
import mod_s_snappy_p3_6 as mfc

# Funciones que necesito implementar

# Cuerpo de script a ejecutar
# Parte 2da
# Tengo definido ruta a archivo de configación del procesador general.
config_path = r'/src/utils/CONF_PROC.INI'
development = True
verbose2conf = False

# Función 1A
# Lectura de archivo de configuración de búsqueda
conf_dict = mfc.read_conf_proc(config_path, verbose2conf)

# Función 1B
# Lectura de csv con listado de productos
path2csv = conf_dict['FOLDERS']['prods_list']
df = mfc.lectura_csv(path2csv, False)

# print("Presento argumento 1", sys.argv[1])

# print(f"Muestro dataframe: \n{df}")
filt_id = df['Name'] == sys.argv[1]
id = df.loc[filt_id]['Id']

print()
print(f'Presento id de producto: {sys.argv[1]}\n{id}')
print()
# print(f'Fila que tiene coincidencia con argumento {sys.argv[1]}\n{row}')
print(f'Presento el tipo de id:\n{type(id)}')
# print(f'Y presento el id que necesito:\n{row.get('Id')}')
# print(f'Y presento el tipo de dato:\n{type(row)}')
# print(f'Y presento el id que necesito:\n{row['Id']}')