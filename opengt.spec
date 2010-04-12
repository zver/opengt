Name: opengt
Version: 0.0.1
Release: alt1

Summary: Open geo tracker system
License: GPLv3
Group: Monitoring

Url: http://spo.tyumen.ru
BuildArch: noarch
Source: %name-%version.tar

%setup_python_module django-opengt

%description
Open geo tracker django modules and daemon for receive,
parse and save data from trackers.


%package -n python-module-django-opengt
Summary: Django opengt modules
Group: Development/Python
%description -n python-module-django-opengt
Django opengt modules

%package -n python-module-opengt
Summary: Python opengt modules
Group: Development/Python
%description -n python-module-opengt
Python opengt modules

%package -n opengtd
Summary: Opengt daemon
Group: Monitoring
%description -n opengtd
Opengt daemon

%prep
%setup

%build
%python_build

%install
%python_install

# opengtd
install -pD -m 644 opengtd/opengtd.conf %buildroot%_sysconfdir/opengtd.conf

%files

%files -n python-module-django-opengt
%python_sitelibdir/django_opengt
%_datadir/django_opengt

%files -n python-module-opengt
%python_sitelibdir/opengt*

%files -n opengtd
%_bindir/opengtd
%_sysconfdir/opengtd.conf


%changelog
* Mon Feb 22 2010 Denis Klimov <zver@altlinux.org> 0.0.1-alt1
- Initial build for ALT Linux

