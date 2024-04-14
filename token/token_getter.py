import sys
import os,stat
sys.path.append(r'../utils')
import mod_dloader as mdl

# Argumento 1: user_s2
# Argumento 2: pass_s2
# Argumento 3: Ruta de salida para guardar cadena de caracteres de keycloak



# Archivos para pedido de token modelo y de salida
curl_model_path = './get_token_model.sh'
curl_output = './get_token.sh'

# Muestro si existe la ruta del archivo modelo
# print(os.path.isfile(curl_model_path), curl_model_path)

# Levanto toda la cadena del archivo modelo
with open(curl_model_path, 'r') as model_req:
    text2rep = model_req.read()

# Definición de cadenas a reemplazar en archivo modelo
repl_list = ['@user', '@pass']

# Muestro todo el texto antes de generar el archivo de salida
# print(text2rep)

# Bloque de código para realizar el reemplazo
for i,stream in enumerate(repl_list):
    # print(repl_list[i], sys.argv[i+1])
    text2rep = text2rep.replace(repl_list[i], sys.argv[i+1])

# Verifico que se haya modificado la cadena de salida como esperaba
# print('Modificado',text2rep, sep='\n')

# Escritura de cadena en archivo de salida. Fuera de este script cambio los permisos del archivo, adentro del script no me lo permite.
with open(curl_output,'w') as output_file:
    output_file.write(text2rep)

## Pedido de keycloak
# print('Pedido de keycloak')
key_cloak_str = mdl.get_keycloak(sys.argv[1], sys.argv[2], sys.argv[3])

# print(key_cloak_str, type(key_cloak_str), sep='\n')

# Escritura de keycloak a archivo de salida
with open(sys.argv[3],'w') as out_file:
    out_file.write(key_cloak_str)

if sys.argv[3]:
    # Muestro qué script se encuentra trabajando
    mdl.show_sname(sys.argv[0])
    print(f'Fin de script {sys.argv[0]}')
    print()
    
    
# os.chmod(curl_output, stat.S_IRWXU)