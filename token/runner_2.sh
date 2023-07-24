#! /bin/bash

PATH_2="/home/negrete/test_gee/token/"
file="get_token.sh"
program=python3

file_p="${PATH_2}${file}"
# echo "${file_p} acá lo veo"
python3 -V
if test -f "${file_p}" ; then
    echo "${file_p} exists."
    # /bin/bash python3 -c "import sys; print(sys.path)"
    /usr/bin/python3 -c "import sys; print(sys.path)"
    type -a ${program}
    python3 -V
fi