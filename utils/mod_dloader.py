import json
import os
import requests
def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
        }
    try:
        r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
        data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Reponse from the server was: {r.json()}"
            )
    return r.json()["access_token"]

# keycloak_token = get_keycloak("USERNAME", "PASSWORD")

def show_sname(script_name):
    print('------------------------------------------------------------')
    print(f"El script que se encuentra funcionando es: \n{script_name}")
    print()
    return None

def show_dict(dict_def):
    # print(type(dict_def), dict_def.keys())
    keys = dict_def.keys()
    for key in keys:
        print(key,dict_def[key],sep='\n')
        print()
    return None

def prod_downloader(prod_id, keycloak_token,output_path):
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + keycloak_token})
    url = f"http://catalogue.dataspace.copernicus.eu/odata/v1/Products({prod_id})/$value"
    print(url)
    response = session.get(url, allow_redirects=False)
    while response.status_code in (301, 302, 303, 307):
        url = response.headers['Location']
        response = session.get(url, allow_redirects=False)

    file = session.get(url, verify=False, allow_redirects=True)
    file_name="producto.zip"
    product_file = os.path.join(output_path,file_name)

    with open(product_file, 'wb') as p:
        p.write(file.content)
    return None