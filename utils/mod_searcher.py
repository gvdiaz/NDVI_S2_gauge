import pickle
import pandas
import configparser
import os

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
    return None

def conf_reader(path2conf):
    config_object = configparser.ConfigParser()
    # file =open(path2conf,"r")
    with open(path2conf,"r") as file:
        config_object.read_file(file)
        output_dict=dict()
        sections=config_object.sections()
        for section in sections:
            items=config_object.items(section)
            if items.is
            output_dict[section]=dict(items)
        print("The output dictionary is:")
        print(output_dict)
    

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
            'ROI': r'/src/Vectores/Campo_Atahona.kml',
            'OUTPUT': '/src/Output/'
        },
        'ATTRIB': {
            'init_date':'01-01-2019',
            'final_date':'31-01-2021',
            'max_cloud':'50',
            'Sent_mission':'MSIL2A',
            'proj_name':'Your name'
        },
        'ESA_SERVER': {
            'url':'https://catalogue.dataspace.copernicus.eu/odata/v1/Products',
            'orderby': 'ContentDate/Start',
            'top':'100'
    }
    }
    with open(path2conf,"w") as file:
    # file =open("employee1.ini","w")
        config_object = configparser.ConfigParser()
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
    
    