#!/bin/bash

BAD_HASH="af7f8e0df9cce2bc800d1ae9f5372d99"
FILES="../../docs/items-icons/*"

for fi in $FILES
do
    hash=$(md5sum $fi | awk '{ print $1 }')
    if [[ $hash == $BAD_HASH ]]
    then
        echo "Removing:" $fi
        rm $fi
    fi
done
