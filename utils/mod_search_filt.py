import os
import configparser
from osgeo import ogr
import glob
import sys
from datetime import datetime
import pytz
import requests
import pandas as pd

# Módulo para transcribir funciones desarrolladas para la búsqueda y filtrado de productos Sentinel-2 en Notebook "Nube_funciones.ipynb"

# Definiciones del código

# Columnas a setear cuando de procesa el nombre del producto Sentinel-2
naming_list = ['Mission_id', 'Prod_level', 'Sensing_time', 'Baseline', 'Rel_orb_num', 'Tile', 'Prod_time']

# Creación o lectura de archivo de configuración
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

# Envio de requests a servidor de la ESA

def send_req(str_req, verbose = False):
    return requests.get(str_req).json()

# Conversión de búsqueda a dataframe para su posterior procesamiento

def req_to_df(req_from_dict, verbose = False):
    return pd.DataFrame.from_dict(req_from_dict)

# Configuración de request de búsqueda en servidores de ESA en función de archivo de configuración

def set_ESA_req(dict, verbose):
    filter_Sent = set_platform(dict['ATTRIB']['sent_mission'], verbose)
    wkt = set_wkt_V1(dict['FOLDERS']['roi'], False)
    init_date = set_init_date(dict['ATTRIB']['init_date'], True)
    final_date = set_final_date(dict['ATTRIB']['final_date'], True)
    orderby_str = dict['ESA_SERVER']['orderby']
    quantity = dict['ESA_SERVER']['top']
    url = dict['ESA_SERVER']['url']
    cloud_cover = dict['ATTRIB']['max_cloud']
    
    prefix_place =f"OData.CSC.Intersects(area=geography'SRID=4326;{wkt}')"
    prefix_cloud = f"Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le {cloud_cover})"
    prefix_dates = f"ContentDate/Start {init_date} and ContentDate/Start {final_date}"
    
    # renew_query_mis_pl = f"{url}?$filter={filter_Sent} and {prefix_place} and ContentDate/Start {init_date} and ContentDate/Start {final_date}&$orderby={orderby_str}&$top={quantity}"
    renew_query_mis_pl_cc = f"{url}?$filter={filter_Sent} and {prefix_place} and {prefix_cloud} and {prefix_dates}&$orderby={orderby_str}&$top={quantity}&$expand=Attributes"
    if verbose:
        print(filter_Sent)
        print(wkt)
        print(init_date)
        print(final_date)
        print(orderby_str)
        print(quantity)
        print(renew_query_mis_pl_cc)
    return renew_query_mis_pl_cc


def set_platform(plat_str, verbose):
    return f"Collection/Name%20eq%20%27{plat_str}%27%20"

def get_time_format_req(date_data, verbose):
# Función para pasar dato de horario a str de salida con formato requerido para hora
    str_date = date_data.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    if verbose:
        print(str_date)
    return str_date

def set_init_date(init_date, verbose):
    # print(init_date)
    init_date_dt = set_date(init_date, verbose)
    return 'gt ' + get_time_format_req(init_date_dt, verbose)

def set_final_date(final_date, verbose):
    final_date_dt = set_date(final_date, verbose)
    return 'lt ' + get_time_format_req(final_date_dt, verbose)

def set_date(date, verbose):
    date_dt = datetime.strptime(date, '%d-%m-%Y')
    return date_dt

def ds_finder(folder, verbose):
    """ Función para buscar archivos terminados en kml o shp (por el momento) """
    shp_list = glob.glob('*.shp', root_dir = folder, recursive = False)
    kml_list = glob.glob('*.kml', root_dir = folder, recursive = False)
    # print(shp_list, kml_list)
    kml_list = [os.path.join(folder, file) for file in kml_list]
    shp_list = [os.path.join(folder, file) for file in shp_list]

    return shp_list + kml_list

