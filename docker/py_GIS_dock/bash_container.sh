#! /bin/bash
# Script en bash para levantar arrancar bash de docker de desarrollo en imagen gis_gvd

PATH_REPO="$(cd ../ && cd ../ && pwd)"
# PATH_REPO="$(pwd)"
PATH_SCRIPTS="${PATH_REPO}/Scripts"
PATH_VECTORES="${PATH_REPO}/Vectores"
PATH_UTILS="${PATH_REPO}/utils"
PATH_TOKEN="${PATH_REPO}/token"

# docker exec -it --name gis_gvd_bash gis_gvd bash
docker run --rm --name gis_gvd_develop \
    -it \
    -v $PATH_SCRIPTS:/src/Scripts \
    -v $PATH_VECTORES:/src/Vectores \
    -v $PATH_UTILS:/src/utils \
    -v $PATH_TOKEN:/src/token \
    --workdir /src \
    -p 8888:8888 \
    gis_gvd \
    bash
    # "jupyter" "notebook" "--allow-root"
    #'jupyter notebook'