#!/bin/bash

if [ ! -f "$1" ]
then
    echo "$1 not found!"
    exit 1
fi

sbsign --key keys/MOK.priv --cert keys/MOK.pem --output $1 $1
