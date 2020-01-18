# NOTE: tests are disabled since should_be has not yet been packaged.
%global run_tests 0

# NOTE: python3 is disabled since python3-Cython is not yet packaged
%global with_python3 0

Name:           python-gssapi
Version:        1.2.0
Release:        3%{?dist}
Summary:        Python Bindings for GSSAPI (RFC 2743/2744 and extensions)

License:        ISC
URL:            https://github.com/pythongssapi/python-gssapi
Source0:        https://github.com/pythongssapi/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

Patch0: k5test-0.9.1-usr_lib64.patch
Patch1: python-gssapi-cython_0.19.patch
Patch2: python-gssapi-1.2.1-overwrite_cred_store.patch
Patch3: python-gssapi-display_status-infinite-recursion.patch

BuildRequires:  python2-devel
BuildRequires:  krb5-devel >= 1.10
BuildRequires:  krb5-libs >= 1.10
BuildRequires:  Cython >= 0.19
BuildRequires:  python-setuptools
Requires:       krb5-libs >= 1.10
Requires:       python-six
Requires:       python-enum34
Requires:       python-decorator

%if 0%{?run_tests}
BuildRequires:  python-nose
BuildRequires:  python-nose-parameterized
BuildRequires:  python-shouldbe
BuildRequires:  python-tox
BuildRequires:  krb5-server >= 1.10
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-Cython

%if 0%{?run_tests}
BuildRequires:  python3-nose
BuildRequires:  python3-nose-parameterized
BuildRequires:  python3-should-be
%endif
%endif

%description
A set of Python bindings to the GSSAPI C library providing both
a high-level pythonic interfaces and a low-level interfaces
which more closely matches RFC 2743.  Includes support for
RFC 2743, as well as multiple extensions.


%if 0%{?with_python3}
%package -n python3-gssapi
Summary:        Python 3 Bindings for GSSAPI (RFC 2743/2744 and extensions)

Requires:       krb5-libs >= 1.10
Requires:       python3-six
Requires:       python3-decorator

%description -n python3-gssapi
A set of Python 3 bindings to the GSSAPI C library providing both
a high-level pythonic interfaces and a low-level interfaces
which more closely matches RFC 2743.  Includes support for
RFC 2743, as well as multiple extensions.
%endif


%prep
%setup -q

%patch0 -p1 -b .usr_lib64
%patch1 -p1 -b .cython_0.19
%patch2 -p1 -b .overwrite_cred_store
%patch3 -p1 -b .display_status-infinite-recursion

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
CFLAGS="%{optflags}" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

# fix permissions on shared objects (mock seems to set them
# to 0775, whereas a normal build gives 0755)
find %{buildroot}%{python3_sitearch}/gssapi -name '*.so' \
    -exec chmod 0755 {} \;

popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# fix permissions on shared objects (mock seems to set them
# to 0775, whereas a normal build gives 0755)
find %{buildroot}%{python2_sitearch}/gssapi -name '*.so' \
    -exec chmod 0755 {} \;

%check
%if 0%{?run_tests}
%{__python2} setup.py nosetests

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py nosetests
popd
%endif
%endif


%files
%doc README.txt
%license LICENSE.txt
%{python2_sitearch}/*

%if 0%{?with_python3}
%files -n python3-gssapi
%doc README.txt
%license LICENSE.txt
%{python3_sitearch}/*
%endif


%changelog
* Tue Apr 11 2017 Robbie Harwood <rharwood@redhat.com> - 1.2.0-3
- Fix an infinite loop from gss_display_status
- Resolves: #1438390

* Mon Apr 04 2016 Robbie Harwood <rharwood@redhat.com> - 1.2.0-2
- Move python-tox from build requirement to test requirement
- Resolves: #1292139

* Mon Mar 28 2016 Robbie Harwood <rharwood@redhat.com> - 1.2.0-1
- Import upstream version 1.2.0 with patches
- Resolves: #1292139
