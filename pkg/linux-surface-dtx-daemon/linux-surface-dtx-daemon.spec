%global pkg_version 0.1.4
%global pkg_release 1
%global pkg_source https://github.com/qzed/linux-surface-dtx-daemon

Name:		linux-surface-dtx-daemon
Summary:	Surface Detachment System (DTX) Daemon
License:	MIT
BuildArch:	x86_64
Requires:	dbus libgcc
BuildRequires:	rust cargo dbus-devel

Version:	%{pkg_version}
Release:	%{pkg_release}%{?dist}
URL:		%{pkg_source}
Source0:	%{pkg_source}/archive/v%{pkg_version}.zip

%global debug_package %{nil}

%description
Linux User-Space Detachment System (DTX) Daemon for the Surface ACPI Driver
(and Surface Books). Currently only the Surface Book 2 is supported, due to lack
of driver-support on the Surface Book 1. This may change in the future.

%prep
%autosetup -n %{name}-%{pkg_version}

%build
env CARGO_TARGET_DIR="$PWD/target" CARGO_INCREMENTAL=0 cargo build --release --locked
strip --strip-all "target/release/surface-dtx-daemon"
strip --strip-all "target/release/surface-dtx-userd"

%install
rm -rf %{buildroot}

# binary files
install -D -m755 "target/release/surface-dtx-daemon" "%{buildroot}/usr/bin/surface-dtx-daemon"
install -D -m755 "target/release/surface-dtx-userd" "%{buildroot}/usr/bin/surface-dtx-userd"

# application files
install -D -m644 "etc/dtx/surface-dtx-daemon.conf" "%{buildroot}/etc/surface-dtx/surface-dtx-daemon.conf"
install -D -m644 "etc/dtx/surface-dtx-userd.conf" "%{buildroot}/etc/surface-dtx/surface-dtx-userd.conf"
install -D -m755 "etc/dtx/attach.sh" "%{buildroot}/etc/surface-dtx/attach.sh"
install -D -m755 "etc/dtx/detach.sh" "%{buildroot}/etc/surface-dtx/detach.sh"
install -D -m644 "etc/systemd/surface-dtx-daemon.service" "%{buildroot}/usr/lib/systemd/system/surface-dtx-daemon.service"
install -D -m644 "etc/systemd/surface-dtx-userd.service" "%{buildroot}/usr/lib/systemd/user/surface-dtx-userd.service"
install -D -m644 "etc/dbus/org.surface.dtx.conf" "%{buildroot}/etc/dbus-1/system.d/org.surface.dtx.conf"
install -D -m644 "etc/udev/40-surface_dtx.rules" "%{buildroot}/etc/udev/rules.d/40-surface_dtx.rules"

# completion files
install -D -m644 "target/surface-dtx-daemon.bash" "%{buildroot}/usr/share/bash-completion/completions/surface-dtx-daemon"
install -D -m644 "target/surface-dtx-userd.bash" "%{buildroot}/usr/share/bash-completion/completions/surface-dtx-userd"
install -D -m644 "target/_surface-dtx-daemon" "%{buildroot}/usr/share/zsh/site-functions/_surface-dtx-daemon"
install -D -m644 "target/_surface-dtx-userd" "%{buildroot}/usr/share/zsh/site-functions/_surface-dtx-userd"
install -D -m644 "target/surface-dtx-daemon.fish" "%{buildroot}/usr/share/fish/completions/surface-dtx-daemon.fish"
install -D -m644 "target/surface-dtx-userd.fish" "%{buildroot}/usr/share/fish/completions/surface-dtx-userd.fish"

# license
install -Dm644 "LICENSE" "%{buildroot}/usr/share/licenses/surface-dtx-daemon/LICENSE"

%files
%license /usr/share/licenses/surface-dtx-daemon/LICENSE
%config /etc/dbus-1/system.d/org.surface.dtx.conf
%config /etc/udev/rules.d/40-surface_dtx.rules
%config(noreplace) /etc/surface-dtx/*
/usr/bin/surface-dtx-daemon
/usr/bin/surface-dtx-userd
/usr/lib/systemd/system/surface-dtx-daemon.service
/usr/lib/systemd/user/surface-dtx-userd.service
/usr/share/bash-completion/completions/surface-dtx-daemon
/usr/share/bash-completion/completions/surface-dtx-userd
/usr/share/zsh/site-functions/_surface-dtx-daemon
/usr/share/zsh/site-functions/_surface-dtx-userd
/usr/share/fish/completions/surface-dtx-daemon.fish
/usr/share/fish/completions/surface-dtx-userd.fish

%changelog
* Fri Sep 27 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update packaging

* Sat Sep 14 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update to 0.1.4

* Fri May 17 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
