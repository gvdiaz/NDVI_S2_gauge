import pickle
import pandas as pd
import configparser
import os
# La función del_folder y read_conf_proc
import shutil
from pathlib import Path

# Módulos para mostrar resumen de serie temporal
import numpy as np
import matplotlib.pyplot as plt

# Atributos
pick_name = 'statistics_dict.pkl'

# Limpieza de carpeta generada (normalmente va a estar completa en etapa de debbuging.
def del_folder(path2folder, verbose):
    # Creo la variable root_folder para definir la carpeta base a borrar
    root_folder = Path(path2folder)
    # Verifico si existe la carpeta
    if root_folder.exists():
        shutil.rmtree(path2folder)
    if verbose:
        print(f'The folder {root_folder} has been deleted.')
    return None

# Creación o lectura de archivo de configuración
def read_conf_proc(path2conf, verbose):
    if not(os.path.exists(path2conf)):
        create_conf_file_proc(path2conf)
    if verbose:
        with open(path2conf, 'r') as file:
            # Read the content of the file
            file_content = file.read()
            # Print the content
            print("File Content:\n", file_content)
    conf2dict = configparser.ConfigParser()
    with open(path2conf,"r") as file:
        conf2dict.read_file(file)
    # conf2dict.read_file(path2conf)
    return {s:dict(conf2dict.items(s)) for s in conf2dict.sections()}

def create_conf_file_proc(path2conf):
    # Configuración inicial
    # ROI*
    # Fecha de inicio de búsqueda
    # Fecha de fin de búsqueda
    # Tipo de producto Sentinel
    # Porcentaje de nubosidad límite
    # Nombre de proyecto relacionado
    dict_gen = {
        'FOLDERS': {
            ';Prueba de comentarios para FOLDERS':None,
            'ROI': r'/src/Vectores/',
            'OUTPUT': '/src/Output/'
        },
        'ATTRIB': {
            ';Prueba de comentarios para ATTRIB':None,
            'init_date':'01-01-2019',
            'final_date':'31-01-2021',
            'max_cloud':'50',
            'Sent_mission':'MSIL2A',
            'proj_name':'Your name'
        },
        'ESA_SERVER': {
            ';Prueba de comentarios para ESA_SERVER':None,
            'url':'https://catalogue.dataspace.copernicus.eu/odata/v1/Products',
            'orderby': 'ContentDate/Start',
            'top':'100'
    },
        'SCRIPTING':{
            ';Configuración para aplicar en funciones':None,
            'verbose': False
        }
    }

def folder_creator_method(root_path, folder2create, verbose):
    # Creo la variable root_folder para definir la carpeta base sobre la cual se crearán las subcarpetas del proyecto.
    root_folder = Path(root_path)
    if root_folder.exists() and root_folder.is_dir():
        folder_list = [root_folder, folder2create]
        path2newfol = Path(*folder_list)
        if path2newfol.exists() and path2newfol.is_dir():
            pass
        else:
            path2newfol.mkdir()
    else:
        sys.exit(f'Funcion "{folder_creator.__name__()}" terminada porque no se encontró la ruta a la carpeta "{root_path}" donde debe crearse "{folder2create}"')
    if verbose:
        print(f'Creacion correcta de carpeta "{path2newfol}"')
    return path2newfol

# Lectura de dataframes de búsqueda a partir del csv

def lectura_csv(path, verbose):
    df = pd.read_csv(path)
    df['acq_date'] = pd.to_datetime(df['acq_date'])
    # df.sort_values(by='A', ascending=True, inplace=True)
    df.sort_values(by='acq_date', ascending=True)

    if verbose:
        print(f'Muestro variable path de funcion {lectura_csv.__name__}')
        print()
        print(df)
    return df

def lectura_pkl(path, verbose):
    df = pd.read_pickle(path)
    if verbose:
        print(f'Muestro variable path de funcion {lectura_csv.__name__}')
        print()
        print(df)
    return df

# Funciones para escribir lista de búsqueda y poder leerla
# write list to binary file
def write_list(a_list,path_file):
    # store list in binary file so 'wb' mode
    with open(path_file, 'wb') as fp:
        pickle.dump(a_list, fp)
        print('Done writing list into a binary file')
        
# Write searched product ids in pickle
def write_df_search(df,output_path):
    # store list in binary file so 'wb' mode
    with open(output_path, 'wb') as fp:
        pickle.dump(df, fp)
        print('Done writing dataframe into a binary file')

# Read list to memory
def read_df_search(path_file):
    # Para leer dataframe de interés
    with open(path_file, 'rb') as fp:
        return pickle.load(fp)

