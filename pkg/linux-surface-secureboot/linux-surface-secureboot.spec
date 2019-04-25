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

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT/usr/share/linux-surface-secureboot
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT/usr/share/linux-surface-secureboot

%post

# Install the repository
mokutil --import /usr/share/linux-surface-secureboot/MOK.der --password 000

%preun

mokutil --delete /usr/share/linux-surface-secureboot/MOK.der --password 000

%files
/usr/share/linux-surface-secureboot/MOK.der

%changelog
* Thu Apr 25 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
