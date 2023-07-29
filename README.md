## Título proyecto: NDVI_S2_gauge 
# Autor: Gustavo V. Diaz
# Fecha inicio: 25/07/2023

### Descripción

Según lo hablado con el Licenciado Andrés Ezequiel Dolinko acerca de investigaciones llevadas a cabo por su equipo encontré una oportunidad para ayudarnos. Uno de los proyectos era ser capaces de evaluar el sistema de riego articial de alguna manera. Sobre este proyecto una de las cuestiones que falta es una manera evaluar la evolución de los cultivos con las diferentes estratégias de riego.

### Propuesta

Generar un script python/bash que sea capaz de seleccionar escenas Sentinel-2, recortar los productos seleccionados sobre la zona de interés y computar NDVI sobre dichas áreas. La intención es tener una primera aproximación para poder evaluar las estrategias utilizadas desde el 2021 (disponibilidad de datos del satélite).

### Trabajos realizados

**al 29/07/2023**

Me encuentro generado un notebook en la carpeta scripts para generar una muestra del trabajo a realizar y relevar requerimientos, por ejemplo:

* Mostrar footprint de escena superpuesta con la ROI de interés de manera de verificar que la ROI se encuentre dentro del producto a bajar.

* Luego de generar el listado de las escenas que contienen EN SU TOTALIDAD la ROI de interés **se debe** mostrar en un gráfico temporal las escenas disponibles por fecha. El fin de esta acción es poder seleccionar las escenas que interesen.

**al 25/07/2023**

Actualmente en la carpeta de "token" se encuentran los primeros intentos para establecer:

+ Comunicación con servidores de la ESA,
    + Acceso a buscador de escenas
    + Descargador de escenas
        + Adquisición de token para bajar escenas
    

