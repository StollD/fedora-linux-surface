%global pkg_version 20190927
%global pkg_release 1
%global pkg_source https://github.com/StollD/fedora-linux-surface

Name:		linux-surface-secureboot
Summary:	The secureboot certificate for kernel-surface
License:	GPLv2
BuildArch:	noarch
Requires:	mokutil

Version:	%{pkg_version}
Release:	%{pkg_release}%{?dist}
URL:		%{pkg_source}
Source0:	StollD.der

%description
This package installs the secureboot certificate that is used to sign the kernel
from the kernel-surface package. When you reboot for the first time, it will ask
you to enroll the MOK certificate. Please check if the key is really mine, and
then confirm the import by entering "000" as the password.

%prep
%setup -q -c -T

%global cert_dir /usr/share/linux-surface-secureboot

%install
rm -rf %{buildroot}
install -dm 755 %{buildroot}%{cert_dir}
install -pm 644 %{SOURCE0} %{buildroot}%{cert_dir}

%post
TEMP=$(mktemp)
mokutil --generate-hash=000 > $TEMP
mokutil --hash-file $TEMP --import %{cert_dir}/StollD.der

%files
%{cert_dir}/StollD.der

%changelog
* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update packaging

* Thu Apr 25 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
