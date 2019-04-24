#!/bin/bash

if [ ! -f "$1" ]
then
    echo "$1 not found!"
    exit 1
fi

DIR=$(dirname "$0")
sbsign --key $DIR/keys/MOK.priv --cert $DIR/keys/MOK.pem --output $1 $1
