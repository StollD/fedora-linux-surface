# fedora-linux-surface
**IMPORTANT: This uses code / configs that are not verified to work by jakeday.**

This is a collection of random scripts and `*.spec` files that I am using to compile kernels on Fedora with [jakedays](https://github.com/jakeday/linux-surface) linux-surface patches applied.

For a DNF / YUM repository, please look here: https://gitlab.com/StollD/fedora-linux-surface-repo

## Compilation
The first thing you need to do is to clone the kernel source code, with fedoras patches applied, jakedays patch repository, and this repository
```
$ git clone git://git.kernel.org/pub/scm/linux/kernel/git/jwboyer/fedora.git
$ git clone https://github.com/jakeday/linux-surface
$ git clone https://github.com/StollD/fedora-linux-surface
```

Make sure that all repositories are in the same parent directory. Now enter the `fedora` folder and check out the branch you want to build. I am building for Fedora 30 so I am going to use `f30`
```
$ git checkout f30
```

You can now use the `build.sh` script to automatically patch and compile the kernel for you. If you have a secureboot certificate that the script should use to sign the kernel, overwrite the files in `keys/` with it. If the script sees a `MOK.priv` file in that directory, it will use it automatically.
```
$ ../fedora-linux-surface/build.sh -j4 ../linux-surface
```
Modify `-j4` to be the amount of CPU cores you want to use to build the kernel, and `../linux-surface` to be the path to jakedays repository.

## Installation
When the build completed you will find the generated RPM packages under `$HOME/rpmbuild/RPMS`. Install them and reboot into the installed kernel.
Alternatively you can check out the releases section for precompiled packages, that are already signed with my secure boot certificate. To use them with secure boot,
just import the certificate from this repository (using the `install.sh` script), or resign them using jakedays tutorial.

Required:
* [kernel](https://github.com/StollD/fedora-linux-surface/releases/tag/kernel-surface-5.0.16)
* [libwacom](https://github.com/StollD/fedora-linux-surface/releases/tag/libwacom-surface-0.33)

Optional:
* [linux-surfacegen5-button-autoremap](https://github.com/StollD/fedora-linux-surface/releases/tag/linux-surfacegen5-button-autoremap-1)

## Dependencies
Installation:
* mokutil (for `install.sh`)

Compilation:
* sbsigntools (for `sign.sh`)
* autoconf 
* automake 
* doxygen 
* libgudev1-devel 
* libtool 
* systemd-devel
* openssl-devel
