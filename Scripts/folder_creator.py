# Script para crear carpetas de proyecto una vez que se realizó la búsqueda de los productos disponibles
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
# Parte 1ra
# Tengo definido ruta a archivo de configación del procesador general.
config_path = r'/src/utils/CONF_PROC.INI'
development = False
verbose2conf = False

# Función 1A
# Lectura de archivo de configuración de búsqueda
conf_dict = mfc.read_conf_proc(config_path, verbose2conf)

# # Función 1B
# # Borrado de carpeta root en caso de que se haya creado algo.
root_folder = Path(conf_dict['FOLDERS']['output'])
if development:
    mfc.del_folder(root_folder, False)

# # Función 1C
# # Creación de carpeta root para salida de procesamiento
if root_folder.exists() and root_folder.is_dir():
    # print("Folder exists")
    pass
else:
    root_folder.mkdir()
    # print("Folder does not exist")
    # print("Creating...")

# Función 1D
# Creación de carpeta cutted_masked partiendo de root_folder
subfolder_name = 'cutted_masked'
# Creación de carpeta NDVI o RGB
flag_proc = conf_dict['PROCESSOR']['type']
if flag_proc == 'NDVI':
    subfolder_name = 'NDVI' + '_' + subfolder_name
elif flag_proc == 'RGB':
    subfolder_name = 'RGB' + '_' + subfolder_name

cutted_masked_path = mfc.folder_creator_method(root_folder, subfolder_name, False)

# Función 1E
# Creación de carpeta table (carpeta donde guardaré df de salida)
subfolder_name = 'table'
table_path = mfc.folder_creator_method(root_folder, subfolder_name, False)

# Función 1F
# Creación de carpeta temporal (se guardará producto S2 y se procesará, en caso de que necesite guardar algún subproducto)
subfolder_name = 'tmp'
tmp_path = mfc.folder_creator_method(root_folder, subfolder_name, False)

# Función 1G
# Lectura de csv con listado de productos
path2csv = conf_dict['FOLDERS']['prods_list']
df = mfc.lectura_csv(path2csv, False)

# print(df['Name'])
list_name = "prods2download.list"
path2list = os.path.join(tmp_path, list_name)

df['Name'].to_csv(path2list, index=False, header=False)

# os.environ["MY_VAR"] = os.path.join(tmp_path, list_name)
output_folder = conf_dict['FOLDERS']['output'].split('/')[3]
# print(str(output_folder))
# Creación de path para ejecutarlo en bash del SO base.
output_path = os.path.join(output_folder, subfolder_name, list_name)
# Imprimo el path de salida sin que tenga el retorno de carro (me dificultó mucho encontrar este claro error)
print(output_path, end="")

# print("Fin de procesador folder_creator.py")