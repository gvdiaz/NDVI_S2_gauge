import os
import configparser
from osgeo import ogr
from datetime import datetime
import pytz
import requests

# Módulo para transcribir funciones desarrolladas para la búsqueda y filtrado de productos Sentinel-2 en Notebook "Nube_funciones.ipynb"

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

def set_wkt_V1(fn, verbose):
    # Primer versión de lector de wkt, busca la geometría del primer feature de la capa
    ds = ogr.Open(fn, 0)
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