%global pkg_version 20190927
%global pkg_release 1
%global pkg_source https://github.com/StollD/fedora-linux-surface

%global sb_password surface

Name:		linux-surface-secureboot
Summary:	The secureboot certificate for kernel-surface
License:	GPLv2
BuildArch:	noarch
Requires:	mokutil

Version:	%{pkg_version}
Release:	%{pkg_release}%{?dist}
URL:		%{pkg_source}
Source0:	StollD.cer

%description
This package installs the secureboot certificate that is used to sign the kernel
from the kernel-surface package. When you reboot for the first time, it will ask
you to enroll the MOK certificate. Please check if the key is really mine, and
then confirm the import by entering "%{sb_password}" as the password.

%prep
%setup -q -c -T

%global cert_dir /usr/share/linux-surface-secureboot

%install
rm -rf %{buildroot}
install -dm 755 %{buildroot}%{cert_dir}
install -pm 644 %{SOURCE0} %{buildroot}%{cert_dir}

%pre

# Upgrading
if [ "$1" = "2" ]; then
	cp %{cert_dir}/StollD.cer %{cert_dir}/StollD.cer.bak
	cmp --silent %{cert_dir}/StollD.cer %{cert_dir}/StollD.cer.bak
	echo $?
fi

%post

# First installation
if [ ! -f "%{cert_dir}/StollD.cer.bak" ]; then
	echo ""
	echo "The secure-boot certificate has been installed to:"
	echo ""
	echo "	%{cert_dir}/StollD.cer"
	echo ""
	echo "It will now be automatically enrolled for you and guarded with the password:"
	echo ""
	echo "	%{sb_password}"
	echo ""

	HASHFILE=$(mktemp)
	mokutil --generate-hash=%{sb_password} > $HASHFILE
	mokutil --hash-file $HASHFILE --import %{cert_dir}/StollD.cer

	echo "To finish the enrollment process you need to reboot, where you will then be"
	echo "asked to enroll the certificate. During the import, you will be prompted for"
	echo "the password mentioned above. Please make sure that you are indeed adding"
	echo "the right key and confirm by entering '%{sb_password}'."
	echo ""
	echo "Note that you can always manage your secure-boot keys, including the one"
	echo "just enrolled, from inside Linux via the 'mokutil' tool."
	echo ""
elif ! cmp --silent %{cert_dir}/StollD.cer %{cert_dir}/StollD.cer.bak; then
	echo ""
	echo "Updating secure boot certificate. The old key will be revoked and a new key"
	echo "will be installed. You will need to reboot your system, where you will then"
	echo "be asked to delete the old and import the new key. In both cases, make sure"
	echo "this is the right key and confirm with the password '%{sb_password}'."
	echo ""

	HASHFILE=$(mktemp)
	mokutil --generate-hash=%{sb_password} > $HASHFILE
	mokutil --hash-file $HASHFILE --import %{cert_dir}/StollD.cer
	mokutil --hash-file $HASHFILE --delete %{cert_dir}/StollD.cer.bak
	rm -f %{cert_dir}/StollD.cer.bak
else
	rm -f %{cert_dir}/StollD.cer.bak
fi

%preun

# Last version is being removed
if [ "$1" = "0" ]; then
	echo ""
	echo "The following secure-boot certificate will be uninstalled and revoked from:"
	echo "your system"
	echo ""
	echo "	%{cert_dir}/StollD.cer"
	echo ""

	HASHFILE=$(mktemp)
	mokutil --generate-hash=%{sb_password} > $HASHFILE
	mokutil --hash-file $HASHFILE --delete %{cert_dir}/StollD.cer

	echo "The key will be revoked on the next start of your system. You will then"
	echo "again asked for the password. Enter '%{sb_password}' to confirm."
	echo ""
	echo "Kernels signed with the corresponding private key will still not be allowed"
	echo "to boot after this. Note that you can always manage your secure-boot keys"
	echo "via the 'mokutil' tool. Please refer to 'man mokutil' for more information."
	echo ""
fi


%files
%{cert_dir}/StollD.cer

%changelog
* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update to match qzed's version for Arch

* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update packaging

* Thu Apr 25 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
