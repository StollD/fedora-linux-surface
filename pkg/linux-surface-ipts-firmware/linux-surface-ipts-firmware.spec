%global pkg_version 20191004
%global pkg_release 1
%global pkg_source https://github.com/qzed/linux-surface
%global pkg_commit a6c6b97da238af28dfb5fea4cd71c69f61d8d24e

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
- Actually fix the HID descriptor on Surface Laptop instead of replacing it

* Wed Oct 02 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update firmware to fix touch input for Surface Laptop

* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
