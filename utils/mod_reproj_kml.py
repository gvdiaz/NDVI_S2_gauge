# Objetivo: Módulo python para tomar kml + código EPSG y
# * reproyectar geometría
# * Entregar WKT en nueva proyección

from osgeo import ogr
from osgeo import osr

def test_kml2kmlp(input_path, epsg_c, verbose):
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(epsg_c)
    if verbose:
        print('Presentacion de proyeccion definida:',sr, sep='\n')
        print()
        print('Presentacion de codigo EPSG', sr.GetAttrValue('AUTHORITY', 1), sep='\n')

    return None