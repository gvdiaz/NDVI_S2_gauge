#! /bin/bash
PATH_1=""
PATH_2="./"
PATH_3="../Output/"
file="get_token.sh"
out_file="token_dict.txt"
out_file_2="keycloak.txt"
out_file_3="prod_id_selected.txt"
program=python3
file_py="token_decoder.py"
file_2_py="token_getter.py"
user="gus838@gmail.com"
pass="Ul!RsPWTPuw3"

# Activo entorno virtual de python (realizado a través del alias de "mi" sesión)
# dload_s2 #-> no funciona

file_p="${PATH_2}${file}"
file_p_py="${PATH_2}${file_py}"
file_p_2_py="${PATH_2}${file_2_py}"
token_p="${PATH_2}${out_file}"
keycloak_p="${PATH_2}${out_file_2}"
prod_id_p="${PATH_3}${out_file_3}"

echo ${file_p_2_py}
# [ test -f "${file_p_2_py}" ] && echo "true" || echo "false"

# Modificación de script creador de get_token.sh (Agrego user y pass a requisidor)
if test -f "${file_p_2_py}" ; then
    echo "${file_p_2_py} exists."
    # /bin/bash python3 -c "import sys; print(sys.path)"
    # /usr/bin/python3 -c "import sys; print(sys.path)"
    # type -a ${program}
    python3 ${file_p_2_py} ${user} ${pass} ${keycloak_p}
    chmod 777 ${file_p}
fi

export KEYCLOAK_TOKEN=$(cat ${keycloak_p})
# echo "Variable KEYCLOAK_TOKEN"
# echo $KEYCLOAK_TOKEN

# Pedido de token y guardado en archivo out_file_p
# python3 "${file_p_2_py} ${user} ${pass}"
${file_p} > ${token_p}

# ls -aol

# Verifico si existe out_file_p (archivo con token) y
if test -f "${token_p}" ; then
    echo "${token_p} exists."
    # /bin/bash python3 -c "import sys; print(sys.path)"
    # /usr/bin/python3 -c "import sys; print(sys.path)"
    # type -a ${program}
    python3 ${file_p_py} ${token_p} ${keycloak_p} ${prod_id_p}
fi

# echo ${KEYCLOAK_TOKEN}
# printenv KEYCLOAK_TOKEN

# deactivate #-> no funciona