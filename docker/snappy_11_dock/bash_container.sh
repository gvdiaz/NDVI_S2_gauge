#! /bin/bash
# Script en bash para levantar arrancar bash de docker de desarrollo en imagen snappy_11_gvd

PATH_REPO="$(cd ../ && cd ../ && pwd)"
PATH_SCRIPTS="${PATH_REPO}/Scripts"
PATH_VECTORES="${PATH_REPO}/Vectores"
PATH_UTILS="${PATH_REPO}/utils"
PATH_TOKEN="${PATH_REPO}/token"
PATH_OUTPUT="${PATH_REPO}/output"

# bash en imagen snappy_11_gvd
docker run --rm --name snappy_11_develop \
    -it \
    -v $PATH_SCRIPTS:/src/Scripts \
    -v $PATH_VECTORES:/src/Vectores \
    -v $PATH_UTILS:/src/utils \
    -v $PATH_TOKEN:/src/token \
    -v $PATH_OUTPUT:/src/output \
    --workdir /src \
    snappy_11_gvd \
    bash
    # Agregar siguiente línea para habilitar el puerto 8888:8888 para cuando tenga el notebook funcionando.
    # -p 8888:8888 \
    # "jupyter" "notebook" "--allow-root"
    #'jupyter notebook'