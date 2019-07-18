# fedora-linux-surface
This is a collection of random scripts and `*.spec` files that I am using to 
compile kernels on Fedora with [jakedays](https://github.com/jakeday/linux-surface) 
linux-surface patches applied.

All packages that I produce from these scripts are available in a dnf 
repository so you can install and keep them up to date easily.

If you don't want to use the repository, you can get the packages directly from
the release section.

Required:
* [kernel](https://github.com/StollD/fedora-linux-surface/releases/tag/kernel-surface-5.1.18)
* [libwacom](https://github.com/StollD/fedora-linux-surface/releases/tag/libwacom-surface-0.33)
* [linux-surface-secureboot](https://github.com/StollD/fedora-linux-surface/releases/tag/linux-surface-secureboot-1)

Optional:
* [linux-surfacegen5-button-autoremap](https://github.com/StollD/fedora-linux-surface/releases/tag/linux-surfacegen5-button-autoremap-1)
* [linux-surface-control](https://github.com/StollD/fedora-linux-surface/releases/tag/linux-surface-control-0.2.2)
* [linux-surface-dtx-daemon](https://github.com/StollD/fedora-linux-surface/releases/tag/linux-surface-dtx-daemon-0.1.2)

## Installing the repository
You can add the repository to dnf using the following commands
```bash
$ sudo dnf config-manager --add-repo=https://tmsp.io/fs/repos/fedora/linux-surface/linux-surface.repo
$ sudo dnf config-manager --enablerepo linux-surface
```

## Installing linux-surface
You have to download jakedays repository and run the included `setup.sh` 
script, which installs required configuration files and binary firmware blobs 
for WiFi and touchscreen. When it asks you to install the patched libwacom and 
kernel, select no, since that would start downloading `.deb` packages that are 
useless on Fedora.
```bash
$ git clone https://github.com/jakeday/linux-surface
$ cd linux-surface
$ bash setup.sh
```
You only need to do this once and it will continue to work just fine. If 
jakeday at some point updates the script with files or commands relevant to 
your device, you should rerun it.

## Installing the kernel
First you need to install the secureboot certificate that the kernels are 
signed with. You can sign them yourselves of course and not install the 
certificate. Then, install the patched kernel and the patched libwacom 
(required for proper rotation of the Surface Pen).
```bash
$ sudo dnf install linux-surface-secureboot
$ sudo dnf install kernel-surface
$ sudo dnf install --allowerasing libwacom-surface
```

If you own a Gen 5 Surface device (SB2 / S2017 or newer), you should install 
the autorotation service for the buttons:
```bash
$ sudo dnf install linux-surfacegen5-button-autoremap
$ sudo systemctl enable surfacebook2-button-autoremap.service
```

Then, reboot the device to boot into the new kernel. At the UEFI screen, you 
will be greeted with a big blue screen, that says `MOK Management`. Confirm 
that you want to enroll my secureboot certificate. When it asks for a password 
enter `000`, then reboot. You should be able to start the surface kernel just 
fine now.

## Surface wakes up from hibernation immideately
If your surface doesn't hibernate correctly, but restarts instead, this can 
happen due to misleading signals from the USB 3.0 controller and other wakeup 
sources. You can disable them, by creating a file `/etc/systemd/system/disable-usb-wakeup.service` 
with the following content
```ini
[Unit]
Description=Disable USB wakeup triggers in /proc/acpi/wakeup

[Service]
Type=oneshot
ExecStart=/bin/sh -c "echo EHC1 > /proc/acpi/wakeup; echo EHC2 > /proc/acpi/wakeup; echo XHC > /proc/acpi/wakeup"
ExecStop=/bin/sh -c "echo EHC1 > /proc/acpi/wakeup; echo EHC2 > /proc/acpi/wakeup; echo XHC > /proc/acpi/wakeup"
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```
and enabling / starting the service
```bash
$ sudo systemctl enable disable-usb-wakeup.service
$ sudo systemctl start disable-usb-wakeup.service
```
Your surface should now hibernate correctly.

## Building the kernel yourself
The first thing you need to do is to clone the kernel source code, with fedoras 
patches applied, jakedays patch repository, and this repository
```
$ git clone https://git.kernel.org/pub/scm/linux/kernel/git/jwboyer/fedora.git
$ git clone https://github.com/jakeday/linux-surface
$ git clone https://github.com/StollD/fedora-linux-surface
```

Make sure that all repositories are in the same parent directory. Now enter the 
`fedora` folder and check out the branch you want to build.
```
$ git checkout fxy
```

You can now use the `build.sh` script to automatically patch and compile the 
kernel for you. If you have a secureboot certificate that the script should use 
to sign the kernel, overwrite the files in `keys/` with it. If the script sees 
a `MOK.priv` file in that directory, it will use it automatically.
```
$ ../fedora-linux-surface/build.sh -j4 ../linux-surface
```
Modify `-j4` to be the amount of CPU cores you want to use to build the kernel, 
and `../linux-surface` to be the path to jakedays repository.

When the build completed you will find the generated RPM packages under 
`$HOME/rpmbuild/RPMS`. Install them and reboot into the installed kernel.
Alternatively you can check out the releases section for precompiled packages, 
that are already signed with my secure boot certificate. To use them with 
secure boot, just import the certificate from this repository (using the 
`install.sh` script), or resign them using jakedays tutorial.

## Dependencies (for manual installation / compilation)
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
* flex
* bison
