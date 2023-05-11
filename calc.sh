#!/bin/sh
if [ $# -ne 1 ];then
    echo "you need 1 variable"
    exit 1
fi

docker run --rm  -it -v ${PWD}:/VSM vsmalz python3 createFig/main.py $1