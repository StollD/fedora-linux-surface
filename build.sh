#!/bin/sh

DIR=$(dirname "$0")
KERNELVERSION=$(make -s kernelversion | cut -d'-' -f1)
KERNELBUILD=$(($(cat .version 2>/dev/null || echo 0) + 1))
FEDORAVER=$(. /etc/os-release && echo $VERSION_ID)

usage() {
	echo "Usage: $0 [OPTION]..."
	echo "Patches a kernel source with linux-surfaces and packages it for Fedora."
	echo
	echo "Options:"
	echo "	-h	This help message"
	echo "	-j	The amounts of threads to use for compiling"
	echo "	-s	The path where the patchfiles are located"
	echo "	-p	Force a specific patchset to be used"
	echo "	-r	Force a specific release to be used"
	exit
}

while getopts ":h:j:s:p:r:" args; do
	case "$args" in
	s)
		SOURCE=$OPTARG
		;;
	j)
		THREADS=$OPTARG
		;;
	p)
		PATCHSET=$OPTARG
		;;
	r)
		KERNELBUILD=$OPTARG
		;;
	h|*)
		usage
		;;
	esac
done
shift $((OPTIND-1))

# If no source was specified, do nothing
if [ "$SOURCE" = "" ]; then
	usage
fi

# If not threads where specified, use 4
if [ "$THREADS" = "" ]; then
	THREADS=4
fi

# Figure out which patchset to use
if [ "$PATCHSET" = "" ]; then
	PATCHSET=$(echo $KERNELVERSION | cut -d'.' -f1,2)
fi

# Check if the patches exist
if [ ! -d "$SOURCE/patches/$PATCHSET" ]; then
	echo "ERROR: Patcheset $SOURCE/patches/$PATCHSET not found!"
	exit -2
fi

# Undo all changes
git reset --hard HEAD
git clean -df

# Apply jakedays patches
for i in $SOURCE/patches/$PATCHSET/*.patch
do
	patch -p1 < $i
done

# Apply our own patches
for i in $DIR/patches/$PATCHSET/*.patch
do
	patch -p1 < $i
done

# Apply the surface config
scripts/kconfig/merge_config.sh -m 				\
	fedora/configs/kernel-$KERNELVERSION-x86_64.config	\
	$DIR/config.surface

# Generate the kernel version string
KVER="-$KERNELBUILD.surface.fc$FEDORAVER.x86_64"

# Update version
echo $(($KERNELBUILD - 1)) > .version

# Compile the kernel
make -j$THREADS all LOCALVERSION=$KVER

# Sign the compiled vmlinuz image
if [ -f $DIR/keys/MOK.priv ]; then
	IMAGE=$(make -s image_name)
	sbsign --key $DIR/keys/MOK.priv --cert $DIR/keys/MOK.pem	\
		--output $IMAGE $IMAGE
fi

# Package the kernel as .rpm
make -j$THREADS binrpm-pkg LOCALVERSION=$KVER
