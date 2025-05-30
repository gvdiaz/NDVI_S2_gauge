# Script para implementar funcionamiento de subprocess lanzado en script principal
# Fecha: 20/12/2024

import sys
import pandas as pd
import os
# módulo para verificar si un path existe
from pathlib import Path

# Módulo para bajer productos S2
sys.path.append(r'../utils')
import mod_dloader as mdl

# Para implementar funciones de snappy en módulo
import mod_snappy_S2 as msnap

# Cuerpo de script a ejecutar
# Parte 1ra
# Tengo definido ruta a archivo de configación del procesador general.
config_path = r'/src/utils/CONF_PROC.INI'
development = True
verbose2conf = False

# Función 1A
# Lectura de archivo de configuración de búsqueda
conf_dict = msnap.read_conf_proc(config_path, verbose2conf)

# Función 1B
# Borrado de carpeta root en caso de que se haya creado algo.
root_folder = Path(conf_dict['FOLDERS']['output'])
if development:
    msnap.del_folder(root_folder, False)

# Función 1C
# Creación de carpeta root para salida de procesamiento
root_folder.mkdir()

# Función 1D
# Creación de carpeta cutted_masked partiendo de root_folder
subfolder_name = 'cutted_masked'
# Creación de carpeta NDVI o RGB
flag_proc = conf_dict['PROCESSOR']['type']
if flag_proc == 'NDVI':
    subfolder_name = 'NDVI' + '_' + subfolder_name
elif flag_proc == 'RGB':
    subfolder_name = 'RGB' + '_' + subfolder_name

cutted_masked_path = msnap.folder_creator(root_folder, subfolder_name, False)

# table_path = msnap.folder_creator(root_folder, subfolder_name, True)

# Función 1E
# Creación de carpeta table (carpeta donde guardaré df de salida)
subfolder_name = 'table'
table_path = msnap.folder_creator(root_folder, subfolder_name, False)

# Función 1F
# Creación de carpeta temporal (se guardará producto S2 y se procesará, en caso de que necesite guardar algún subproducto)
subfolder_name = 'tmp'
tmp_path = msnap.folder_creator(root_folder, subfolder_name, False)

# Función 1G
# Lectura de csv con listado de productos
path2csv = conf_dict['FOLDERS']['prods_list']
df = msnap.lectura_csv(path2csv, False)

# Función 1H
# Bajar productos completos
# Iteración sobre todos los productos
# Dejo una configuración que me permitirá solo procesar el primer producto,\
# cuando verifique que funciona dehabilitaré la función para que procese todos los productos de la misma manera que el primero
flag_one_proc = False

# Definición de usuario
user = conf_dict['ATTRIB']['user']
passw = conf_dict['ATTRIB']['pass']
kc_token = 'KEYCLOAK_TOKEN'

# Definición de parámetros a registrar sobre cada producto
dict2df = {'path2png':[],
            'mean_value': [],
            'std_dev_value': []
}

for row in df.iterrows():
    prod_id = row[1]['Id']
    prod_name = row[1]['Name']
    acq_date = str(row[1]['acq_date'])
    str_token = mdl.get_keycloak(user, passw, False)
    os.environ[kc_token] = str_token
    file2verif = os.path.join(tmp_path,prod_name + '.zip')
    if os.path.isfile(file2verif):
        print(f'Archivo {file2verif} existente')
        pass
    else:
        print(f'Archivo {file2verif} NO existente, bajando')
        mdl.prod_downloader_2(prod_id, os.environ[kc_token], tmp_path, prod_name, False)
    
    path2wkt = conf_dict['FOLDERS']['wkt_roi']
    path2prod = os.path.join(tmp_path, file2verif)

    # Función 1I
    # Recortar producto
    product_subset = msnap.subset_prod(path2prod, path2wkt, False)

    # Implementación de función de resize 1J
    resamp_prod = msnap.resize(product_subset, 'B2')

    # Función 1K
    # Enmascarado de cirros
    prod_s_res_msk = msnap.masking(resamp_prod, 'cirrus_clouds', invert = True)

    # Agrego shape a vectores
    shp_path = conf_dict['FOLDERS']['shp_roi']
    added_geom_prod = msnap.add_geometry2prod_3(prod_s_res_msk, shp_path) # Código comentado porque cambió el origen del shape, ahora debe ser wkt
    # added_geom_prod = msnap.add_geometry2prod_4(prod_s_res_msk, path2wkt)
    shp_name = os.path.basename(shp_path).split('.')[0] # Guardo nombre para llamarlo en la función masking
    # shp_name = 'shape' # Hardcodeo porque la función add_geometry2prod_4 solo lo guarda con ese nombre genérico

    # Implementación de Función 1M
    prod_s_res_msk_roi_msk = msnap.masking(added_geom_prod, shp_name, invert = False)

    # Implementación de Función 1Na
    file_extension = '_c_and_m'
    if flag_proc == 'NDVI':
        file_extension = '_NDVI' + file_extension
    elif flag_proc == 'RGB':
        file_extension = '_RGB' + file_extension
    output_name = msnap.out_filename(prod_name, file_extension, False)

    # Escritura de archivo de salida
    output_path = os.path.join(cutted_masked_path, output_name)
    # msnap.writeProd(prod_s_res_msk_roi_msk, output_path)
    if flag_proc == 'NDVI':
        # La siguiente función devuelve media, std_dev y path de producto generado
        mean, std_dev, path2png = msnap.plotNDVI_s2_png(prod_s_res_msk_roi_msk, acq_date, output_path, 0, 1)
    elif flag_proc == 'RGB':
        mean, std_dev, path2png = msnap.plotRGB_s2_2_png(prod_s_res_msk_roi_msk, acq_date, output_path, 0, 0.3)

    # Guardo datos estadísticos de cualquiera de las dos procesamientos
    dict2df['path2png'].append(path2png)
    dict2df['mean_value'].append(mean)
    dict2df['std_dev_value'].append(std_dev)

    # Borrado de archivo bajado
    msnap.erase_tmp(path2prod, True)
    
    if flag_one_proc == True:
        break

# Guardado en df de los nuevos datos estadísticos.
for key, value in dict2df.items():
    df[key] = value

# Exporto df a tabla para poder explorarla
# Primero creo el path al archivo
path2table = os.path.join(table_path, 'statistics')
msnap.save_simple_df(df, path2table, False)

# Ploteo de serie temporal (por ahora solo para NDVI)
msnap.temp_series_2(df, table_path, False)

# Guardo archivo de configuración en carpeta de salida
msnap.save_search_conf(config_path, conf_dict, verbose2conf)


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

# root_folder = Path(conf_dict['FOLDERS']['output'])
# if development:
#     msnap.del_folder(root_folder, True)
# print(f'Apertura de carpeta de salida: {root_folder}')