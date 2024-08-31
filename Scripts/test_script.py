# Script para implementar conversión de kml original a nueva proyección
import sys
sys.path.append(r'../utils')
import mod_reproj_kml as mrk

## Bloque para lectura de kml de entrada
i_path = r'/src/Vectores/Tratayen.kml'
##

## Bloque para lectura de proyección de entrada
epsg_code = 32719
##

## Ingreso de parámetros en función que reproyecta

mrk.test_kml2kmlp(i_path, epsg_code, True)