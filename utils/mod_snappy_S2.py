# Para abrir y bajar archivos en lista de bajada
import pandas as pd
import os
import sys
# Módulo para leer configuración
import configparser
# Módulo para crear y borrar rutas a archivos o directorios
import shutil
# módulo para verificar si un path existe
from pathlib import Path

import snappy
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF
from snappy import ProductIO
from snappy import File
from snappy import ProgressMonitor
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

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
        print(f'Pass: {passw}')
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

def subset_prod(path2prod, path2wkt, verbose):
    # Objetivo 2 del día Cortar producto por geometría
    product = ProductIO.readProduct(path2prod)
    SubsetOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
    geometry = WKTReader().read(path2wkt)
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geometry)
    # product_subset = GPF.createProduct('Subset', parameters, product)
    return GPF.createProduct('Subset', parameters, product)

def plotRGB_s2(product, title, vmin, vmax):
    band_list = ['B4','B3','B2']
    band_stack = []
    for band in band_list:
        band=product.getBand(band)
        w=band.getRasterWidth()
        h=band.getRasterHeight()
#         depth = 3
        print(w,h)
        band_layer=np.zeros(w*h,np.float32)
        band.readPixels(0,0,w,h,band_layer)
        band_layer.shape=h,w
        band_stack.append(band_layer)
        
    width=12
    height=12
    rgb = np.dstack(band_stack)  # stacks 3 h x w arrays -> h x w x 3
    plt.figure(figsize=(width,height))
    plt.title('Producto de fecha: ' + title, fontweight ="bold") 
    imgplot=plt.imshow(rgb,cmap=plt.cm.binary,vmin=vmin,vmax=vmax)
    # plt.savefig('./aux_files/muetra.png', bbox_inches='tight')

    return None

def plotRGB_s2_2_png(product, title, path, vmin, vmax):
    band_list = ['B4','B3','B2']
    band_stack = []
    for band in band_list:
        band=product.getBand(band)
        w=band.getRasterWidth()
        h=band.getRasterHeight()
#         depth = 3
        # print(w,h)
        band_layer=np.zeros(w*h,np.float32)
        band.readPixels(0,0,w,h,band_layer)
        band_layer.shape=h,w
        band_stack.append(band_layer)
        
    width=12
    height=12
    rgb = np.dstack(band_stack)  # stacks 3 h x w arrays -> h x w x 3
    plt.figure(figsize=(width,height))
    plt.title('Producto de fecha: ' + title, fontweight ="bold") 
    imgplot=plt.imshow(rgb,cmap=plt.cm.binary,vmin=vmin,vmax=vmax)
    plt.savefig(path + '.png', bbox_inches='tight')

    return None

# Función para guardar y computar estadísticas de producto NDVI del producto
def plotNDVI_s2_png(product, title, path, vmin, vmax):
    band_list = ['B4','B8']
    band_stack = []
#     for band in band_list:
#         band=product.getBand(band)
#         w=band.getRasterWidth()
#         h=band.getRasterHeight()
# #         depth = 3
#         # print(w,h)
#         band_layer=np.zeros(w*h,np.float32)
#         band.readPixels(0,0,w,h,band_layer)
#         band_layer.shape=h,w
#         band_stack.append(band_layer)
        
#     width=12
#     height=12
#     rgb = np.dstack(band_stack)  # stacks 3 h x w arrays -> h x w x 3
#     plt.figure(figsize=(width,height))
#     plt.title('Producto de fecha: ' + title, fontweight ="bold") 
#     imgplot=plt.imshow(rgb,cmap=plt.cm.binary,vmin=vmin,vmax=vmax)
#     plt.savefig(path + '.png', bbox_inches='tight')

