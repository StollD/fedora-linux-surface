%global pkg_version 1
%global pkg_release 1
%global pkg_source https://github.com/qzed/linux-surfacegen5-button-autoremap
%global pkg_commit 93b37ab94573bf5c72f9716cb56a0f2ce0405fdb

Name:		linux-surfacegen5-button-autoremap
Summary:	Auto-remap Surface Book 2/Surface Pro (2017) volume buttons based on device orientation.
License:	MIT
BuildArch:	noarch
Requires:	python3-evdev python3-dbus python3-pydbus iio-sensor-proxy

Version:	%{pkg_version}
Release:	%{pkg_release}%{?dist}
URL:		%{pkg_source}
Source0:	%{pkg_source}/archive/%{pkg_commit}.zip
Patch0:		0001-explicit-python3.patch

%description
Auto-remap Microsoft Surface Book 2 and Surface Pro (2017) volume buttons based
on device orientation. Ensures that the left/lower volume button always
decreases, and the right/upper always increases the volume.

%prep
%autosetup -n %{name}-%{pkg_commit}

%install
rm -rf %{buildroot}
install -dm 755 %{buildroot}/usr/lib/systemd/system
install -dm 755 %{buildroot}/opt/surfacebook2-button-autoremap
install -pm 644 surfacebook2-button-autoremap.service %{buildroot}/usr/lib/systemd/system
install -pm 755 autoremap.py %{buildroot}/opt/surfacebook2-button-autoremap

%files
/usr/lib/systemd/system/surfacebook2-button-autoremap.service
/opt/surfacebook2-button-autoremap/autoremap.py

%changelog
* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update packaging

* Thu Apr 25 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
