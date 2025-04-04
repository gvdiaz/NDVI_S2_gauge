# Script guardar información estadística recogida en procesamiento en "proc_prods.py"
# Fecha: 29/03/2025

# Módulo para ingresar módulo desarrollado sin importar snappy (para hacerlo más liviano)
import sys
# Módulo para función 1B
# módulo para verificar si un path existe
from pathlib import Path

# Módulo para 
import os

# Módulo con funciones desarrolladas.
# Módulo para bajer productos S2
sys.path.append(r'../utils')
import mod_s_snappy_p3_6 as mfc

# Funciones que necesito implementar

# Tengo definido ruta a archivo de configación del procesador general.
config_path = r'/src/utils/CONF_PROC.INI'
development = False
verbose2conf = False

# Función 1A
# Lectura de archivo de configuración de búsqueda
conf_dict = mfc.read_conf_proc(config_path, verbose2conf)

# Verifico si existe la carpeta donde bajé producto
root_folder = conf_dict['FOLDERS']['output']

# Uso la carpeta tmp
subfolder_name = 'tmp'

tmp_path = os.path.join(root_folder, subfolder_name)

# Lectura valores estadísticos computados
dict2df = mfc.dict_reader(tmp_path, verbose2conf)

# Función 1B
# Lectura de csv con listado de productos
path2csv = conf_dict['FOLDERS']['prods_list']
df = mfc.lectura_csv(path2csv, False)

# Agrego columnas de estadística en dataframe con los valores agregados
df = mfc.add_statistics(df, dict2df, verbose2conf)
# df = df.assign(**dict2df).ffill()

print(df)

# Función 1E
# Creación de carpeta table (carpeta donde guardaré df de salida)
subfolder_name = 'table'
table_path = mfc.folder_creator_method(root_folder, subfolder_name, False)

# Secuencia de guardado de información
# Exporto df a tabla para poder explorarla
# Primero creo el path al archivo
path2table = os.path.join(table_path, 'statistics')                     ## Tarea: traer variable 'table_path' -> Hecho
mfc.save_simple_df(df, path2table, False)

# Ploteo de serie temporal (por ahora solo para NDVI)
mfc.temp_series_2(df, table_path, False)

# Guardo archivo de configuración en carpeta de salida
# mfc.save_search_conf(config_path, conf_dict, verbose2conf)


if verbose2conf:
    print(conf_dict)
    print(f'Carpeta recien creada: {root_folder}')
    print(f'Carpeta recien creada: {cutted_masked_path}')
    print(f'Carpeta recien creada: {table_path}')
    print(f'Carpeta recien creada: {tmp_path}')
    print(f'Muestra de dataframe cargado: {path2csv}', df, sep = '\n')
    # Verificación de atributos de producto
    # msnap.show_att_S2(path2prod, verbose = True)
    # msnap.plotRGB_s2(product_subset, str(acq_date), 0, 0.3)
    # msnap.plotRGB_s2(prod_s_res_msk, str(acq_date), 0, 0.3)
    # msnap.plotRGB_s2(prod_s_res_msk_roi_msk, str(acq_date), 0, 0.3)
