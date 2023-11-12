## Título proyecto: NDVI_S2_gauge 
# Autor: Gustavo V. Diaz
# Fecha inicio: 25/07/2023

### Descripción

Según lo hablado con el Licenciado Andrés Ezequiel Dolinko acerca de investigaciones llevadas a cabo por su equipo encontré una oportunidad para ayudarnos. Uno de los proyectos era ser capaces de evaluar el sistema de riego articial de alguna manera. Sobre este proyecto una de las cuestiones que falta es una manera evaluar la evolución de los cultivos con las diferentes estratégias de riego.

### Propuesta

Generar un script python/bash que sea capaz de seleccionar escenas Sentinel-2, recortar los productos seleccionados sobre la zona de interés y computar NDVI sobre dichas áreas. La intención es tener una primera aproximación para poder evaluar las estrategias utilizadas desde el 2021 (disponibilidad de datos del satélite).
|
### Trabajos realizados

**al 12/11/2023**
16:28

Subí modificaciones de proyecto. No pude compilar en un mismo contenedor herramientas para python 3.6 y 3.10. Me superó la situación. Ante eso comencé a implementar la idea de tener un conetendor con herramientas GIS utilizando python 3.10 y otro contenedor con snappy funcionando con python 3.6. Logré el primer objetivo con relativa facilidad.

En cuanto a la instalación de snappy está a punto de poder ser completada. En este caso lo que sucede es que comencé a utilizar todos los componentes que RV utiliza para poder compilar snappy pero al momento de crear el módulo snappy lo crea y termina la compilación pero no vuelve al símbolo del sistema. Se queda esperando algo que nunca sucede. Lamentablemente por el momento debo dejarlo allí pero está pronto a poder resolverse.

**al 17/09/2023**

19:18

Por la mañana no logré compilar snappy porque el wheel generado de jpy (que si logré compilar) tenía que ubicarse en un lugar en especial dentro de las carpetas de snap. También logré instalarlo en python 3.10 con ayuda de pip3. Aún cuando copié el wheel en la carpeta de snappy que correspondía ejecuté la línea,

```
# /snappy-conf /usr/bin/python3 /usr/local/lib/python3.10/dist-packages
```

Ahora devuelve el error 30 al intentar compilar. El log de error da lo siguiente,

```
INFO: Installing from Java module '/opt/snap/snap/modules/org-esa-snap-snap-python.jar'
WARNING: Architecture requirement possibly not met: Python is x86_64 but JVM requires amd64
INFO: Installing jpy...
INFO: Unzipping '/usr/local/lib/python3.10/dist-packages/snappy/jpy-0.15.0.dev0-cp310-cp310-linux_x86_64.whl'
INFO: Configuring jpy...
INFO: jpy Python API configuration written to '/usr/local/lib/python3.10/dist-packages/snappy/jpyconfig.py'
INFO: jpy Java API configuration written to '/usr/local/lib/python3.10/dist-packages/snappy/jpyconfig.properties'
INFO: Configuring snappy...
INFO: snappy configuration written to '/usr/local/lib/python3.10/dist-packages/snappy/snappy.ini'
INFO: Importing snappy for final test...
ERROR: Configuration failed with exit code 30
```

Hago pruebas intentando encontrar si se instaló o no el módulo pero cuando invoco snappy en python me da el siguiente mensaje,

```python
>>> import snappy
RuntimeError: jpy: internal error: static method not found: unwrapProxy(Ljava/lang/Object;)Lorg/jpy/PyObject;

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.10/dist-packages/snappy/__init__.py", line 236, in <module>
    jpy.create_jvm(options=_get_snap_jvm_options())
SystemError: <built-in function create_jvm> returned a result with an exception set
```

No encuentro la manera de que funcione. Empiezo a evaluar utilizar el plug-in de esa-snappy. Lo dejo por el día de hoy...

10:43

