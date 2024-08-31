# Objetivo: Módulo python para tomar kml + código EPSG y
# * reproyectar geometría
# * Entregar WKT en nueva proyección

from osgeo import ogr   # Módulo para procesar datos vectoriales
from osgeo import osr   # Módulo para generar objetos de sistema de referencia
from osgeo import gdal  # Módulo para realizar la reproyección de la geometría elegida

# Módulos necesarios para procesamiento
import sys

def test_kml2kmlp(input_path, epsg_c, verbose=False):
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(epsg_c)
    get_wkt_V1(input_path, sr, verbose)
    if verbose:
        print('Presentacion de proyeccion definida:',sr, sep='\n')
        print()
        print('Presentacion de codigo EPSG', sr.GetAttrValue('AUTHORITY', 1), sep='\n')

    return None

def get_wkt_V1(file2read, reproj_sr, verbose=False):
    # Por el momento solo devuelve la geometría de la primer feature (suponiendo que es polígono)
    # file2read = get_kml_name(search_folder)
    # Primer versión de lector de wkt, busca la geometría del primer feature de la capa

    ## Apertura de dataset enviado (se espera datos vectoriales en polígono)
    ds = ogr.Open(file2read, 0)
    if ds is None:
        sys.exit(f'No se puede abrir el archivo {fn}')
    

    lyr = ds.GetLayer(0)

    for feature in lyr:
        geometry = feature.GetGeometryRef()
        print('Tipo de geometria: ',geometry.GetGeometryName())
        geom_wkt = geometry.ExportToWkt()
        spatial_ref_auth = geometry.GetSpatialReference().GetAttrValue('AUTHORITY')
        spatial_ref_code = geometry.GetSpatialReference().GetAttrValue('AUTHORITY', 1)
        crs = spatial_ref_auth + ':' +  spatial_ref_code

        # Reproyección de geometría y entrega de wkt nuevo
        gdal.SetConfigOption('OGR_ENABLE_PARTIAL_REPROJECTION', 'TRUE') ## Escribir más prolijo, acá se pierde en código
        geometry.TransformTo(reproj_sr)
        geom_wkt_rp = geometry.ExportToWkt()
        break
        # geom_list.append((geom_wkt, crs))
        # break00
    if verbose:
        # Visualización de campos disponibles
        print('Tipos de campos disponibles')
        for field in lyr.schema:
            print(field.name, field.GetTypeName(), sep ='\t'*2)
        # Visualización de tipo de geometría
        print()
        print('Tipo de geometria de capa: ', lyr.GetGeomType())
        print()
        print('Visualizacion de referencia espacial', lyr.GetSpatialRef(), sep = '\n')
        print()
        print('Visualizacion de geometrias')
        # print(geometry.GetGeometryName())
        print(geom_wkt)
        print('Visualizacion de geometrias reproyectadas')
        # print(geometry.GetGeometryName())
        print(geom_wkt_rp)
        
    del ds
    # return geom_wkt, crs
    return None