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
##

## Bloque para lectura de proyección de entrada
epsg_code = 32719
##

## Ingreso de parámetros en función que reproyecta y obtengo wkt reproyectado

wkt_reproj = mrk.test_kml2kmlp(i_path, epsg_code, True)
print(f'Verifico si se guardo algo en wkt_reproj:\n {wkt_reproj}\n y su tipo:\n {type(wkt_reproj)}')

## Guardo wkt de salida en archivo auxiliar

with open(o_path, 'w') as f:
    f.write(wkt_reproj)

print(f'Se guardo el archivo correctamente? {os.path.isfile(o_path)}' )