# Read list to memory
def read_list(path_file):
    # Para leer dataframe de interés
    with open(path_file, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list

def read2list(path_file):
    # Función especial para tomas listas de dataframes con distintas búsquedas y devolución de la columna a lista de la primera búsqueda
    df_list = read_list(path_file)
    return df_list[0]['Id'].to_list()

def read_conf_searcher(path2conf, verbose):
    if not(os.path.exists(path2conf)):
        create_conf_file(path2conf)
    if verbose:
        with open(path2conf, 'r') as file:
            # Read the content of the file
            file_content = file.read()
            # Print the content
            print("File Content:\n", file_content)
    conf2dict = configparser.ConfigParser()
    with open(path2conf,"r") as file:
        conf2dict.read_file(file)
    # conf2dict.read_file(path2conf)
    return {s:dict(conf2dict.items(s)) for s in conf2dict.sections()}

def conf_reader(path2conf):
    config_object = configparser.ConfigParser()
    # file =open(path2conf,"r")
    with open(path2conf,"r") as file:
        config_object.read_file(file)
        output_dict=dict()
        sections=config_object.sections()
        for section in sections:
            items=config_object.items(section)
            # if items.is
            output_dict[section]=dict(items)
        print("The output dictionary is:")
        print(output_dict)
    return None
    

def create_conf_file(path2conf):
    # Configuración inicial
    # ROI*
    # Fecha de inicio de búsqueda
    # Fecha de fin de búsqueda
    # Tipo de producto Sentinel
    # Porcentaje de nubosidad límite
    # Nombre de proyecto relacionado
    dict_gen = {
        'FOLDERS': {
            ';Prueba de comentarios para FOLDERS':None,
            'ROI': r'/src/Vectores/Campo_Atahona.kml',
            'OUTPUT': '/src/Output/'
        },
        'ATTRIB': {
            ';Prueba de comentarios para ATTRIB':None,
            'init_date':'01-01-2019',
            'final_date':'31-01-2021',
            'max_cloud':'50',
            'Sent_mission':'MSIL2A',
            'proj_name':'Your name'
        },
        'ESA_SERVER': {
            ';Prueba de comentarios para ESA_SERVER':None,
            'url':'https://catalogue.dataspace.copernicus.eu/odata/v1/Products',
            'orderby': 'ContentDate/Start',
            'top':'100'
    }
    }
    with open(path2conf,"w") as file:
    # file =open("employee1.ini","w")
        config_object = configparser.ConfigParser(allow_no_value=True)
    # myDict={'employee': {'name': 'John Doe', 'age': '35'},
    #         'job': {'title': 'Software Engineer', 'department': 'IT', 'years_of_experience': '10'},
    #         'address': {'street': '123 Main St.', 'city': 'San Francisco', 'state': 'CA', 'zip': '94102'}}
        sections=dict_gen.keys()
        for section in sections:
            config_object.add_section(section)
        for section in sections:
            inner_dict=dict_gen[section]
            fields=inner_dict.keys()
            for field in fields:
                value=inner_dict[field]
                config_object.set(section, field, str(value))
        config_object.write(file)
    # file.close()
    return None

def dict_reader(path2dict, verbose):
    # Función para crear o abrir diccionario pickel
    # pick_name = 'statistics_dict.pkl' -> lo defino en los atributos para que lo pueda usar el read como el saver
    pick_path = os.path.join(path2dict, pick_name)
    if os.path.isfile(pick_path):
        with open(pick_path, 'rb') as file:
            pkl_dict = pickle.load(file)
    else:
        pkl_dict = {'path2png':[],
                    'mean_value': [],
                    'std_dev_value': [],
                    'prod_name': []
                    }

    return pkl_dict
    
def temp_series_2(df, folder2save, verbose):
    out_path = os.path.join(folder2save, 'temporal_series.png')
    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ndvi_color = 'green'
    ax1.errorbar(df['acq_date'], df['mean_value'], yerr = df['std_dev_value']/2, linestyle='-', marker='o', color=ndvi_color, label='mean_NDVI')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('NDVI [-]', color=ndvi_color)
    ax1.tick_params(axis='y', labelcolor=ndvi_color)
    plt.legend(loc='lower right')

    # Create a secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(df['acq_date'], df['cloudCover'], linestyle='', marker='D', color='blue', label='Product Cloud cover')
    ax2.set_ylabel('Cloud cover (%)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Add titles and grid
    plt.title('Temporal series two axis')
    fig.tight_layout()  # Adjust layout to prevent overlap
    plt.grid()
    plt.legend()
    plt.savefig(out_path , bbox_inches='tight')
    
    if verbose:
        plt.show()
    return None

def save_simple_df(df, output_path, verbose):
    # # Salvo dataframes en excels
    output_path_csv = output_path + '.csv'
    output_path_xls = output_path + '.xls'
    df.to_csv(output_path_csv)
    df.to_excel(output_path_xls)
    if verbose:
        print(df)
    
    return None

def save_search_conf(conf_dict, verbose):
    # Copio archivo de configuración de búscador a carpeta de salida
    # Primero obtengo nombre de archivo base
    out_name = os.path.basename(conf_dict['PROCESSOR']['conf_search_path'])
    # Segundo, genero ruta de archivo de salida
    out_path = os.path.join(conf_dict['FOLDERS']['output'], out_name)
    shutil.copy(conf_dict['PROCESSOR']['conf_search_path'], out_path)
    return None

def add_statistics(df_init, dict2add, verbose):
    df_stats = pd.DataFrame(dict2add)
    df_final = pd.merge(left=df_init, right=df_stats, how='left', left_on='Name', right_on='prod_name')
    return df_final

def delete_file(file2del, verbose2conf):
# Borro archivo de configuración de procesador, necesario para que no queden rastros de pass
    os.remove(file2del)
    return None