#*****************************************************************************************

    # product = ProductIO.readProduct(file)   # Apertura de producto
    width = product.getSceneRasterWidth()   # Obtención de ancho de producto
    height = product.getSceneRasterHeight() # Obtención de alto de producto
    name = product.getName()                # Obtención de nombre de producto
    description = product.getDescription()  # Obtención de descripción de producto
    # band_names = product.getBandNames()

    # print("Product:     %s, %s" % (name, description))
    # print("Raster size: %d x %d pixels" % (width, height))
    # print("Start time:  " + str(product.getStartTime()))
    # print("End time:    " + str(product.getEndTime()))
    # print("Bands:       %s" % (list(band_names)))


    b4 = product.getBand('B4')                                                  # Lectura de banda (supongo que roja)
    b8 = product.getBand('B8')                                                  # Lectura de banda (supongo que infrarroja)
    # ndviProduct = Product('NDVI', 'NDVI', width, height)                        # Definición de producto nuevo
    # ndviBand = ndviProduct.addBand('ndvi', ProductData.TYPE_FLOAT32)            # Agrego banda única (ndvi)
    # ndviFlagsBand = ndviProduct.addBand('ndvi_flags', ProductData.TYPE_UINT8)   # Agrego flags supongo que para el tipo de producto
    # writer = ProductIO.getProductWriter('BEAM-DIMAP')                           # Escritura de producto

    # ProductUtils.copyGeoCoding(product, ndviProduct)                            # Copia de proyección de georreferencia

    # ndviFlagCoding = FlagCoding('ndvi_flags')                                   # Flags de ndvi
    # ndviFlagCoding.addFlag("NDVI_LOW", 1, "NDVI below 0")                       # Agrego flag de mínimo valor
    # ndviFlagCoding.addFlag("NDVI_HIGH", 2, "NDVI above 1")                      # Agrego flag de máximo valor
    # group = ndviProduct.getFlagCodingGroup()                                    # Creo grupo de flags
    # #print(dir(group))
    # group.add(ndviFlagCoding)                                                   # Agrego grupo a producto

    # ndviFlagsBand.setSampleCoding(ndviFlagCoding)                               

    # ndviProduct.setProductWriter(writer)                                        # Creación de producto
    # ndviProduct.writeHeader('snappy_ndvi_output.dim')                           # Nombre de producto de salida

    r4 = np.zeros(width, dtype=np.float32)                                # Creación de línea en numpy banda B4
    r8 = np.zeros(width, dtype=np.float32)                               # Creación de línea en numpy banda B8

    v4  = np.zeros(width, dtype=np.uint8)                                 # Creación de línea, supongo para enmascarar B4
    v8 = np.zeros(width, dtype=np.uint8)                                 # Creación de línea, supongo para enmascarar B8

    for y in range(height):
        b4.readPixels(0, y, width, 1, r4)                                       # Lectura de líneas de banda B4
        b8.readPixels(0, y, width, 1, r8)                                     # Lectura de línea de banda B8

        b4.readValidMask(0, y, width, 1, v4)                                    # Lectura de máscara válida para B4
        b8.readValidMask(0, y, width, 1, v8)                                  # Lectura de máscara válida para B8

        invalidMask4 = np.where(v4 == 0, 1, 0)                               # Lectura de valores inválidos B4
        invalidMask8 = np.where(v8 == 0, 1, 0)                             # Lectura de valores inválidos B4

        ma4 = np.ma.array(r4, mask=invalidMask4, fill_value=np.nan)       # Enmascarado de línea en banda B4
        ma8 = np.ma.array(r8, mask=invalidMask8, fill_value=np.nan)    # Enmascarado de línea en banda B8

        print("processing line ", y, " of ", height)                            # Muestra de procesamiento de línea
        ndvi_row = (ma8 - ma4) / (ma8 + ma4)                                  # Cómputo de la línea.
        
        ndvi = ndvi_row if y == 0 else np.vstack([ndvi, ndvi_row])              # Stackeo vertical de producto NDVI
        # np.vstack([ndvi, ndvi_row])

        # ndviBand.writePixels(0, y, width, 1, ndvi.filled(numpy.nan))            # Escritura línea de NDVI

    width=12
    height=12
    # rgb = np.dstack(band_stack)  # stacks 3 h x w arrays -> h x w x 3
    plt.figure(figsize=(width,height))
    plt.title('Producto de fecha: ' + 'NDVI ' + title, fontweight ="bold") 
    imgplot=plt.imshow(ndvi,cmap='viridis',vmin=vmin,vmax=vmax)
    plt.colorbar(imgplot)
    plt.savefig(path + '_NDVI' + '.png', bbox_inches='tight')

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

def folder_creator(root_path, folder2create, verbose):
    # Creo la variable root_folder para definir la carpeta base sobre la cual se crearán las subcarpetas del proyecto.
    root_folder = Path(root_path)
    if root_folder.exists():
        folder_list = [root_folder, folder2create]
        path2newfol = Path(*folder_list)
        path2newfol.mkdir()
    else:
        sys.exit(f'Funcion "{folder_creator.__name__()}" terminada porque no se encontró la ruta a la carpeta "{root_path}" donde debe crearse "{folder2create}"')
    if verbose:
        print(f'Creacion correcta de carpeta "{path2newfol}"')
    return path2newfol

# Lectura de dataframes de búsqueda a partir del csv

def lectura_csv(path, verbose):
    df = pd.read_csv(path)
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

# Función para mostrar atributos de productos con entrada de ruta a productos
def show_att_S2(path2prod, verbose = False):
    product = ProductIO.readProduct(path2prod)
    width = product.getSceneRasterWidth()
    height = product.getSceneRasterHeight()
    prod_name = product.getName()
    band_names = product.getBandNames()
    str_band_n = ", ".join(band_names).split(", ")
    # display(len(str_band_n), str_band_n)
    crs_raster = product.getSceneCRS()
    geocod_raster = product.getSceneGeoCoding()
    if verbose:
        print(f"Ancho: {width} px\n")
        print(f"Alto: {height} px\n")
        print(f"Nombre: {prod_name}\n")
        print(f"Cantidad de bandas: {len(str_band_n)}\n")
#         print("Muestras de proyección de producto", type(crs_raster), crs_raster, type(geocod_raster), geocod_raster, sep = '\n')
    return None

