import os
import configparser
from osgeo import ogr
import glob
import sys
from datetime import datetime
import pytz
import requests
import pandas as pd
import getpass

import geopandas as gpd, geoplot, matplotlib
from shapely.geometry import shape
from shapely import wkt

# Módulo para computar cociente y resto de una división
import numpy as np

# Módulo para Verificar si las credenciales ingresadas son correctas
sys.path.append(r'../utils')
from mod_dloader import try_cred
from mod_common2all import configure_logging

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
            'WKT_ROI': r'/src/Vectores/aux_wkt/wkt_file.txt',
            'SHP_ROI': r'/src/Vectores/shp/shp_file.shp',
            'OUTPUT': '/src/Output/',
            'SEARCHER_LOG': r'/src/utils/log'
        },
        'ATTRIB': {
            ';Comment line test for ATTRIB':None,
            'init_date':'01-01-2019',
            'final_date':'31-01-2021',
            'max_cloud':'50',
            'Sent_mission':'SENTINEL-2',
            ';The attribute "proj_name" should not have blank spaces':None,
            'proj_name':'Your_name',
            ';The processor will process the quantity of sample number':None,
            'sample_number':'12'
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
        },
        'PROCESSOR': {
            '; Configuración para procesador posterior a búsqueda/filtrado':None,
            '; Type: Significa el tipo de procesamiento a aplicar a la colección de productos a bajar, puede ser NDVI, RGB': None,
            'Type':'RGB',
            'Conf_proc':'/src/utils/CONF_PROC.INI',
            'conf_searcher':'/src/utils/CONF_SEARCHER.INI'
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

def verfi_cred(dictWcreds, verbose):
    # utilizo diccionario con credencailes ingresadas de manera manual
    # print(dictWcreds)
    user = dictWcreds['ESA_SERVER']['user']
    passw = dictWcreds['ESA_SERVER']['pass']
    msg_dict, status_creds = try_cred(user, passw, False)
    # print(str_token)
    while(not status_creds):
        print('Credenciales inválidas, vuelva a ingresarlas por favor.')
        # Vuelvo a ingresar credenciales por teclado
        new_dictWcreds = read_keys(dictWcreds, False)
        user = new_dictWcreds['ESA_SERVER']['user']
        passw = new_dictWcreds['ESA_SERVER']['pass']
        msg_dict, status_creds = try_cred(user, passw, False)
    print('Credenciales validas')
    if verbose:
        print(dictWcreds)
        # print(str_token)
    # print('Salida de debbuging en verficación de credenciales')
    # os._exit(0)

    return None

def read_keys(config_dictionary, verbose):
    new_conf_dict = config_dictionary
    print('A continuación se requerirá el ingreso del usuario de dataspace copernicus:')
    name = input("Ingreso de usuario: ")
    new_conf_dict['ESA_SERVER']['user'] = name
    # print(f"Hello, {name}!")
    # pass_key = input('Ingreso de contraseña')
    # password = getpass.getpass(f"Ingreso de contraseña (para {name}): ")
    while True:
        try:
            password = getpass.getpass(f"Ingreso de contraseña (para {name}): ")
            if not password:  # Checks if input is empty
                raise ValueError("La contraseña no puede estar vacía. Intente nuevamente.")
            break  # Exit loop if password is valid
        except ValueError as e:
            print(e)

# print("Password received successfully!")
    new_conf_dict['ESA_SERVER']['pass'] = password
    return new_conf_dict

# Creación de archivo de configuración para procesador
def save_conf2proc(conf_searcher, output_meta_df, verbose):
    # Me baso en lo que voy necesitando en 'Note2proc.ipynb' y en Note2script_snappy.ipynb
    # Necesito, en ppio las siguientes variables
    # Ruta a listado csv (FOLDERS)
    # Ruta a kml de entrada (FOLDERS)
    # Ruta a wkt de kml de entrada (FOLDERS)
    # Usuario de portal de la ESA (ATTRIB)
    # Pass de usuario (ATTRIB)
    # Carpeta de salida única de búsqueda (o sea debo gnerar la carpeta de salida única por búsqueda) (FOLDERS)

    # líneas de debug
    #################
    # print(conf_searcher)
    # print(output_meta_df)
    # print(output_meta_df.index)
    # print('Presentación de datos de serie: ',output_meta_df.at['Proj Name', 'Datos']) # Llamada correcta para obtener el valor de la serie
    # print('Presentación de datos de serie, método 2: ',output_meta_df.loc['Datos'].get('Proj Name')) # Incorrecto
    # print(output_meta_df['Proj Name']) # -> de esta manera no parece acceder al dato de la serie 'Proj Name'
    #################


    # Definición de carpeta de salida de proyecto para guardar los productos de salida
    folder_output = output_meta_df.at['Proj Name', 'Datos'] + '_' + output_meta_df.at['Search name', 'Datos'].split('_')[1]
    output_path = os.path.join(conf_searcher['FOLDERS']['output'], folder_output)
    log_path = os.path.join(output_path, 'logs')


    # Genero diccionario a guardar como configuración de procesador.
    dict_gen = {
        'FOLDERS': {
            ';Prueba de comentarios para FOLDERS':None,
            'PRODS_LIST': os.path.join(conf_searcher['FOLDERS']['output'], output_meta_df.at['Search name', 'Datos'].split('.')[0] + '.csv'),
            'KML_INPUT': os.path.join(conf_searcher['FOLDERS']['roi'], output_meta_df.at['ROI name', 'Datos']),
            'WKT_ROI': conf_searcher['FOLDERS']['wkt_roi'],
            'SHP_ROI': conf_searcher['FOLDERS']['shp_roi'],
            'OUTPUT': output_path,
            'LOGS': log_path
        },
        'ATTRIB': {
            ';Prueba de comentarios para ATTRIB':None,
            'user': conf_searcher['ESA_SERVER']['user'],
            'pass': conf_searcher['ESA_SERVER']['pass'],
            'proj_name':conf_searcher['ATTRIB']['proj_name']
        },
        'PROCESSOR': {
            '; Configuracion para procesador posterior a busqueda/filtrado':None,
            '; Type: Significa el tipo de procesamiento a aplicar a la coleccion de productos a bajar, puede ser NDVI, RGB': None,
            'Type':conf_searcher['PROCESSOR']['type'],
            'conf_search_path':conf_searcher['PROCESSOR']['conf_searcher']
        }
    }
    with open(conf_searcher['PROCESSOR']['conf_proc'],"w") as file:
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
    init_date = set_init_date(dict['ATTRIB']['init_date'], False)
    final_date = set_final_date(dict['ATTRIB']['final_date'], False)
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
    if plat_str == 'SENTINEL-2':
        # Busco por colección y por contenido de la palabra en el producto ('MSIL2A')
        ret_str = f"Collection/Name eq '{plat_str}' and contains(Name,'MSIL2A')"
    else:
        ret_str = f"Collection/Name eq '{plat_str}'"
    return ret_str

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
        sys.exit('Hay más de un archivo vectorial en carpeta Vectores, borrar hasta que quede uno solo')
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

def write_wkt_4326(path2roi, o_path, verbose):
    # o_path = '/src/Vectores/aux_wkt/wkt_file.txt'
    wkt = set_wkt_V1(path2roi, verbose)
    with open(o_path, 'w') as f:
        f.write(wkt)
    return None

def write_shp_4326(fn, o_path, verbose):
    # Primer versión de lector de kml, busca la geometría del primer feature de la capa y lo guarda en formato Esri Shapefile
    # Obtengo nombre de shapefile de salida.
    # out_dir, out_name = os.path.split(o_path)

    # Uso de glob
    ds_path = ds_finder(fn, False)
    ds_qty = len(ds_path)
    if ds_qty == 1:
        fn_path = ds_path[0]
    elif ds_qty > 1:
        sys.exit('Hay más de un archivo vectorial en carpeta Vectores, borrar hasta que quede uno solo')
    else:
        sys.exit(f'No se encuentra datasource en la carpeta "{fn}"')
    
    # Lectura de ds de entrada
    ds_input = ogr.Open(fn_path, 0)
    if ds_input is None:
        sys.exit(f'No se puede abrir el archivo {fn}')
    
    in_lyr = ds_input.GetLayer(0)

    # Creación de ds de salida
    out_ds_name, out_layer_name = parse_ds_and_name(o_path, verbose)    # Nombres de ds y capa de salida
    shp_driver = ogr.GetDriverByName('ESRI Shapefile')                  # Creación de driver de salida
    shp_ds = shp_driver.CreateDataSource(out_ds_name)                   # Creación de ds en base a nombre

    # Borro el contenido de la capa previamente guardada (sino tengo problemas cuando vuelvo a escribir la capa)
    if shp_ds.GetLayer(out_layer_name):
        shp_ds.DeleteLayer(out_layer_name)
    
    # print(f'Verifico defnición de geometría para capa de entrada: {in_lyr.GetGeomType()}')
    # print(ogr.wkbPolygon, ogr.wkbMultiPolygon, ogr.wkbUnknown)
    out_lyr = shp_ds.CreateLayer(out_layer_name, in_lyr.GetSpatialRef(), ogr.wkbUnknown) # Creo capa de salida utilizando el nombre designado
    out_lyr.CreateFields(in_lyr.schema)                                 # Creo camposs en función de la capa de entrada

    # Creación de característica (feature) en blanco para completarla y guardarla en capa de salida
    out_defn = out_lyr.GetLayerDefn()   # definición de campos de salida
    out_feat = ogr.Feature(out_defn)    # Atributo o feature con los mismos campos de la capa de entrada

    # La única manera que encontré para acceder al primer feature fue a través del iterable de in_lyr
    for feature in in_lyr:
        geom = feature.geometry()                       # Copio geometría de feature seleccionad
        out_feat.SetGeometry(geom)                      # Seteo geometría en feature auxiliar
        for i in range(feature.GetFieldCount()):        # Copio todos los campos de la feat seleccionada
            value = feature.GetField(i)                 # Tomo el valor del atributo seleccionado
            out_feat.SetField(i, value)                 # Seteo valor en atributo auxiliar
        out_lyr.CreateFeature(out_feat)                 # Seteo atributo auxiliar en atributo de salida


    del ds_input
    del shp_ds

    if verbose:
        print()
        print(f'Prueba de verbose en función {write_shp_4326.__name__}')
        print(f'Nombre de ds de entrada {fn}')
        print(f'Nombre de capa de salida {out_ds_name}')
    return None

def parse_ds_and_name(path, verbose):
    ds_name, layer_name = os.path.split(path)
    # Modificación de layer_name para quitarle la extensión al archivo
    layer_name = layer_name.split('.')[0]

    if verbose:
        print()
        print(f'Verbose de función {parse_ds_and_name.__name__}')
        print(f'Nombre de ds: {ds_name}')
        print(f'Nombre de layer: {layer_name}')
    return ds_name, layer_name


def df_proc(df, verbose):
    # Primer paso: descomponer nombre de producto (en columna 'Name') en otras columnas
    df_name_conv = descom_name(df, verbose)
    # Segundo paso: Transformo fecha de adquisición a tipo datetime
    df_name_conv['Sensing_time']= pd.to_datetime(df_name_conv['Sensing_time'])
    # Tercer paso: Setear multíndice 'Sensing_time', 'Prod_level', 'Baseline', 'Tile'
    dfWatts_Sidx = df_name_conv.set_index(['Sensing_time','Prod_level','Tile', 'Baseline'])
    # Cuarto paso: Filtro por tipo de proceasmiento, solo se queda con 'MSIL2A'
    dfWatts_Sidx_Fd = dfWatts_Sidx.loc[:,['MSIL2A'],:]
    # Quinto paso: Cómputo de cloud cover a partir de columna de df
    dfWatts_Sidx_Fd['cloudCover'] = read_cloud_cover(dfWatts_Sidx_Fd.Attributes.apply(pd.Series), verbose = False)
    # Sexto paso: Cambio de orden de columna, mando cloud cover al ppio del df
    dfWatts_Sidx_Fd = change_col(dfWatts_Sidx_Fd)
    # Séptimo paso: Obtiene frame de producto S2
    gdfWatts_Sidx_Fd = get_shape_S2(dfWatts_Sidx_Fd, verbose = False)
    return gdfWatts_Sidx_Fd

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

def get_shape_S2(df, verbose = False):
    Fprint_list = list(df['GeoFootprint'])
    geo_list = []
    # display(Fprint_list)
    for geojson_item in Fprint_list:
        geom_f_gjson = shape(geojson_item)
        geo_list.append(geom_f_gjson)
    
    crs = 'EPSG:' + df.iloc[0][['Footprint']].item().split(';')[0].split('=')[1]

    df['shape'] = geo_list

    return gpd.GeoDataFrame(df, geometry='shape',crs=crs)

def roi2gdf(roi_folder, df, verbose = False):
    ROI_wkt = set_wkt_V1(roi_folder, False)
    ROI_shape = wkt.loads(ROI_wkt)
    # display(ROI_shape)
    d = {'col1': ['ROI busqueda'], 'geometry': [ROI_shape]}
    crs = 'EPSG:' + df.iloc[0][['Footprint']].item().split(';')[0].split('=')[1]
    return gpd.GeoDataFrame(d, crs=crs)

def get_shape(folder, verbose = False):
    ROI_wkt = set_wkt_V1(folder, False)
    return wkt.loads(ROI_wkt)

def comp_intersec(gdf, roi_folder, verbose = False):
    roi_gdf = roi2gdf(roi_folder, gdf, verbose = False)
    ROI_shape = get_shape(roi_folder, verbose = False)
    inter_shapes = gdf.overlay(roi_gdf, how='intersection')
    list2add = list(inter_shapes.area/ROI_shape.area)
    # Lo agrego en ppio a geodataframe de interesección 'inter_shapes_2'
    gdf['ROI_intersec'] = list2add
    if verbose:
        print(gdf,inter_shapes, sep = '\n')

    return gdf

# Link de recursos para hallar valores únicos de fechas en MultiIndex
# https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html
def filter_df(df2filter, filter_type =1):
    """ Filtro el df generado para quedarme con un solo producto por día """
    if filter_type == 3:
        list2concat = filter_3(df2filter)
    else:
        
        # Select from all the entries filtered by "sensing day" just one appling differents algorithms
        idx = df2filter.index
        # I try to get entries by day, someway...
        day_list = list(idx.remove_unused_levels().get_level_values(0).unique())
        
        ## Código para filtrar productos encontrados un solo día ##
        list2concat = []
        for date in day_list:
            # print(f'Listado de productos de fecha: {str(date)}')
            # display(df2filter.loc[date])
            if filter_type == 1:
                list2concat.append(filter_1(df2filter.loc[date]))
            elif filter_type == 2:
                list2concat.append(filter_2(df2filter.loc[date]))
        ####################################################################
    
        print('Cantidad de productos a ingresar:', len(list2concat))

    prod_filtered = pd.DataFrame(list2concat)

    # display(prod_filtered)
    
    return prod_filtered

def filter_1(dfbydate):
    # print('Cantidad de productos por fecha: ', dfbydate['Id'].count())
    # display(dfbydate.iloc[0])
    return dfbydate.iloc[0]

def filter_2(dfbydate):
    # display(dfbydate)
    qty_entries = dfbydate.Id.count()
    # print(f'Cantidad de entradas por día {qty_entries}')
    if  qty_entries == 1:
        return dfbydate.iloc[0]
    else:
        # Filtro en primera instancia por área de intersección con ROI
        df_filt_1 = dfbydate.nlargest(qty_entries, 'ROI_intersec')
        qty_entries_2 = df_filt_1.Id.count()
        # Filtro en segunda instancia por cobertura nubosa
        df_filt_2 = df_filt_1.nsmallest(qty_entries_2, 'cloudCover')
        return df_filt_2.iloc[0]

def filter_3(df):
    """ Filtrado general, analizo primero todo el df y luego filtro, los otros filtran ciertos atributos pero de a un día a la vez """
    # Línea para filtrar columna por valor determinado (en este caso discriminación de tile)    
    
    idx = df.index
    tile_list = list(idx.remove_unused_levels().get_level_values(2).unique())
    
    # Obtengo los tipo de tile en qué se divide el producto disponible y obtengo la cantidad de nubosidad por tile
    list_cc = []
    for i,tile in enumerate(tile_list):
        df2analize = df.loc[:,:,[tile]]
        cloud_cover_sum = df2analize['cloudCover'].sum()
        list_cc.append((i, tile, cloud_cover_sum))
    
    print(list_cc)

    if len(list_cc) > 1:
        # Elección de tile según comparación de cobertura nubosa (ellijo la que tiene el menor número)
        if list_cc[0][2] < list_cc[1][2]:
            tile_def = list_cc[0][1]
            tile_wrong = list_cc[1][1]
        else:
            tile_def = list_cc[1][1]
            tile_wrong = list_cc[0][1]
    else:
        tile_def = list_cc[0][1]

    # Quedaría seleccionar las entradas por tile y quedarme con una por día (a implementar)
    
    # Procesamiento de df elegido para quedarme con la de mayor número de procesamiento
    df_chos = df.loc[:,:,[tile_def]]
    idx_chos = df_chos.index
    basel_series = (idx_chos.get_level_values(3)).to_series() # PENDIENTE DE CONTINUAR: Este procesamiento lo tengo que hacer por día

    # Procesamiento de serie para transformar los caracteres en número
    # Primero quito la 'N' del código de baseline
    basel_proc = basel_series.str.replace('N','')

    # Segundo paso la cadena de caracteres a número
    basel_proc = pd.to_numeric(basel_proc)

    # Guardo la serie procesada como una columna en el dataframe elegido
    # Vuelo a setear índice original para no tener problema con el seteo de la nueva columna en dataframe elegido
    # basel_proc.reset_index(inplace = True) -> no funcionó esta solución, debí pasarla a lista y después guardarla como columna
    basel_nbr_list = list(basel_proc)
    df_chos['base_nber'] = basel_nbr_list

    # Aplico algoritmo para seleccionar producto por día
    # Filtro en primera instancia por área de intersección con ROI
    
    idx_chos = df_chos.index
    # I try to get entries by day, someway...
    day_list_chos = list(idx_chos.remove_unused_levels().get_level_values(0).unique())
    
    ## Código para filtrar productos encontrados un solo día ##
    list2concat = []
    # display(df_chos)
    for date in day_list_chos:
        # print(date)
        list2concat.append(filter_base_nber(df_chos.loc[date], date, verbose = False))
    df_final = pd.DataFrame(list2concat)
    return df_final
        
def filter_base_nber(dfbyday, date, verbose = False):
    qty_entries = dfbyday.Id.count()
    dfbyday['acq_date'] = date
    # print(f'Cantidad de entradas por día {qty_entries}')
    if  qty_entries == 1:
        return dfbyday.iloc[0]
    else:
        # Filtro la opción 9999, será la última opción
        dfbyday.sort_values(by = 'base_nber', inplace = True, ascending = False)
        # display(dfbyday.iloc[0])
        if dfbyday.iloc[0]['base_nber'] == 9999:
            return dfbyday.iloc[1]
        else:
            return dfbyday.iloc[0]
        # max_value = dfbyday['base_nber'].max()
        # idx_max = dfbyday.index[dfbyday['base_nber'] == max_value]
        # print(f'Presentación de máximo valor de número de base: {max_value, idx_max}')
        # display(dfbyday.loc[idx_max])
        # display(dfbyday)
        # PENDIENTE: Elegir productos dejando como última opción 9999 y luego elegir dataset por mayor valor de procesamiento
def disp_and_type(obj, type_of_show='display'):
    print('Tipo del objeto presentado', type(obj), sep='\n')
    print('Objeto a verificar')
    if (type_of_show == 'print'):
        print(obj)
    else:
        display(obj)
    return None

# def msf.sample_gdf(gdf_filtered, conf_dict['ATTRIB']['sample_number'], True)
def sample_gdf(gdf, sample_number, verbose):
    tot_samp = len(gdf)
    sample_number = int(sample_number)
    if sample_number == 0:
        if verbose:
            print("No se modifica cantidad de regsitros en dataframe")
        return gdf
    else: 
        quotient, remaider = np.divmod(tot_samp, sample_number)
        if quotient >= 1:
            if remaider == 0:
                sample_step = quotient
            elif remaider > 0:
                sample_step = quotient + 1
        elif quotient < 1:
            sample_step = 1

    if verbose:
        print(f'Muestro valor de variables de función {sample_gdf.__name__}')
        print(f"Cantidad de entradas totales: {tot_samp}")
        print(f"Cantidad de muestras deseadas: {sample_number}")
        print(f"Saltos dentro de muestreo: {sample_step}")
        print(f"Cantidad de muestras final de dataframe: {len(gdf[::sample_step])}")
        print('Original dataframe without sample it')
        print(gdf)
        print('Dataframe sampled')
        print(gdf[::sample_step])

    return gdf[::sample_step]

def save_df(df_and_name, output_path):
    # Salvo dataframes en excels
    with pd.ExcelWriter(output_path) as writer:
        # df_conf.to_excel(writer, sheet_name=s_names[0])
        # gdf.to_excel(writer, sheet_name=s_names[1])
        for df, name in df_and_name:
            df.to_excel(writer, sheet_name=name)
        # df2.to_excel(writer, sheet_name='Sheet_name_2')
    # Creo nombres de archivos csv y pkl de salida
    # print(output_path)
    output_path_csv = output_path.split('.')[0] + '.csv'
    output_path_pkl = output_path.split('.')[0] + '.pkl'
    # Solo voy a guardar el dataframe de resumen en csv y pkl
    for df, name in df_and_name:
        if (name == 'resume_search'):
            df.to_csv(output_path_csv)
            df.to_pickle(output_path_pkl)    
    return None

def  comp_search_att(conf_dict, verbose = False):
    # Primer versión de confección de dataframe con datos de búsqueda
    data = {}
    # Guardo nombre de proyecto
    proj_name = conf_dict['ATTRIB']['proj_name']
    data['Proj Name'] = proj_name
    # Guardo el momento de generar la búsqueda
    x_date = datetime.now()
    search_date = x_date.strftime("%c")
    data['Search date'] = search_date
    # Guardo nombre de datos vectorial
    ds_path = os.path.basename(ds_finder(conf_dict['FOLDERS']['roi'], False)[0])
    # Guardo configuración de fechas inicial y final de búsqueda
    data['ROI name'] = os.path.basename(ds_path)
    init_date = conf_dict['ATTRIB']['init_date']
    data['Initial date'] = init_date
    final_date = conf_dict['ATTRIB']['final_date']
    data['Final date'] = final_date
    # Guardo máximo valor de cobertura de nubes
    data['Cloud cover conf'] = conf_dict['ATTRIB']['max_cloud']
    # Cantidad máxima de resultados a devolver
    data['Max result qty'] = conf_dict['ESA_SERVER']['top']
    # Nombre de archivo de búsqueda
    search_name = 'research' + '_' + x_date.strftime("%Y%m%dT%H%M%S") + '_' + ds_path.split('.')[0] + '.xlsx'
    data['Search name'] = search_name

    df = pd.DataFrame.from_dict(data, orient='index', columns = ['Datos'])
    if verbose:
        print(data, df, sep='\n')

    return df