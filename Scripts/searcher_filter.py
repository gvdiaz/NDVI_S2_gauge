# Script para generar request de búsqueda y filtrado de productos Sentinel-2
import sys

sys.path.append(r'../utils')
import mod_search_filt as msf

# Cuerpo de script a ejecutar

config_path = r'/src/utils/CONF_SEARCHER.INI'

verbose2conf = True
conf_dict = msf.read_conf_searcher(config_path, verbose2conf)
req_str = msf.set_ESA_req(conf_dict, verbose2conf)
json = msf.send_req(req_str)
df = msf.req_to_df(json['value'])
gdf_final = msf.df_proc(df, False)
# roi_gdf = msf.roi2gdf(conf_dict['FOLDERS']['roi'], df, verbose = False)
gdf_intersec = msf.comp_intersec(gdf_final, conf_dict['FOLDERS']['roi'], verbose = False)
print(gdf_final, gdf_intersec, sep='\n')
gdf_filtered = msf.filter_df(gdf_intersec, filter_type =3)
pre_out_prod = r'/src/Output/research.xlsx'
msf.save_df(gdf_filtered, pre_out_prod)