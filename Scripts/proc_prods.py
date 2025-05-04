# Script para procesar producto bajado con módulo snappy
# Fecha 23/03/2025

# Módulos a importar
import sys
import os
import logging
# Módulo para bajer productos S2
sys.path.append(r'../utils')

# Para implementar funciones de esa_snappy en módulo
import mod_snappy11_S2 as msnap

def main(conf_dict, verbose2conf):

    # Leo tipo de procesamiento
    flag_proc = conf_dict['PROCESSOR']['type']

    # Función 1B
    # Lectura de csv con listado de productos
    path2csv = conf_dict['FOLDERS']['prods_list']
    df = msnap.lectura_csv(path2csv, False)

    # Selecciono fila correspondiente a producto, luego voy a tener guardar los datos de estadística en esa fila y guardar el df

    filt_id = df['Name'] == sys.argv[1]
    idx_row = df.loc[filt_id].index.to_list()[0]

    # Definiciones necesarias para creación de productos de salida
    prod_name = df.at[idx_row, 'Name']
    acq_date = str(df.at[idx_row, 'acq_date'])

    # Verifico si existe la carpeta donde bajé producto
    root_folder = conf_dict['FOLDERS']['output']

    subfolder_name = 'cutted_masked'
    # Creación de carpeta NDVI o RGB
    flag_proc = conf_dict['PROCESSOR']['type']
    if flag_proc == 'NDVI':
        subfolder_name = 'NDVI' + '_' + subfolder_name
    elif flag_proc == 'RGB':
        subfolder_name = 'RGB' + '_' + subfolder_name

    cutted_masked_path = os.path.join(root_folder, subfolder_name)

    subfolder_name = 'tmp'

    tmp_path = os.path.join(root_folder, subfolder_name)

    if os.path.isdir(tmp_path):
        print(f"Carpeta temporal {tmp_path} creada.")
    else:
        print(f"Carpeta temporal {tmp_path} no creada.")

    # Configuración para guardar errores en archivo de log
    # log_name = sys.argv[1].split('.')[0] + "_proc_prods_error.log"
    # log_path = os.path.join(tmp_path, log_name)
    # sys.stderr = open(log_path, 'w')

    path2wkt = conf_dict['FOLDERS']['wkt_roi']

    prod_path = os.path.join(tmp_path,prod_name + '.zip')

    # Ahora verifico si existe el producto bajado
    if os.path.isfile(prod_path):
        print(f"Archivo {prod_path} bajado.")

        dict2df = msnap.dict_reader(tmp_path, verbose2conf)
        
        # Verificación de fecha para adaptar los nuevos productos Sentinel-2 (acq_date > 01-07-2024)
        
        

        # Función 1I
        # Recortar producto
        product_subset = msnap.subset_prod(prod_path, path2wkt, False)

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
            # La siguiente función dconf_dict, verbose2confevuelve media, std_dev y path de producto generado
            mean, std_dev, path2png = msnap.plotNDVI_s2_png_v2(prod_s_res_msk_roi_msk, acq_date, output_path, 0, 1)
        elif flag_proc == 'RGB':
            mean, std_dev, path2png = msnap.plotRGB_s2_2_png_v2(prod_s_res_msk_roi_msk, acq_date, output_path, 0, 0.3)
        
        print(f"Valores estadisticos obtenidos:\nmedia: {mean}\nstd_dev: {std_dev}\nUbicacion: {path2png}")

        # Guardo datos estadísticos de cualquiera de las dos procesamientos
        dict2df['path2png'].append(path2png)
        dict2df['mean_value'].append(mean)
        dict2df['std_dev_value'].append(std_dev)
        dict2df['prod_name'].append(prod_name)

        # Borrado de archivo bajado
        msnap.erase_tmp(prod_path, True)

        msnap.dict_saver(tmp_path, dict2df, False)

    else:
        print(f"Archivo {tmp_path} no bajado.")

    return 0

# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         if 'prod_path' in globals():    
#             if os.path.isfile(prod_path):
#                 os.remove(prod_path)
#                 print(f'Archivo {prod_path} borrado.')
#             # print(f"Critical error: {e}", file=sys.stderr)
#             # traceback.print_exc()  # Print full traceback
#             # # Take custom actions:
#             # send_alert_email("Script crashed!")  # Example recovery
#             # sys.exit(1)  # Exit with error code

if __name__ == "__main__":
    # Cuerpo de script a ejecutar
    # Parte 1ra
    # Tengo definido ruta a archivo de configación del procesador general.
    config_path = r'/src/utils/CONF_PROC.INI'
    verbose2conf = False

    # Función 1A
    # Lectura de archivo de configuración de búsqueda
    conf_dict = msnap.read_conf_proc(config_path, verbose2conf)
    log_filename = msnap.configure_logging(folder_path = conf_dict['FOLDERS']['logs'], proj_name = conf_dict['ATTRIB']['proj_name'])

    # msnap.configure_logging()
    try:
        exit_code = main(conf_dict, verbose2conf)
        # exit_code = main(conf_dict, verbose2conf, development)
        if os.path.exists(log_filename) and os.path.getsize(log_filename) == 0:
            os.remove(log_filename)
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        exit_code = 1
    sys.exit(exit_code)