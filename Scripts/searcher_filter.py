# Script para generar request de búsqueda y filtrado de productos Sentinel-2
import sys
import os

sys.path.append(r'../utils')
import mod_search_filt as msf

# Cuerpo de script a ejecutar

config_path = r'/src/utils/CONF_SEARCHER.INI'

verbose2conf = False
# Lectura de archivo de configuración de búsqueda
conf_dict = msf.read_conf_searcher(config_path, verbose2conf)
# Lectura de usuario y pass de DataSpace Copernicus de la ESA (https://documentation.dataspace.copernicus.eu/APIs/OData.html#product-download)
conf_dict = msf.read_keys(conf_dict, verbose2conf)
# Verifico credenciales ingresadas antes de continuar
msf.verfi_cred(conf_dict, verbose2conf)
# Armado de request para realizar la búsqueda
req_str = msf.set_ESA_req(conf_dict, True)
# Envío de request
json = msf.send_req(req_str)
# Conversión de información recibida a df
df = msf.req_to_df(json['value'])
# Procesamiento de df para obtener df con MultiIndices, filtrado por misión, computada área nubosa y área de superposición
gdf_final = msf.df_proc(df, False)
# Procesamiento de df para computar área de intersección enrte ROI y frames S2
gdf_intersec = msf.comp_intersec(gdf_final, conf_dict['FOLDERS']['roi'], verbose = False)
# Filtrado de opciones presentadas (hay tres opciones)
gdf_filtered = msf.filter_df(gdf_intersec, filter_type =3)
# Reducción de dataframe filtrado para que entregue la cantidad de 'sample_number' diccionario de configuración
gdf_filtered_reduc = msf.sample_gdf(gdf_filtered, conf_dict['ATTRIB']['sample_number'], True)
gdf_filtered_reduc_name = 'search_page'
# Genero dataframe resumido para facilitar lectura en excel
resume_gdf = gdf_filtered_reduc.loc[:, ['cloudCover', 'Id', 'Name', 'shape', 'acq_date']]
resume_gdf_name = 'resume_search'
# df_new = df.loc[:, ['team', 'rebounds']]
# Armado de portada de búsqueda (se guardará en excel)
search_df = msf.comp_search_att(conf_dict, True)
search_df_name = 'cover_search'
# Compendio de información a guardar
df_and_name_tuple = [(search_df, search_df_name),\
                     (resume_gdf, resume_gdf_name), \
                     (gdf_filtered_reduc, gdf_filtered_reduc_name)]
# Tomo nombre generado en los atributos de búsqueda
bsname = search_df.loc['Search name'].item()
# Agrego carpeta a path de archivo de salida
pre_out_prod = os.path.join(conf_dict['FOLDERS']['output'], bsname)
# Guardo la información generada en excel
msf.save_df(df_and_name_tuple, pre_out_prod)
# Genero wkt en carpeta de Vectores/aux_wkt
msf.write_wkt_4326(conf_dict['FOLDERS']['roi'], conf_dict['FOLDERS']['wkt_roi'], verbose2conf)
# Genero shp en carpeta ...
msf.write_shp_4326(conf_dict['FOLDERS']['roi'], conf_dict['FOLDERS']['shp_roi'], verbose2conf)
# Guardo configuración para Procesador (paso posterior)
msf.save_conf2proc(conf_dict, search_df, conf_dict['SCRIPTING']['verbose'])