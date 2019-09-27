%global pkg_version 5.3.1
%global pkg_release 1
%global pkg_source https://github.com/qzed/linux-surface

Name:		linux-surface-ipts-firmware
Summary:	Touchscreen firmware for Microsoft Surface
License:	proprietary
BuildArch:	noarch

Version:	%{pkg_version}
Release:	%{pkg_release}%{?dist}
URL:		%{pkg_source}
Source0:	%{pkg_source}/archive/v%{pkg_version}-%{pkg_release}.zip

%description
This package provides firmware files required for the touchscreen to operate.

%prep
%autosetup -n linux-surface-%{pkg_version}-%{pkg_release}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib
cp -r firmware %{buildroot}/usr/lib

%files
/usr/lib/firmware/intel/ipts

%changelog
* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
