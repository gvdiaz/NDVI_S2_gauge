# Script para implementar conversión de kml original a nueva proyección
import sys
sys.path.append(r'../utils')
import mod_reproj_kml as mrk

# Importo módulo os para verificar si existe el archivo generado
import os

## Bloque para lectura de kml de entrada
i_path = r'/src/Vectores/Tratayen.kml'
## Path a archivo auxiliar para guardar WKT reproyectado
o_path = r'./aux_files/wkt_reproj_file.txt'
## Path a archivo auxiliar 2 para guardar WKT original
o_path_2 = r'./aux_files/wkt_file.txt'
##

## Bloque para lectura de proyección de entrada
epsg_code = 32719
##

## Ingreso de parámetros en función que reproyecta y obtengo wkt reproyectado

wkt_reproj, wkt_orig = mrk.test_kml2kmlp(i_path, epsg_code, False)
# print(f'Verifico si se guardo algo en wkt_reproj:\n {wkt_reproj}\n y su tipo:\n {type(wkt_reproj)}')

## Guardo wkt reproyectado de salida en archivo auxiliar

with open(o_path, 'w') as f:
    f.write(wkt_reproj)

## Guardo wkt original de salida en archivo auxiliar 2

with open(o_path_2, 'w') as f:
    f.write(wkt_orig)

# print(f'Se guardo el archivo correctamente? {os.path.isfile(o_path)}' )
