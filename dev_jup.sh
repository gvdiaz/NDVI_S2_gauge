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
PATH_REPO="$(cd ../ && pwd)"
PATH_SCRIPTS="${PATH_REPO}/Scripts"

# echo $PATH_REPO $PATH_SCRIPTS
docker run --rm --name gis_gvd_develop \
    -it \
    -v $PATH_SCRIPTS:/src/Scripts \
    --workdir /src \
    -p 8888:8888 \
    gis_gvd \
    "jupyter" "notebook" "--allow-root"
    #'jupyter notebook'