Name:           linux-surface-repo
Version:        1
Release:        1
Summary:        Packages for running Fedora on Microsoft Surface devices

License:        GPLv2
URL:            https://github.com/StollD/fedora-linux-surface-repo
Source0:        https://github.com/StollD/fedora-linux-surface-repo/raw/master/linux-surface.repo
BuildArch:      noarch

%description

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT

# Install the repository
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d


%files
%doc
%config(noreplace) /etc/yum.repos.d/*



%changelog
* Thu Apr 25 2019 Dorian Stoll <dorian.stoll@tmsp.io>
- Initial version
