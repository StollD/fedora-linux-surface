#!/bin/sh

MAKEFLAGS=$1
DIR=$(dirname "$0")
JAKEDAY=$2
PATCHSET=$3
KERNELVERSION=$(make -s kernelversion | cut -d'-' -f1)

# Undo all changes
git reset --hard HEAD
git clean -df

# Figure out which patchset to use
if [ "$PATCHSET" = "" ]; then
    PATCHSET=$(echo $KERNELVERSION | cut -d'.' -f1).$(echo $KERNELVERSION | cut -d'.' -f2)
fi

# Apply jakedays patches
for i in $JAKEDAY/patches/$PATCHSET/*.patch
do
    patch -p1 < $i
done

# Apply our own patches
for i in $DIR/patches/*.patch
do
    patch -p1 < $i
done

# Apply the surface config
scripts/kconfig/merge_config.sh -m fedora/configs/kernel-$KERNELVERSION-x86_64.config $DIR/config.surface

# Compile the kernel
make $MAKEFLAGS all LOCALVERSION=-surface

# Sign the compiled vmlinuz image
if [ -f $DIR/keys/MOK.priv ]; then
    $DIR/sign.sh $(make -s image_name)
fi

# Package the kernel as .rpm
make $MAKEFLAGS binrpm-pkg LOCALVERSION=-surface
