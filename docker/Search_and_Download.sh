#! /bin/bash
# Script bash para arrancar scripts de buscado y bajado
# Fecha: 11/02/2025
# Autor: Gustavo V. Diaz

PATH_REPO="$(cd ..&& pwd)"
# PATH_REPO="$(cd ../ && pwd)"
# PATH_REPO="$(pwd)"
# PATH_REPO="${}"
PATH_PY_GIS="${PATH_REPO}/docker/py_GIS_dock/"
SEARCH_SCRIPT="search_filt_runner.sh"
PATH_SNAPPY="${PATH_REPO}/docker/snapy_dock/"
PROC_SCRIPT="downloader_and_proc.sh"
# Me situo sobre la carpeta REPO
cd ${PATH_REPO}
# echo "Directorio para repo: $(pwd)"
# pwd
# echo ${PATH_REPO}
cd ${PATH_PY_GIS}
sudo ./${SEARCH_SCRIPT}
# echo "Directorio para py_GIS_dock: $(pwd)"
# pwd
# echo ${PATH_PY_GIS}
cd ${PATH_SNAPPY}
sudo ./${PROC_SCRIPT}
# echo "Directorio para snapy_dock: $(pwd)"
# pwd
# echo ${PATH_SNAPPY}


