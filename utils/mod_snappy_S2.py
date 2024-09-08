# Para abrir y bajar archivos en lista de bajada
import pandas as pd
import os
import sys

def set_input_vars(verbose=False):
    aux_dict = {}
    aux_dict['input_path'] = r'/src/output/research_20240725T223256_Tratayen.xls'
    aux_dict['output_path'] = r'/src/Scripts/aux_files/muestras_RGB/'
    aux_dict['S2_prod_path'] = r'/src/Scripts/aux_files/S2_aux/'
    aux_dict['wkt_orig_path'] = r'./aux_files/wkt_file.txt'
    if verbose:
        display(aux_dict)
    return aux_dict

def wkt_reader(wkt_path, verbose=False):
    with open(wkt_path, 'r') as f:
        wkt_string = f.readline()
    if verbose:
        print(f'WKT: {wkt_string}')
    return wkt_string

def lect_df_prod_s2(input_path, verbose=False):
    df = pd.read_excel(input_path, sheet_name='resume_search')
    if verbose:
        print(df)
    return df

def set_user_pass(verbose=False):
    user = 'gus838@gmail.com'
    passw = 'Ul!RsPWTPuw3'
    if verbose:
        print(f'User: {user}')
        print(f'User: {passw}')
    return (user, passw)

def lect_vars(serie, verbose=False):
    prod_id = serie['Id']
    prod_name = serie['Name']
    acq_date = serie['acq_date']
    if verbose:
        print(f'Id producto: {prod_id}')
        print(f'Nombre producto: {prod_name}')
        print(f'Fecha adquisición producto: {acq_date}')
        print()
    return (prod_id, prod_name, acq_date)