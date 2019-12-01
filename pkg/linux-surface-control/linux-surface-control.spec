%global pkg_version 0.2.5
%global pkg_release 1
%global pkg_source https://github.com/qzed/linux-surface-control

Name:		linux-surface-control
Summary:	Control various aspects of Microsoft Surface devices from the shell
License:	MIT
BuildArch:	x86_64
Requires:	dbus libgcc
BuildRequires:	rust cargo

Version:	%{pkg_version}
Release:	%{pkg_release}%{?dist}
URL:		%{pkg_source}
Source0:	%{pkg_source}/archive/v%{pkg_version}.zip

%global debug_package %{nil}

%description
Control various aspects of Microsoft Surface devices on Linux from the shell.
Aims to provide a unified front-end to the various sysfs-attributes and special
devices.

%prep
%autosetup -n %{name}-%{pkg_version}

%build
env CARGO_TARGET_DIR="$PWD/target" CARGO_INCREMENTAL=0 cargo build --release --locked
strip --strip-all "target/release/surface"

%install
rm -rf %{buildroot}
install -D -m755 "target/release/surface" "%{buildroot}/usr/bin/surface"
install -D -m644 "target/surface.bash" "%{buildroot}/usr/share/bash-completion/completions/surface"
install -D -m644 "target/_surface" "%{buildroot}/usr/share/zsh/site-functions/_surface"
install -D -m644 "target/surface.fish" "%{buildroot}/usr/share/fish/completions/surface.fish"
install -D -m644 "LICENSE" "%{buildroot}/usr/share/licenses/surface-control/LICENSE"

%files
%license LICENSE
/usr/bin/surface
/usr/share/bash-completion/completions/surface
/usr/share/zsh/site-functions/_surface
/usr/share/fish/completions/surface.fish
/usr/share/licenses/surface-control/LICENSE

%changelog
* Sun Dec 01 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update to version 0.2.5

* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update packaging

* Sat Sep 14 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update to 0.2.4

* Fri May 17 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
