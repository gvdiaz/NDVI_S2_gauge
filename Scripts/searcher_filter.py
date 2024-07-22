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
df_final = df_proc(df, False)
print(df_final.info)