Logré instalar el jdk y posteriormente compilar el jpy. Pero enseguida el contendor se bloqueó y debí generar todo el proceso de compilación nuevamente.

Cuando intenté compilar el módulo jpy me saltó que no tenía instalado el paquete maven que olvidé registrar el día de hoy y el día de ayer.

Instalción de paquete maven [referencia](https://linuxhint.com/install_apache_maven_ubuntu/)

1. Arranco el contenedor con el script 'bash_container.sh'
2. Una vez dentro actualizo con el siguiente comando,
```
# apt update
```
3. Luego actualizo los paquetes que correspondan con el siguiente comando,
```
# apt upgrade
```
4. Instalo el paquete maven
```
# apt install maven -y
```
5. Pruebo nuevamente de compilar jpy

09:21
Me doy cuenta de que la instalación de java no es la que correspondía. Instalé el jre cuando debía instalar jdk (java development kit). Eso voy a hacer...

Vuelvo a encarar la instalación de jdk.

Utilizo nuevamente la guía descripta en la documentación del jpy-consortium [link](https://github.com/jpy-consortium/jpy/tree/master)

Pasos realizados,
1. Creo una nueva carpeta (/src/utils/jdk_source_true) en el contenedor para bajar los fuentes correctos.

2. Encuentro, ahora sí, el módulo de java necesario jdk 8 publicado por oracle [jdk](https://www.oracle.com/ar/java/technologies/javase/javase8u211-later-archive-downloads.html) y lo bajo mediante wget con el siguiente comando,

```
# wget -O jdk8_oracle_linux_x64.tar.gz https://www.oracle.com/ar/java/technologies/javase/javase8u211-later-archive-downloads.html#license-lightbox
```

No sirve porque oracle me obligó a generar una cuenta para bajar la versión jdk 8 de linux x64. Por lo cual tuve que hacer la cuenta bajar por mi cuenta el tar y guardarlo en la carpeta utils del contenedor (está compartida con el SO nativo).

Una vez hecho todo eso descomprimo el tar de nuevo en la carpeta /usr/java/ (dentro del contenedor) con el siguiente comando,

```
# tar zxvf jdk-8u371-linux-x64.tar.gz -C /usr/java
```

Lo hizo bien.

3. Redefino las variables de entorno,

```
# export JDK_HOME=/usr/java/jdk1.8.0_371
# export JAVA_HOME=$JDK_HOME
```

Lo verifico con el comando printenv y lo modificó correctamente.

4. Ejecuto el comando de compilación de jpy dentro de la carpeta donde bajé el proyecto jpy (se encuentra en /src/utils/jpy/jpy-master),

```
# python3 setup.py build maven bdist_wheel
```

Y lo hizo finalmente. Ya tengo compilado el jpy!!!! Continúo con la instalación de snappy en el sistema.

**al 16/09/2023**
18:00

Pude instalar el entorno de programación jre1.8.0_381 pero no pude terminar de compilar el módulo jpy. Ingresaba el siguiente comando para compilar dicho módulo,

```
# python3 setup.py build maven bdist_wheel
```

pero el contenedor me devuelve lo siguiente,

```
/src/utils/jpy/jpy-master/setup.py:25: DeprecationWarning: The distutils package is deprecated and slated for removal in Python 3.12. Use setuptools or check PEP 632 for potential alternatives
  from distutils import log
Error: environment variable "JAVA_HOME" must be set to a JDK (>= v1.7) installation directory
```

Es decir que no encuentra la instalación de java que necesita.

16:34

Leo la documentación referida en [instalación snappy 9](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface+SNAP+versions+9) y me indica que debo compilar manualmente el módulo jpy (traductor de clases de java a python y viceversa).

Cuando me encuentro leyendo la documentación me doy cuenta de que el log que necesitaba revisar no se encuentra en la instancia del contenedor porque esa instancia no fue la que se había compilado sino una nueva. Por lo cual decido correr el comando de instalación de snappy en el contenedor instanciado por el ejecutable 'bash_container.sh'.

Una vez que realicé la acción encontré el log que estaba buscando y lo copio a la carpeta de Scripts del proyecto y luego la muevo a la carpeta 'docker' y lo dejo en la subcarpeta 'aux_files'.

En el archivo snappyutil.log me indica como realizar la compilación del jpy que no fue encontrado en el sistema. La tarea que hay que realizar es,

* compilar el jpy por mí mismo
* Luego copiarlo en la siguiente carpeta dentro del contenedor
* Path: "/usr/local/lib/python3.10/dist-packages/snappy"

Para compilar dicho módulo iba a seguir los pasos pero decido primero revisar los archivos de compilación de jpy. En el [link](https://github.com/bcdev/jpy), allí me indica que el proyecto cambió de lugar [link nuevo jpy](https://github.com/jpy-consortium/jpy). En el mismo me indica cómo compilar dicho paquete,


Los pasos son los siguientes,

1. Instalar JDK 8, todavía no lo tengo así que lo instalo con los siguientes pasos indicados en el siguiente link [instalación de JDK](https://linux.how2shout.com/how-to-install-oracle-java-8-64-bit-ubuntu-22-04-20-04-lts/)
    1. Bajé el paquete java del repositorio de oracle [url_java](https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248763_8c876547113c4e4aab3c868e9e0ec572) usando wget
    2. renombro el nombre del archivo con mv, pasé del nombre a jdk8_oracle_linux_x64.tar.gz pero esto debería implementarlo directamente con el wget opción -O ([Fuente de info](https://www.quora.com/How-do-you-rename-a-downloaded-file-with-Wget-in-Linux))sería algo así
    ```
    # wget -O jdk8_oracle_linux_x64.tar.gz https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248763_8c876547113c4e4aab3c868e9e0ec572
    ```
    3. Creo el directorio donde voy a dejar la extracción
    ```
    # mkdir /usr/java
    ```
    4. Extraigo el tar en el directorio creado,
    ```
    # tar -xf jdk8_oracle_linux_x64.tar.gz -C /usr/java
    ```
    5. Agrego la ruta del ejecutable java, en esta instancia hecha se encuentra en el siguiente directorio,
    ```
    # /usr/java/jre1.8.0_381/bin/java
    ```
    Por lo cual el comando sería el siguiente,
    ```
    # echo 'export PATH="$PATH:/usr/java/jre1.8.0_381/bin"' >> ~/.bashrc
    ```
    6. Probar la instalación con el siguiente comando,
    ```
    # java -version
    ```
    Que debería devolver la versión de java utilizada
2. 



16:26

Registro lo último que sucedió el día 10/09/2023. Intenté compilar el contendor habiendo encontrado las rutas y ejecutables necesarios, pero no me permitió compilar.

El error que tira se da en el momento de ejecutar el siguiente comando,

```
# /snappy-conf /usr/bin/python3 /usr/local/lib/python3.10/dist-packages
```

Cuando lo ejecuta me devuelve lo siguiente,

```
19.61 Configuring SNAP-Python interface...                                      
20.22 java.io.IOException: Python configuration failed.
20.22 Command [/usr/bin/python3 ./snappyutil.py --snap_home /opt/snap --java_module /opt/snap/snap/modules/org-esa-snap-snap-python.jar --force --log_file ./snappyutil.log --jvm_max_mem 5G --java_home /opt/snap/jre/jre --req_arch amd64]
20.22 failed with return code 10.
20.22 Please check the log file '/usr/local/lib/python3.10/dist-packages/snappy/snappyutil.log'.
```

Por lo cual intento entrar en snappyuil.log pero el mismo no existe. Decido compilar el módulo snappy para python 3.10 y luego volver a ejecutar el comando 'snappy-conf...' bajo las indicaciones que me da el link de [instalación snappy 9](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface+SNAP+versions+9)


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
    

