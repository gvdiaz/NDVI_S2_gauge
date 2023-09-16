## Título proyecto: NDVI_S2_gauge 
# Autor: Gustavo V. Diaz
# Fecha inicio: 25/07/2023

### Descripción

Según lo hablado con el Licenciado Andrés Ezequiel Dolinko acerca de investigaciones llevadas a cabo por su equipo encontré una oportunidad para ayudarnos. Uno de los proyectos era ser capaces de evaluar el sistema de riego articial de alguna manera. Sobre este proyecto una de las cuestiones que falta es una manera evaluar la evolución de los cultivos con las diferentes estratégias de riego.

### Propuesta

Generar un script python/bash que sea capaz de seleccionar escenas Sentinel-2, recortar los productos seleccionados sobre la zona de interés y computar NDVI sobre dichas áreas. La intención es tener una primera aproximación para poder evaluar las estrategias utilizadas desde el 2021 (disponibilidad de datos del satélite).
|
### Trabajos realizados

**al 10/09/2023**

17:02

También debí encontrar la ruta donde se encontraba el archivo 'snap-conf'. Para ello utilicé la siguiente función,

```
# find / -name snappy-conf
```

Que me entregó la ruta '/opt/snap/bin/snappy-conf'.

Por último, creo, debo decidir donde agregar el módulo snappy de python para que lo encuentre. Para ello me valgo de ejecutar una instancia de python e importar el módulo sys para ver donde búsca los módulos. Esta ejecución me devuelve las siguientes rutas,

```
['', '/usr/lib/python310.zip', '/usr/lib/python3.10', '/usr/lib/python3.10/lib-dynload', '/usr/local/lib/python3.10/dist-packages', '/usr/lib/python3/dist-packages']
```

Por lo cual la línea a agregar para la compilación sería la siguiente,

```
RUN ./snappy-conf /usr/bin/python3 /usr/local/lib/python3.10/dist-packages
```

Pruebo a ver que me da...

16:40

Para hacer funcionar el módulo snappy la documentación me indica que debo ejecutar el siguiente comando,

```
./snappy-conf <python-exe> <snappy-dir>
```

donde python-exe sería la ubicación del ejecutable de python. Para ello debí desarrollar otro script que me permita entrar al bash del contenedor y ejecutar el siguiente comando,

```
$ which python3
```

de modo de conocer la ubicación del ejecutable. Cómo resultado dió la ubicación '/usr/bin/python3'. La cual utilizaré para ejecutar esa línea en el build y recompilar el contenedor.

16:28

Encuentro la referencia de snappy y como configurarlo luego de la instalación en el siguiente [link](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface+SNAP+versions+9). Voy a implementarla.

Agrego que también encontré la página de referencia que enseña a utilizar el módulo snappy en el siguiente [link](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/19300362/How+to+use+the+SNAP+API+from+Python)

16:22

Logré hacer funcionar el contenedor con el servidor jupyter y ver las carpetas necesarias para desarrollo. Continúo por hacer funcionar los ejemplos de snappy dentro del contenedor.

**al 09/09/2023**

Trabajé a distancia con la pc del laburo. Dado que no tengo instalado docker ni compilado el docker que desarrollé la semana pasada encaré el trabajo en la pc del laburo realicé las siguientes acciones para poder hacerlo,

* Bajé una escena sentinel-2 a la pc para poder procesarla con snappy
* Instalé el módulo snappy 9 en la pc del laburo pero queda pendiente terminar la instalación confiugrando el snap-config. Dejo la página de referencia [instalación snappy](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface+SNAP+versions+9)
* Lectura de implementación de snappy. [foro snappy](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/8847381/Developer+Guide)

OBJETIVO: En los próximos días debería poner en funcionamiento el módulo snappy y luego probar el funcionamiento dentro de la instalación de docker.

**al 03/09/2023**

Recopilación de acciones al día de hoy y sus racionales,

* Agrego en dockerfile paquete software-properties-common para poder utilizar el add-apt-repository que necesita la instalción de GDAL para agregar el repositorio ubuntugis:ppa. [link de ayuda](https://itsfoss.com/add-apt-repository-command-not-found/)

* Surtió efecto agregar el paquete pero al mantener la versión 3.9 de python, pip no encuentra ciertos paquetes que utilicé en el desarrollo de las herramientas utilizadas para el buscador de escenas. Por lo cual a medida que va fallando la instalación de paquetes voy quitando la especificación de versión de los paquetes que no los encuentra. [link paquetes disponibles en distros de Ubuntu](https://packages.ubuntu.com/)

* Son cuatro los paquetes que no puedo instalar. En este punto decido modificar tres aspectos de compilación,

    1. Cambiar versión de python a 3.10 para mantener las versiones originales de requirements_casa.txt.
    2. Volver a indicar las versiones de los paquetes, ahora que los va a poder encontrar.
    3. Cambiar la versión de ubuntu porque Ubuntu focal (20.04) no cuenta con el paquete python3.10-dev. Por lo cual tuve que volver a compilar todo con Ubuntu jammy (22.04LTS) 

**Resultado:**

Logré compilar primer versión de docker. Los pasos a seguir son desarrollar los scripts para lanzar el contendedor ya sea en,

* Desarrollo: Lanzar notebook jupyter con acceso a todos los paquetes de python instalados, sobretodo el de snappy
* Ejecución: Ejecutar script con y dejar registro de de acciones realizadas durante ejecución.

**al 26/08/2023**

Creo en pc de casa usuario "black_dock" en SO Ubuntu nativo para poder ejecutar con privilegios los comandos de docker.

También creé archivos de configuración inicial en repositorio de manera de comenzar a desarrollar contenedor que sirva para ejecución de procesamiento o desarrollo. Esto último se puede llegar a elegir en el run que ejecute un script o lance un notebook.

PENDIENTE:

* Definir distribución de linux a utilizar (ubuntu, debian o alguna otra, tal vez alpine para probar)
* Definir paquetes de python a incluir
* Elección de snappy (¿10?) a utilizar

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
    

