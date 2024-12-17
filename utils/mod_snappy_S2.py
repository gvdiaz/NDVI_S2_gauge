# Para abrir y bajar archivos en lista de bajada
import pandas as pd
import os
import sys
import snappy
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF
from snappy import ProductIO
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