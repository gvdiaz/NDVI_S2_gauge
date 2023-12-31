# Modificación de "token_decoder.py" para que antes de bajar los productos renueve el token id

import os
import datetime as dt
import json
import requests
import sys
sys.path.append(r'../utils')
import mod_dloader as mdl
import mod_searcher as ms

# Argumento 1: Ruta que contiene diccionario token
# Argumento 2: Ruta que contiene string keycloak
# Argumento 3: Ruta que contiene string prod_id
# Argumento 4: user
# Argumento 5: pass

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
    path_prod_id = r'../output/'
    prod_id_file = r'prod_id_selected.pkl'
    pth_prod_id = os.path.join(path_prod_id, prod_id_file)
    print(os.path.isfile(pth_prod_id), pth_prod_id)

# Verifico usuario
try:
    user = sys.argv[4]
except:
    user = r''
    # pth_prod_id = os.path.join(path_prod_id, prod_id_file)
    # print(os.path.isfile(pth_prod_id), pth_prod_id)

# Verifico pass
try:
    passw = sys.argv[5]
except:
    passw = r''
    
# # Relevo escritura de archivo de token
# with open(pth_comp, mode="r") as file:
#     lines = file.readlines()
# # print(lines[0])

# dict_def = json.loads(lines[0])
# dict_def['review_time'] = dt.datetime.now()

# Muestro diccionario a través de sus claves
# mdl.show_dict(dict_def)
aux_key = 'access_token'
kc_token = 'KEYCLOAK_TOKEN'
# os.environ[kc_token] = dict_def[aux_key]
# print(f'Muestra de keycloak token {kc_token}',os.environ[kc_token],sep='\n')
# print('Muestro token de access token: ',dict_def[aux_key], sep='\n')

# Lectura de archivo que contiene "product id"
# with open(pth_prod_id, 'r') as prod_id_file:
#     # print(prod_id_file.read())
#     prod_id = prod_id_file.read()
# print('Muestra de id de producto:',prod_id, sep='\n')

# prod_id = ms.read_list(pth_prod_id)[0]
# print(prod_id)

# Directorio de producto de salida
output_path = r'../output/'

# Prueba de lectura de dataframe de búsqueda
df_search = ms.read_df_search(pth_prod_id)
print(df_search[['Id','Name']])
for row in df_search.iterrows():
    prod_id = row[1]['Id']
    prod_name = row[1]['Name']
    str_token = mdl.get_keycloak(user, passw)
    print(str_token)
    os.environ[kc_token] = str_token
    mdl.prod_downloader(prod_id, os.environ[kc_token], output_path, prod_name)

    # print('Product id',row[1]['Id'])
    # print('File Name',row[1]['Name'])
    # print()