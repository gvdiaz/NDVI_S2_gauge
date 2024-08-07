#! /bin/bash
# Script en bash para levantar sevidor jupyter de docker de desarrollo en imagen gis_gvd
# Aprendizaje
#   Opciones de docker run:
#   -d (detach): Run container in background and print container ID
#   --rm: Automatically remove the container when it exits
#   --name (name string): Automatically remove the container when it exits
#   --net (network network): Connect a container to a network
#   -i (--interactive ): Keep STDIN open even if not attached
#   -t (--tty): Allocate a pseudo-TTY
#   -v (-volume list): Bind mount a volume
#   --workdir string: Working directory inside the container

# echo $PWD
PATH_REPO="$(cd ../ && cd ../ && pwd)"
# PATH_REPO="$(cd ../ && pwd)"
# PATH_REPO="$(pwd)"
PATH_SCRIPTS="${PATH_REPO}/Scripts"
PATH_VECTORES="${PATH_REPO}/Vectores"
PATH_UTILS="${PATH_REPO}/utils"
PATH_TOKEN="${PATH_REPO}/token"
PATH_OUTPUT="${PATH_REPO}/output"

# echo $PATH_REPO $PATH_SCRIPTS
docker run --rm --name gis_gvd_develop \
    -it \
    -v $PATH_SCRIPTS:/src/Scripts \
    -v $PATH_VECTORES:/src/Vectores \
    -v $PATH_UTILS:/src/utils \
    -v $PATH_TOKEN:/src/token \
    -v $PATH_OUTPUT:/src/Output \
    --workdir /src/Scripts \
    gis_gvd \
    "python3" "searcher_filter.py"
    # "jupyter" "notebook" "--allow-root"
    #'jupyter notebook'