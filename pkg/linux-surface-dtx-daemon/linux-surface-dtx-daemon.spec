Name:           linux-surface-dtx-daemon
Version:        0.1.4
Release:        1
Summary:        Surface Detachment System (DTX) Daemon

License:        MIT
URL:            https://github.com/qzed/linux-surface-dtx-daemon
Source0:        https://github.com/qzed/linux-surface-dtx-daemon/archive/v%{version}.tar.gz

Requires:       dbus libgcc
BuildRequires:  rust cargo

%global debug_package %{nil}

%description
Linux User-Space Detachment System (DTX) Daemon for the Surface ACPI Driver (and Surface Books).
Currently only the Surface Book 2 is supported, due to lack of driver-support on the Surface Book 1. 
This may change in the future.

%prep
%autosetup -n linux-surface-dtx-daemon-%{version}

%build
env CARGO_TARGET_DIR="$PWD/target" CARGO_INCREMENTAL=0 cargo build --release --locked
strip --strip-all "target/release/surface-dtx-daemon"
strip --strip-all "target/release/surface-dtx-userd"

%install
rm -rf $RPM_BUILD_ROOT

# binary files
install -D -m755 "target/release/surface-dtx-daemon" "$RPM_BUILD_ROOT/usr/bin/surface-dtx-daemon"
install -D -m755 "target/release/surface-dtx-userd" "$RPM_BUILD_ROOT/usr/bin/surface-dtx-userd"

# application files
install -D -m644 "etc/dtx/surface-dtx-daemon.conf" "$RPM_BUILD_ROOT/etc/surface-dtx/surface-dtx-daemon.conf"
install -D -m644 "etc/dtx/surface-dtx-userd.conf" "$RPM_BUILD_ROOT/etc/surface-dtx/surface-dtx-userd.conf"
install -D -m755 "etc/dtx/attach.sh" "$RPM_BUILD_ROOT/etc/surface-dtx/attach.sh"
install -D -m755 "etc/dtx/detach.sh" "$RPM_BUILD_ROOT/etc/surface-dtx/detach.sh"

# systemd service files
install -D -m644 "etc/systemd/surface-dtx-daemon.service" "$RPM_BUILD_ROOT/usr/lib/systemd/system/surface-dtx-daemon.service"
install -D -m644 "etc/systemd/surface-dtx-userd.service" "$RPM_BUILD_ROOT/usr/lib/systemd/user/surface-dtx-userd.service"

# dbus config file
install -D -m644 "etc/dbus/org.surface.dtx.conf" "$RPM_BUILD_ROOT/etc/dbus-1/system.d/org.surface.dtx.conf"

# udev rules
install -D -m644 "etc/udev/40-surface_dtx.rules" "$RPM_BUILD_ROOT/etc/udev/rules.d/40-surface_dtx.rules"

# completion files
install -D -m644 "target/surface-dtx-daemon.bash" "$RPM_BUILD_ROOT/usr/share/bash-completion/completions/surface-dtx-daemon"
install -D -m644 "target/surface-dtx-userd.bash" "$RPM_BUILD_ROOT/usr/share/bash-completion/completions/surface-dtx-userd"

install -D -m644 "target/_surface-dtx-daemon" "$RPM_BUILD_ROOT/usr/share/zsh/site-functions/_surface-dtx-daemon"
install -D -m644 "target/_surface-dtx-userd" "$RPM_BUILD_ROOT/usr/share/zsh/site-functions/_surface-dtx-userd"

install -D -m644 "target/surface-dtx-daemon.fish" "$RPM_BUILD_ROOT/usr/share/fish/completions/surface-dtx-daemon.fish"
install -D -m644 "target/surface-dtx-userd.fish" "$RPM_BUILD_ROOT/usr/share/fish/completions/surface-dtx-userd.fish"

# license
install -Dm644 "LICENSE" "$RPM_BUILD_ROOT/usr/share/licenses/surface-dtx-daemon/LICENSE"

%files
%license LICENSE
%config
/etc/surface-dtx/*
/usr/bin/surface-dtx-daemon
/usr/bin/surface-dtx-userd
/usr/lib/systemd/system/surface-dtx-daemon.service
/usr/lib/systemd/user/surface-dtx-userd.service
/etc/dbus-1/system.d/org.surface.dtx.conf
/etc/udev/rules.d/40-surface_dtx.rules
/usr/share/bash-completion/completions/surface-dtx-daemon
/usr/share/bash-completion/completions/surface-dtx-userd
/usr/share/zsh/site-functions/_surface-dtx-daemon
/usr/share/zsh/site-functions/_surface-dtx-userd
/usr/share/fish/completions/surface-dtx-daemon.fish
/usr/share/fish/completions/surface-dtx-userd.fish
/usr/share/licenses/surface-dtx-daemon/LICENSE

%changelog
* Sat Sep 14 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Update to 0.1.2

* Fri May 17 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
