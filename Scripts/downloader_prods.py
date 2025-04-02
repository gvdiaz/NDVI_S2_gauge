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
# Módulo para bajar productos y acceder a token
import mod_dloader as mdl

# Funciones que necesito implementar

# Cuerpo de script a ejecutar
# Parte 2da
# Tengo definido ruta a archivo de configación del procesador general.
config_path = r'/src/utils/CONF_PROC.INI'
development = False
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
idx_row = df.loc[filt_id].index.to_list()[0]
# id = df.loc[filt_id]['Id']
print(f'Indice de linea de producto buscado{idx_row}')
id = df.at[idx_row, 'Id']

print()
print(f'Presento id de producto: {sys.argv[1]}\n{id}')
print()
# print(f'Fila que tiene coincidencia con argumento {sys.argv[1]}\n{row}')
# print(f'Presento el tipo de id:\n{type(id)}')
# print(f'Y presento el id que necesito:\n{row.get('Id')}')
# print(f'Y presento el tipo de dato:\n{type(row)}')
# print(f'Y presento el id que necesito:\n{row['Id']}')

# Recopilación de datos para bajar producto
# Definición de usuario
user = conf_dict['ATTRIB']['user']
passw = conf_dict['ATTRIB']['pass']

prod_id = df.at[idx_row, 'Id']
prod_name = df.at[idx_row, 'Name']
acq_date = str(df.at[idx_row, 'acq_date'])
str_token = mdl.get_keycloak(user, passw, False)
# print(prod_id, prod_name, acq_date, str_token, sep='\n')
# Verifico creación de directorios de proyecto
root_folder = conf_dict['FOLDERS']['output']
print(root_folder)
subfolder_name = 'tmp'
tmp_path = os.path.join(root_folder, subfolder_name)
if os.path.isdir(tmp_path):
    print(f"Carpeta temporal {tmp_path} creada.")
else:
    print(f"Carpeta temporal {tmp_path} no creada.")

# if len(os.listdir(tmp_path)) > 2:
#     print("Hay mas de un archivo bajado, termino script")
#     sys.exit(0)
# else:
#     pass

out_name = prod_name + '.zip'
prod_path = os.path.join(tmp_path, out_name)
print(f"Debug downloader_prods.py, nombre de archivo de salida:\n{prod_path}")

# Ahora verifico si existe el producto bajado
if os.path.isfile(prod_path):
    print(f"Archivo {prod_path} bajado.")
else:
    print(f"Archivo {prod_path} no bajado.")
    print("Bajando...")
    mdl.prod_downloader_2(prod_id, str_token, tmp_path, prod_name, verbose2conf)

# file2verif = os.path.join(tmp_path,prod_name + '.zip')

# mdl.prod_downloader_2(prod_id, str_token, tmp_path, prod_name, False)