Name:           linux-surfacegen5-button-autoremap
Version:        1
Release:        1
Summary:        Auto-remap Surface Book 2/Surface Pro (2017) volume buttons based on device orientation.

License:        MIT
URL:            https://github.com/qzed/linux-surfacegen5-button-autoremap
Source0:        https://github.com/qzed/linux-surfacegen5-button-autoremap/archive/master.zip
BuildArch:      noarch

Requires:       python3-evdev python3-dbus python3-pydbus iio-sensor-proxy

%description
Auto-remap Microsoft Surface Book 2 and Surface Pro (2017) volume buttons based on device orientation.

Ensures that the left/lower volume button always decreases, and the right/upper always increases the volume.

%prep
%autosetup -n linux-surfacegen5-button-autoremap-master

%build

%install
rm -rf $RPM_BUILD_ROOT

# Install the autorotate service
sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python3|g' autoremap.py
install -dm 755 $RPM_BUILD_ROOT/usr/lib/systemd/system
install -dm 755 $RPM_BUILD_ROOT/opt/surfacebook2-button-autoremap
install -pm 644 surfacebook2-button-autoremap.service $RPM_BUILD_ROOT/usr/lib/systemd/system
install -pm 755 autoremap.py $RPM_BUILD_ROOT/opt/surfacebook2-button-autoremap

%files
%doc
/usr/lib/systemd/system/surfacebook2-button-autoremap.service
/opt/surfacebook2-button-autoremap/autoremap.py

%changelog
* Thu Apr 25 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
