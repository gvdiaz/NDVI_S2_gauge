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
# Armado de request para realizar la búsqueda
req_str = msf.set_ESA_req(conf_dict, verbose2conf)
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
# Armado de portada de búsqueda (se guardará en excel)
search_df = msf.comp_search_att(conf_dict, True)
bsname = search_df.loc['Search name'].item()
# print(bsname)
pre_out_prod = os.path.join(conf_dict['FOLDERS']['output'], bsname)
# print(pre_out_prod)
# r'/src/Output/research.xlsx'
sheet_name = ['set_search', 'search']
msf.save_df(search_df, gdf_filtered, sheet_name, pre_out_prod)