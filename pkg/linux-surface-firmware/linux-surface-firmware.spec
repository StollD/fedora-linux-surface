Name:           linux-surface-firmware
Version:        1
Release:        1
Summary:        Touchscreen firmware for Microsoft Surface.

%define upstream_tag 5.2.16-1

# I literally have no idea
License:        proprietary
URL:            https://github.com/qzed/linux-surface
Source0:        https://github.com/qzed/linux-surface/archive/v%{upstream_tag}.zip
BuildArch:      noarch

%description
Installs touchscreen firmware for Microsoft Surface, used by the linux-surface kernel.

%prep
%autosetup -n linux-surface-%{upstream_tag}

%build

%install
rm -rf $RPM_BUILD_ROOT

# Install the firmware files
mkdir -p $RPM_BUILD_ROOT/lib
cp -r firmware $RPM_BUILD_ROOT/lib

%files
/lib/firmware/intel/ipts

%changelog
* Sun Sep 22 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
