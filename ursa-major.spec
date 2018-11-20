%if 0%{?fedora}
# we have some koji hubs doesn't support Python3 with kerberos auth
# at this moment, so we build with Python2 for all platforms now
%global with_python3 0
%endif

Name:       ursa-major
Version:    0.1.1
Release:    2%{?dist}
Summary:    A utility for working with module's koji tags in koji's tag inheritance.

Group:      Development/Tools
License:    MIT
URL:        https://pagure.io/ursa-major
Source0:    https://files.pythonhosted.org/packages/source/u/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
# libmodulemd is not available for ppc or i686
ExclusiveArch:  noarch aarch64 ppc64le s390x x86_64


BuildRequires:  help2man
BuildRequires:  libmodulemd

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-gobject-base
BuildRequires:  python3-cairo
BuildRequires:  python3-koji
BuildRequires:  python3-six
BuildRequires:  python3-requests
BuildRequires:  python3-jinja2
BuildRequires:  python3-psutil
BuildRequires:  python3-pytest
BuildRequires:  python3-mock
%else
BuildRequires:  python2-devel
BuildRequires:  python2-koji
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python-setuptools
BuildRequires:  python-gobject-base
BuildRequires:  pycairo
BuildRequires:  python-six
BuildRequires:  python-requests
BuildRequires:  python-jinja2
BuildRequires:  python-futures
BuildRequires:  pytest
BuildRequires:  python-mock
%else
BuildRequires:  python2-setuptools
BuildRequires:  python2-gobject-base
BuildRequires:  python2-cairo
BuildRequires:  python2-six
BuildRequires:  python2-requests
BuildRequires:  python2-jinja2
BuildRequires:  python2-futures
BuildRequires:  python2-pytest
BuildRequires:  python2-mock
%endif
%endif

Requires:       gobject-introspection
Requires:       krb5-workstation
Requires:       koji
Requires:       libmodulemd
Requires:       m2crypto

%if 0%{?with_python3}
Requires:       python3-gobject-base
Requires:       python3-cairo
Requires:       python3-koji
Requires:       python3-six
Requires:       python3-requests
Requires:       python3-jinja2
%else
Requires:       python2-koji
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       python-gobject-base
Requires:       pycairo
Requires:       python-six
Requires:       python-requests
Requires:       python-jinja2
Requires:       python-futures
%else
Requires:       python2-gobject-base
Requires:       python2-cairo
Requires:       python2-six
Requires:       python2-requests
Requires:       python2-jinja2
Requires:       python2-futures
%endif
%endif


%description
Usra-Major can be used to edit a tag config file and update module's koji tags
in koji's tag inheritance accordingly per the configuration in tag config file.


%package        -n ursa-major-stage
Summary:        A utility for working with module's koji tags in koji's tag inheritance.
Requires:       %{name} = %{version}-%{release}

%description    -n ursa-major-stage
The ursa-major-stage package contains script and configurations for Ursa-Major
to talk with Fedora's stage instances (Koji, MBS).


%prep
%setup -q

%if 0%{?rhel} && 0%{?rhel} <= 7
# workaround for no egg-info
sed -i '/pycairo/d' requirements.txt
# old setuptools not support environment marker
sed -i 's/futures.*/futures/' requirements.txt
%endif

# workaround for no egg-info
sed -i '/koji/d' requirements.txt

%build
%if 0%{?with_python3}
%py3_build
%else
%py2_build
%endif


%install
%if 0%{?with_python3}
%py3_install
%else
%py2_install
%endif

%if 0%{?with_python3}
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%else
export PYTHONPATH=%{buildroot}%{python2_sitelib}
%endif
mkdir -p %{buildroot}/%{_mandir}/man1

help2man -N --version-string=%{version} %{buildroot}/%{_bindir}/ursa-major > %{buildroot}/%{_mandir}/man1/ursa-major.1
for cmd in show-config check-config remove-module add-module add-tag; do
    help2man -N --version-string=%{version} "%{buildroot}/%{_bindir}/ursa-major $cmd" > %{buildroot}/%{_mandir}/man1/ursa-major-${cmd}.1
done


%check
%if 0%{?with_python3}
py.test-3
%else
py.test
%endif


%files
%doc README.rst
%license LICENSE

%if 0%{?with_python3}
%{python3_sitelib}/ursa_major*
%else
%{python2_sitelib}/ursa_major*
%endif

%{_bindir}/ursa-major
%dir %{_sysconfdir}/ursa-major
%config(noreplace) %{_sysconfdir}/ursa-major/ursa-major.conf
%doc %{_mandir}/man1/ursa-major*.1*

%files stage
%{_bindir}/ursa-major-stage
%config(noreplace) %{_sysconfdir}/ursa-major/ursa-major-stage.conf


%changelog
* Fri Nov 16 2018 Qixiang Wan <qwan@redhat.com> - 0.1.1-2
- Limit build arches as libmodulemd is not available for ppc or i686

* Fri Oct 26 2018 Qixiang Wan <qwan@redhat.com> - 0.1.1-1
- Initial version of spec file
