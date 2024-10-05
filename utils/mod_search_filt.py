import os
import configparser
from osgeo import ogr
import glob
import sys
from datetime import datetime
import pytz
import requests
import pandas as pd

import geopandas as gpd, geoplot, matplotlib
from shapely.geometry import shape
from shapely import wkt

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
            'Sent_mission':'SENTINEL-2',
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
        },
        'PROCESSOR': {
            '; Configuración para procesador posterior a búsqueda/filtrado':None,
            '; Type: Significa el tipo de procesamiento a aplicar a la colección de productos a bajar, puede ser NDVI, RGB': None,
            'Type':'RGB'
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