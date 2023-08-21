## Título proyecto: NDVI_S2_gauge 
# Autor: Gustavo V. Diaz
# Fecha inicio: 25/07/2023

### Descripción

Según lo hablado con el Licenciado Andrés Ezequiel Dolinko acerca de investigaciones llevadas a cabo por su equipo encontré una oportunidad para ayudarnos. Uno de los proyectos era ser capaces de evaluar el sistema de riego articial de alguna manera. Sobre este proyecto una de las cuestiones que falta es una manera evaluar la evolución de los cultivos con las diferentes estratégias de riego.

### Propuesta

Generar un script python/bash que sea capaz de seleccionar escenas Sentinel-2, recortar los productos seleccionados sobre la zona de interés y computar NDVI sobre dichas áreas. La intención es tener una primera aproximación para poder evaluar las estrategias utilizadas desde el 2021 (disponibilidad de datos del satélite).

### Trabajos realizados

**al 21/08/2023**

Generé entorno de python en pc de casa para poder trabajar desde allí y acceder mediante ssh a la pc de casa desde la pc de trabajo. Tuve que realizar varias acciones para poder ejecutar los notebooks, paso a describir:

1. Instalación de gdal en sistema base. Tuve que instalar la versión 3.4.3.
2. Instalación de entorno virtual python para proyecto, utilicé virsualwrapper

La acción 1 generó la necesidad de cambiar el archivo requerimientos dado que utilizaba GDAL 3.4.1. Para ello cree un nuevo archivo de requerimientos llamado requirements_casa.txt el cual cambia la versión de GDAL que necesita instalarse.

** Conclusión de jornada de trabajo **

Genera contenedor para evitar el problema recién descripto.

**al 13/08/2023**

Encaro el trabajo de bajar de a una las escenas y realizar el procesamiento para:

1. Averiguar si tiene cobertura de nubes sobre la ROI utilizando la máscara "cloud cover". Si se encuentra cubierta debería deshecharla.
2. Una vez que detecto que se encuentra limpia debería:
    1. Recortarla sobre la ROI de estudio
    2. Seleccionar las bandas que necesito
    3. Computar NDVI

15:47

Envío el producto Sentinel-2 que bajé para analizar si se encuentra la información de máscara de cloud cover dentro del producto bajado. También analizo la posiblidad de instalar esa-snappy para poder procesarla con la ayuda de SNAP engine.


**al 12/08/2023**

Logré agrandar el área de búsqueda y encontrar el procentaje de solapamiento con las escenas disponibles (listado de escenas encontradas).
Debo decidir si bajo las bandas que requiero solamente de las escenas (para cómputo de NDVI) o me contento con bajarlas totalmente y realizar la clasificación si posee nubes sobre el área de interés. Dejé asentado en notebook "Test_gdal.ipynb" los próximos trabajos a realizar. Vuelvo a citar aquí mismo,

1. Decidir entre bajar toda la escena o solo las bandas que necesite
2. Procesamiento de escenas que se bajen tal cómo,
    1. Recorte de escena
    2. Selección de bandas
    3. Cómputo de NDVI
3. Detectar si tiene o no cobertura de nubes

**al 06/08/2023**

Terminé de obtener los objetivos planteados el día 29/07/2023 en el notebook "Test_gedal.ipynb". Pude visualizar las ROIs de búsqueda y las pude superponer con los footprints de las escenas encontradas. Resta, sobre la búsqueda, poder medir el porcentaje que tiene de superposición la ROI de búsqueda respecto de las escenas. Una idea que se me ocurre es agrandar la escena de los boudaries de manera que algunas escenas no tengan el 100 de superposición y testear el funcionamiento de cálculos de porcentage de área.

**al 29/07/2023**

Me encuentro desarrollando un notebook en la carpeta scripts para generar una muestra del trabajo a realizar y relevar requerimientos, por ejemplo:

* Mostrar footprint de escena superpuesta con la ROI de interés de manera de verificar que la ROI se encuentre dentro del producto a bajar.

* Luego de generar el listado de las escenas que contienen EN SU TOTALIDAD la ROI de interés **se debe** mostrar en un gráfico temporal las escenas disponibles por fecha. El fin de esta acción es poder seleccionar las escenas que interesen.

**al 25/07/2023**

Actualmente en la carpeta de "token" se encuentran los primeros intentos para establecer:

+ Comunicación con servidores de la ESA,
    + Acceso a buscador de escenas
    + Descargador de escenas
        + Adquisición de token para bajar escenas
    

