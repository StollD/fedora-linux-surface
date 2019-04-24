#!/bin/sh

DIR=$(dirname "$0")

# Install the secure boot certificate
sudo mokutil --import $DIR/keys/MOK.der

# TODO: Eventually install a custom repository for the packages?
