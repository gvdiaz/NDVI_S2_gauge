import json
import os
import requests
import shutil
from tqdm.auto import tqdm
def get_keycloak(username: str, password: str, verbose) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password"
        }
    try:
        r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
        data=data
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Reponse from the server was: {r.json()}"
            )
    if verbose:
        print('Visualización de variables en get_keycloak en módulo mod_dloader.py')
        print(data)
        print(r.json())
    return r.json()["access_token"]

def try_cred(username: str, password: str, verbose) -> str:
    flag_status = None
    response = None
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password"
        }
    r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
    data=data)
    # r.raise_for_status()
    response = r.json()
    if 'error' in response:
        flag_status = False
    elif 'access_token' in response:
        flag_status = True
    else:
        flag_status = False
    if verbose:
        print('Visualización de variables en get_keycloak en módulo mod_dloader.py')
        print(data)
        print(r.json())
    return response, flag_status

# keycloak_token = get_keycloak("USERNAME", "PASSWORD")

def show_sname(script_name):
    print('------------------------------------------------------------')
    print(f"El script que se encuentra funcionando es: \n{script_name}")
    print()
    return None

def show_dict(dict_def):
    # print(type(dict_def), dict_def.keys())
    print("----------Separador de inicio show_dict----------")
    keys = dict_def.keys()
    for key in keys:
        print(key,dict_def[key],sep='\n')
        print()
    print("----------Separador de fin show_dict----------")
    return None

def save_response(dict_def, path2save, verbose):
    
    tmp_file_name = "esa_response.txt"
    tmp_file_path = os.path.join(path2save, tmp_file_name)

    with open(tmp_file_path, "w") as file:
        for key, value in dict_def.items():
            file.write(f"{key}: {value}\n")

    print("File written successfully!")

    if verbose:
        with open(tmp_file_path, "r") as file:
            content = file.read()
            print(content)
    
    return None

def prod_downloader(prod_id, keycloak_token,output_path,file_name):
    print("inicio de 'bajador'")
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + keycloak_token})
    url = f"http://catalogue.dataspace.copernicus.eu/odata/v1/Products({prod_id})/$value"
    print(url)

    # with session.get(url, allow_redirects=False) as response:
    #     total_length = int(response.headers.get("Content-Length"))
    #     with tqdm.wrapattr(response.raw, "read", total=total_length, desc="") as raw:
    #         file_name=file_name + ".zip"
    #         product_file = os.path.join(output_path,file_name)
    #         with open(product_file,'wb') as p:
    #             shutil.copyfileobj(raw, p)
                # p.write(file.content)
    
    response = session.get(url, allow_redirects=False, stream=True)
    
    while response.status_code in (301, 302, 303, 307):
        url = response.headers['Location']
        response = session.get(url, allow_redirects=False)
        print(response.status_code, url, sep='\n')

    show_dict(response.headers)
    
    file_name=file_name + ".zip"
    product_file = os.path.join(output_path,file_name)

    print('Debug antes de "bajar" el archivo"')

    # file = session.get(url, verify=False, allow_redirects=True)
    
    # with session.get(url, verify=False, allow_redirects=True) as file:
    #     print(file.headers)
    #     total_length = int(file.headers.get("Content-Length"))
    #     with tqdm.wrapattr(file.raw, "read", total=total_length, desc="") as raw:
    #         with open(product_file, 'wb') as p:
    #             shutil.copyfileobj(raw, p)

    # divisor = 10

    with requests.get(url, stream=True, verify=False, allow_redirects=True) as r:
        print(r, type(r))
    
        total_length = int(r.headers.get('Content-Length'))
        # Define the size of the chunk to iterate over (Mb)
        # piece = 10 * 1024
        with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
            with open(product_file, mode="wb") as file:
                shutil.copyfileobj(raw, file)

        # for i,chunk in enumerate(r.iter_content(chunk_size=piece)):
        #     if (i%divisor) == 0:
        #         print(i)
        #     file.write(chunk)


    print('Debug posterior de "bajar" el archivo"')

    # with open(product_file, 'wb') as p:
    #     p.write(file.content)
    return None

def prod_downloader_2(prod_id, keycloak_token, output_path, file_name, verbose):
    
    url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({prod_id})/$value"
    # url = f"http://catalogue.dataspace.copernicus.eu/odata/v1/Products({prod_id})/$value"

    headers = {"Authorization": f"Bearer {keycloak_token}"}

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, headers=headers, stream=True)

    file_name=file_name + ".zip"
    product_file = os.path.join(output_path,file_name)

    file_size = int(response.headers["Content-Length"])
    chunk_req = 8192
    iters = int(file_size/chunk_req)
    unit_div = 1024

    if verbose:
        save_response(response.headers, output_path, verbose)
        print('Muestro diccionario de headers a request: \n')
        show_dict(response.headers)
        print('Cantidad de bytes a bajar')
        print('Cantidad de bytes a bajar: ', file_size)
        print('Varibales relativas a requests chunks')
        print('chunk:',chunk_req)
        print('Variable cantidad de iteraciones')
        print('iters', iters)

    with open(product_file, "wb") as file:
        for chunk in tqdm(response.iter_content(chunk_size=chunk_req), \
                        #   unit="B", \
                          unit_scale=True,  \
                        #   unit_divisor=(unit_div*chunk_req), \
                          total=iters, \
                          desc=file_name):
            if chunk:
                file.write(chunk)
    
    return None