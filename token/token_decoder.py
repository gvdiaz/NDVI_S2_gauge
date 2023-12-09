# Script para interpretar token de portal de Copernicus / Traer id de producto a bajar / e implementar keycloak getter

import os
import datetime as dt
import json
import requests
import sys
sys.path.append(r'../utils')
import mod_dloader as mdl

# Argumento 1: Ruta que contiene diccionario token
# Argumento 2: Ruta que contiene string keycloak
# Argumento 3: Ruta que contiene string prod_id

# Muestro qué script se encuentra trabajando
mdl.show_sname(sys.argv[0])

# Verifico si se ingresó el archivo de token
try:
    pth_comp = sys.argv[1]
except:
    path_token =r'./'
    text_file = r'token_dict.txt'
    pth_comp = os.path.join(path_token,text_file)
    print(os.path.exists(pth_comp), pth_comp)

# Verifico archivo de product id
try:
    pth_prod_id = sys.argv[3]
except:
    path_prod_id = r'../output/prod_list/'
    prod_id_file = r'prod_id_selected.txt'
    pth_prod_id = os.path.join(path_prod_id, prod_id_file)
    print(os.path.exists(pth_prod_id), pth_prod_id)
    
# Relevo escritura de archivo de token
with open(pth_comp, mode="r") as file:
    lines = file.readlines()
# print(lines[0])

dict_def = json.loads(lines[0])
dict_def['review_time'] = dt.datetime.now()

# Muestro diccionario a través de sus claves
# mdl.show_dict(dict_def)
aux_key = 'access_token'
kc_token = 'KEYCLOAK_TOKEN'
print(f'Muestra de keycloak token {kc_token}',os.environ[kc_token],sep='\n')
print('Muestro token de access token: ',dict_def[aux_key], sep='\n')

# Lectura de archivo que contiene "product id"
# with open(pth_prod_id, 'r') as prod_id_file:
#     # print(prod_id_file.read())
#     prod_id = prod_id_file.read()
# print('Muestra de id de producto:',prod_id, sep='\n')

prod_id = ms.read_list(out_list)[0]
print(prod_id)

# Directorio de producto de salida
output_path = r'../output/'

mdl.prod_downloader(prod_id, os.environ[kc_token],output_path)
# mdl.prod_downloader(prod_id, dict_def[aux_key], output_path)
