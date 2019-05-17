Name:           linux-surface-control
Version:        0.2.2
Release:        1
Summary:        Control various aspects of Microsoft Surface devices from the Command-Line

License:        MIT
URL:            https://github.com/qzed/linux-surface-control
Source0:        https://github.com/qzed/linux-surface-control/archive/v%{version}.tar.gz

Requires:       dbus libgcc
BuildRequires:  rust cargo

%global debug_package %{nil}

%description
Linux User-Space Detachment System (DTX) Daemon for the Surface ACPI Driver (and Surface Books).
Currently only the Surface Book 2 is supported, due to lack of driver-support on the Surface Book 1. 
This may change in the future.

%prep
%autosetup -n linux-surface-control-%{version}

%build
env CARGO_TARGET_DIR="$PWD/target" CARGO_INCREMENTAL=0 cargo build --release --locked
strip --strip-all "target/release/surface"

%install
rm -rf $RPM_BUILD_ROOT

install -D -m755 "target/release/surface" "$RPM_BUILD_ROOT/usr/bin/surface"

# completion files
install -D -m644 "target/surface.bash" "$RPM_BUILD_ROOT/usr/share/bash-completion/completions/surface"
install -D -m644 "target/_surface" "$RPM_BUILD_ROOT/usr/share/zsh/site-functions/_surface"
install -D -m644 "target/surface.fish" "$RPM_BUILD_ROOT/usr/share/fish/completions/surface.fish"

# license
install -Dm644 "LICENSE" "$RPM_BUILD_ROOT/usr/share/licenses/surface-control/LICENSE"

%files
%license LICENSE
/usr/bin/surface
/usr/share/bash-completion/completions/surface
/usr/share/zsh/site-functions/_surface
/usr/share/fish/completions/surface.fish
/usr/share/licenses/surface-control/LICENSE

%changelog
* Fri May 17 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