def set_wkt_V1(fn, verbose):
    # Primer versión de lector de wkt, busca la geometría del primer feature de la capa

    # Uso de glob
    ds_path = ds_finder(fn, False)
    ds_qty = len(ds_path)
    if ds_qty == 1:
        fn_path = ds_path[0]
    elif ds_qty > 1:
        sys.exit('Hay más de un archivo temporal, borrar hasta que quede uno solo')
    else:
        sys.exit(f'No se encuentra datasource en la carpeta "{fn}"')
    

    ds = ogr.Open(fn_path, 0)
    if ds is None:
        sys.exit(f'No se puede abrir el archivo {fn}')
    lyr = ds.GetLayer(0)
    for feature in lyr:
        geometry = feature.GetGeometryRef()
        geom_wkt = geometry.ExportToWkt()
        break
    if verbose:
        # Visualización de campos disponibles
        print('Tipos de campos disponibles')
        for field in lyr.schema:
            print(field.name, field.GetTypeName(), sep ='\t'*2)
        # Visualización de tipo de geometría
        print()
        print('Tipo de geometría de capa: ', lyr.GetGeomType())
        print()
        print('Visualización de referencia espacial', lyr.GetSpatialRef(), sep = '\n')
        print()
        print('Visualización de geometrías')
        print(geometry.GetGeometryName())
        print(geometry.ExportToWkt())
    del ds
    return geom_wkt

def df_proc(df, verbose):
    # Primer paso: descomponer nombre de producto (en columna 'Name') en otras columnas
    df_name_conv = descom_name(df, verbose)
    # Segundo paso: Transformo fecha de adquisición a tipo datetime
    df_name_conv['Sensing_time']= pd.to_datetime(df_name_conv['Sensing_time'])
    # Tercer paso: Setear multíndice 'Sensing_time', 'Prod_level', 'Baseline', 'Tile'
    dfWatts_Sidx = dfWatts.set_index(['Sensing_time','Prod_level','Tile', 'Baseline'])
    # Cuarto paso: Filtro por tipo de proceasmiento, solo se queda con 'MSIL2A'
    dfWatts_Sidx_Fd = dfWatts_Sidx.loc[:,['MSIL2A'],:]
    # Quinto paso: Cómputo de cloud cover a partir de columna de df
    dfWatts_Sidx_Fd['cloudCover'] = read_cloud_cover(dfWatts_Sidx_Fd.Attributes.apply(pd.Series))
    # Sexto paso: Cambio de orden de columna, mando cloud cover al ppio del df
    dfWatts_Sidx_Fd = change_col(dfWatts_Sidx_Fd)
    # Séptimo paso: Cómputo de superposición de ROI con frame Sentinel-2
    
    return df

def descom_name(df, verbose = False):
    df_name = df['Name'].map(lambda x: x.split('_'))
    # Convierto lista de datos, ahora separados, en columnas
    dfFname = df_name.apply(pd.Series)
    # Agrego nombre a columnas
    dfFname.columns = naming_list
    # Concateno nuevo dataframe con el df de entrada
    dfWatts = pd.concat([df, dfFname], axis=1)
    return dfWatts

def read_cloud_cover(df_cloud_att, verbose):
    # Tomo los dos tipos de productos (tienen diferentes atributos) y sumo lo que se lee en cloud cover, sino es 0
    df_cloud_att_2 = (df_cloud_att[2].apply(lambda x: x['Value'] if x['Name'] == 'cloudCover' else 0))
    df_cloud_att_3 = (df_cloud_att[3].apply(lambda x: x['Value'] if x['Name'] == 'cloudCover' else 0))
    df_cloud_att_f = df_cloud_att_2 + df_cloud_att_3
    return df_cloud_att_f

def change_col(df, verbose = False):
    col_list = (list(df.columns))

    aux_value = col_list[-1]
    col_list[-1] = col_list[0]
    col_list[0] = aux_value

    return df[col_list]