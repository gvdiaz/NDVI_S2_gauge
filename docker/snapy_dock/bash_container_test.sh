#! /bin/bash
# Script en bash para levantar arrancar bash de docker de desarrollo en imagen snappy_9_gvd

PATH_REPO="$(cd ../ && cd ../ && pwd)"
PATH_SCRIPTS="${PATH_REPO}/Scripts"
PATH_VECTORES="${PATH_REPO}/Vectores"
PATH_UTILS="${PATH_REPO}/utils"
PATH_TOKEN="${PATH_REPO}/token"

# bash en imagen snappy_9_gvd
docker run --rm --name snappy_develop \
    -it \
    -v $PATH_SCRIPTS:/src/Scripts \
    -v $PATH_VECTORES:/src/Vectores \
    -v $PATH_UTILS:/src/utils \
    -v $PATH_TOKEN:/src/token \
    --workdir /src \
    -p 8888:8888 \
    snappy_9_gvd_test \
    bash
    # "jupyter" "notebook" "--allow-root"
    #'jupyter notebook'