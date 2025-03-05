#! /bin/bash
# Script bash para arrancar scripts de buscado y bajado
# Fecha: 03/03/2025
# Autor: Gustavo V. Diaz

# PATHS
PATH_REPO="$(cd ..&& pwd)"
# PATH_REPO="$(cd ../ && pwd)"
# PATH_REPO="$(pwd)"
# PATH_REPO="${}"
PATH_PY_GIS="${PATH_REPO}/docker/py_GIS_dock/"
PATH_SNAPPY="${PATH_REPO}/docker/snapy_dock/"
PROC_CONF="${PATH_REPO}/utils/CONF_PROC.INI"
PATH_OUTPUT="${PATH_REPO}/output/"

# SCRIPTS BASH
PYTHON_LAUNCHER="python_36_launcher.sh"
PROC_SCRIPT="downloader_and_proc.sh"
SEARCH_SCRIPT="search_filt_runner.sh"

# SCRIPTS PYTHON3
FOLDER_CREATOR="folder_creator.py"

# Me situo sobre la carpeta REPO
# cd ${PATH_REPO}
# echo "Directorio para repo: $(pwd)"
# pwd
# echo ${PATH_REPO}
cd ${PATH_PY_GIS}
# sudo ./${SEARCH_SCRIPT}
# echo "Directorio para py_GIS_dock: $(pwd)"
# pwd
# echo ${PATH_PY_GIS}
cd ${PATH_SNAPPY}

# sudo ./${PYTHON_LAUNCHER} ${FOLDER_CREATOR}

REL_PATH2LIST=$(sudo ./${PYTHON_LAUNCHER} ${FOLDER_CREATOR})
# echo ${REL_PATH2LIST}
PATH2LIST="${PATH_OUTPUT}${REL_PATH2LIST}"
echo $PATH2LIST
cat $PATH2LIST
# echo "Directorio para snapy_dock: $(pwd)"
# pwd
# echo ${PATH_SNAPPY}

while IFS= read -r line; do
    # echo "Line: $line"
    if [[ "$line" == prods_list* ]]; then
        echo $line
        path="${line}"
        filename=$(basename "$path")
        path_bash="${PATH_OUTPUT}${filename}"
        echo $path_bash
        line_count="Cantida de lineas en $path_bash"
        # cat $path_bash
        echo $line_count
        lines=$(($(wc -l < "$path_bash") - 1 ))
        echo $lines

    fi
done < $PROC_CONF

# line_count=$(wc -l < "$file")