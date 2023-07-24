#! /bin/bash

echo $PWD
echo $USER
echo $PYTHON
echo $PATH
echo $BASH_VERSION
echo $HOSTNAME
echo $COLUMNS
echo $PS1
echo $PS2

type -a python3
python3 -V

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