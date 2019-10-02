%global pkg_version 20191002
%global pkg_release 1
%global pkg_source https://github.com/qzed/linux-surface
%global pkg_commit f12bf966702b9217d219cf84b6c657079f842d17

Name:		linux-surface-ipts-firmware
Summary:	Touchscreen firmware for Microsoft Surface
License:	proprietary
BuildArch:	noarch

Version:	%{pkg_version}
Release:	%{pkg_release}%{?dist}
URL:		%{pkg_source}
Source0:	%{pkg_source}/archive/%{pkg_commit}.zip

%description
This package provides firmware files required for the touchscreen to operate.

%prep
%autosetup -n linux-surface-%{pkg_commit}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib
cp -r firmware %{buildroot}/usr/lib

%files
/usr/lib/firmware/intel/ipts

%changelog
* Wed Oct 02 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update firmware to fix touch input for Surface Laptop

* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
