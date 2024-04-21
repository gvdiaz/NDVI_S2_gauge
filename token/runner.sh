#! /bin/bash
PATH_1=""
PATH_2="./"
PATH_3="../Scripts/aux_files/"
file="get_token.sh"
out_file="token_dict.txt"
out_file_2="keycloak.txt"
out_file_3="search_s2_df.pkl"
program=python3
file_py="token_decoder.py"
file_2_py="token_getter.py"
file_3_py="downloader_prods.py"
user="gus838@gmail.com"
pass="Ul!RsPWTPuw3"
verbose="False"

# Activo entorno virtual de python (realizado a través del alias de "mi" sesión)
# dload_s2 #-> no funciona

file_p="${PATH_2}${file}"
file_p_py="${PATH_2}${file_py}"
file_p_2_py="${PATH_2}${file_2_py}"
file_p_3_py="${PATH_1}${file_3_py}"
token_p="${PATH_2}${out_file}"
keycloak_p="${PATH_2}${out_file_2}"
prod_id_p="${PATH_3}${out_file_3}"

echo ${file_p_2_py}
# [ test -f "${file_p_2_py}" ] && echo "true" || echo "false"

# echo "Tiempo de inicio de script " ${file_2_py}
# echo $(date)
# echo

# Modificación de script creador de get_token.sh (Agrego user y pass a requisidor)
if test -f "${file_p_2_py}" ; then
    echo "${file_p_2_py} exists."
    # /bin/bash python3 -c "import sys; print(sys.path)"
    # /usr/bin/python3 -c "import sys; print(sys.path)"
    # type -a ${program}
    python3 ${file_p_2_py} ${user} ${pass} ${keycloak_p}
    chmod 777 ${file_p}
fi

# echo "Visualización de keycloak"
# cat $keycloak_p
# echo
# echo "Fecha de última modificaión"
# date -r $keycloak_p
# echo
export KEYCLOAK_TOKEN=$(cat ${keycloak_p})
# echo "Variable KEYCLOAK_TOKEN"
# echo $KEYCLOAK_TOKEN

# echo "Tiempo de inicio de script " ${file}
# echo $(date)
# echo

# Pedido de token y guardado en archivo out_file_p
# python3 "${file_p_2_py} ${user} ${pass}"
${file_p} > ${token_p}

# echo "Visualización de keycloak (con curl)"
# cat $token_p
# echo
# echo "Fecha de última modificaión"
# date -r $token_p
# echo

# ls -aol

# Verifico si existe out_file_p (archivo con token) y
if test -f "${token_p}" ; then
    echo "${token_p} exists."
    # /bin/bash python3 -c "import sys; print(sys.path)"
    # /usr/bin/python3 -c "import sys; print(sys.path)"
    # type -a ${program}
    # python3 ${file_p_py} ${token_p} ${keycloak_p} ${prod_id_p}
    python3 ${file_p_3_py} ${token_p} ${keycloak_p} ${prod_id_p} ${user} ${pass} ${verbose}
fi

# echo ${KEYCLOAK_TOKEN}
# printenv KEYCLOAK_TOKEN

# deactivate #-> no funciona