def show_att_snapobj(snap_prod, verbose = False):
    width = snap_prod.getSceneRasterWidth()
    height = snap_prod.getSceneRasterHeight()
    prod_name = snap_prod.getName()
    band_names = snap_prod.getBandNames()
    str_band_n = ", ".join(band_names).split(", ")
    # display(len(str_band_n), str_band_n)
    crs_raster = snap_prod.getSceneCRS()
    geocod_raster = snap_prod.getSceneGeoCoding()
    if verbose:
        print(f"Ancho: {width} px\n")
        print(f"Alto: {height} px\n")
        print(f"Nombre: {prod_name}\n")
        print(f"Cantidad de bandas: {len(str_band_n)}\n")
#         print("Muestras de proyección de producto", type(crs_raster), crs_raster, type(geocod_raster), geocod_raster, sep = '\n')
    return None

def subset_prod(path2prod, path2wkt, verbose):
    # Objetivo 2 del día Cortar producto por geometría
    product = ProductIO.readProduct(path2prod)
    SubsetOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
    with open(path2wkt, 'r') as f:
        wkt_orig = f.readline()
    geometry = WKTReader().read(wkt_orig)
    print(geometry)
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geometry)
    product_subset = GPF.createProduct('Subset', parameters, product)
    
    # Para debuggear
    print('Datos de producto S2 completo')
    show_att_snapobj(product, True)
    print('Datos de producto S2 recortado')
    show_att_snapobj(product_subset, True)
    return product_subset

# Función 1J
# Función de resize
def resize(product, referenceBand):
    if referenceBand == None:
        referenceBand == 'B2'
    upsamp = 'Nearest'
    downsamp = 'First'
    flag_DSamp = 'First'
    resampleOPL = 'true'

    parameters = HashMap()
#     <referenceBand>B2</referenceBand>
    parameters.put('referenceBand', referenceBand)
#     <upsampling>Nearest</upsampling>
#     <downsampling>First</downsampling>
#     <flagDownsampling>First</flagDownsampling>
#     <resampleOnPyramidLevels>true</resampleOnPyramidLevels>
    parameters.put('upsampling', upsamp)
    parameters.put('downsampling', downsamp)
    parameters.put('flagDownsampling', flag_DSamp)
    parameters.put('resampleOnPyramidLevels', resampleOPL)
    return GPF.createProduct('Resample', parameters, product)

def add_geometry2prod_3(prod, shp_path, verbose = False):
    # Implementación aconsejada en https://forum.step.esa.int/t/import-vector-data-shapefile-from-snappy-python/4115/2
    # Importar vector de un shapefile
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    parameters.put('vectorFile', shp_path)
    parameters.put('separateShapes', False)
    result = GPF.createProduct('Import-Vector', parameters, prod)
    return result

def masking(product, geometry_name, invert):
    # **Error que da origen a modificación de código**
    # expression: Undefined symbol 'cirrus_clouds'. due to Undefined symbol 'cirrus_clouds'.
    # Traceback (most recent call last):
    # File "proc_s2.py", line 109, in <module>
    # prod_s_res_msk = msnap.masking(resamp_prod, 'cirrus_clouds', False)
    # File "../utils/mod_snappy_S2.py", line 335, in masking
    # return GPF.createProduct('Land-Sea-Mask', parameters, product)
    # RuntimeError: org.esa.snap.core.gpf.OperatorException: expression: Undefined symbol 'cirrus_clouds'. due to Undefined symbol 'cirrus_clouds'.
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    parameters = HashMap()
    parameters.put('geometry', geometry_name)
    parameters.put('invertGeometry', invert)
    # parameters.put('byPass', True)
    try:
        prod_masked = GPF.createProduct('Land-Sea-Mask', parameters, product)
    except RuntimeError:
        parameters = HashMap()
        parameters.put('geometry', 'cirrus_clouds_10m')
        parameters.put('invertGeometry', invert)
        prod_masked = GPF.createProduct('Land-Sea-Mask', parameters, product)
    return prod_masked
    
# Función 1Na
# Creación de nombre de producto
def path_creator(folder, file_name, verbose):
    if verbose:
        print(f'Funcion {path_creator.__name__}')
    return os.path.join(folder, file_name)
def out_filename(filename, end, verbose = False):
    name_1 = os.path.basename(filename).split('.')[0] # Quito la cadena final '.SAFE'
    name_2 = name_1 + end # + '.dim' No necesita  la extensión final
    if verbose:
        print(f'Funcion {out_filename.__name__}')
        print(name_1)
        print(name_2)
    return name_2

# Escritura de producto (optimizada)
def writeProd(prod2write_obj, prod_path):
    WriteOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.WriteOp')
#     writeOp = WriteOp(prod_s_res_msk_roi_msk, File(output_path), 'BEAM-DIMAP')
    writeOp = WriteOp(prod2write_obj, File(prod_path), 'BEAM-DIMAP')
    writeOp.writeProduct(ProgressMonitor.NULL)
    return None

# Borro archivo temporal que bajé

def erase_tmp(path2tmp, verbose):
    if os.path.exists(path2tmp) and os.path.isfile(path2tmp):
        os.remove(path2tmp)
    if verbose:
        print(f'Borrado de archivo {path2tmp}')
    return