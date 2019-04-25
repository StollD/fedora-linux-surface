Name:           linux-surface-secureboot
Version:        1
Release:        1
Summary:        Installs the secureboot key that the linux-surface kernel is signed with.

License:        GPLv2
URL:            https://github.com/StollD/fedora-linux-surface
Source0:        https://github.com/StollD/fedora-linux-surface/raw/master/keys/MOK.der

Requires:       mokutil
BuildArch:      noarch

%description
This package installs the secureboot certificate that is used to sign the kernel from the kernel-surface package.
When you reboot for the first time, it will ask you to enroll the MOK certificate. Please check if the key is really mine,
and then confirm the import by entering "000" as the password.

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT/usr/share/linux-surface-secureboot
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT/usr/share/linux-surface-secureboot

%post

# Install the repository
TEMP=$(mktemp)
mokutil --generate-hash=000 > $TEMP
mokutil --hash-file $TEMP --import /usr/share/linux-surface-secureboot/MOK.der

%preun

TEMP=$(mktemp)
mokutil --generate-hash=000 > $TEMP
mokutil --hash-file $TEMP --delete /usr/share/linux-surface-secureboot/MOK.der

%files
/usr/share/linux-surface-secureboot/MOK.der

%changelog
* Thu Apr 25 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
