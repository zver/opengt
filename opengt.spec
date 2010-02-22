Name: opengt
Version: 0.0.1
Release: alt1

Summary: Open geo tracker system
License: GPLv3
Group: Monitoring

Url: http://spo.tyumen.ru
Source: %name-%version.tar

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

%package -n osolutions-webapps-agp
Summary: AGP web site with opengt system
Group: Development/Python
%description -n osolutions-webapps-agp
AGP web site with opengt system

%prep
%setup

%build

%install
%python_install

# opengtd
install -pD -m 644 opengtd/opengtd.conf %buildroot%_sysconfdir/opengtd.conf

# Install sample agp web app
%define AGP_INSTALL_DIR /var/www/webapps/opengt_agp
%add_python_lib_path %AGP_INSTALL_DIR
mkdir -p %buildroot%AGP_INSTALL_DIR
cp -r django_opengt/agp %buildroot%AGP_INSTALL_DIR
cp -r django_opengt/media %buildroot%AGP_INSTALL_DIR
cp -r django_opengt/templates %buildroot%AGP_INSTALL_DIR
cp django_opengt/*.py %buildroot%AGP_INSTALL_DIR

%files

%files -n python-module-django-opengt
%python_sitelibdir/django_opengt
%_datadir/django_opengt

%files -n python-module-opengt
%python_sitelibdir/opengt*

%files -n opengtd
%_bindir/opengtd
%_sysconfdir/opengtd.conf

%files -n osolutions-webapps-agp
%AGP_INSTALL_DIR


%changelog
* Mon Feb 22 2010 Denis Klimov <zver@altlinux.org> 0.0.1-alt1
- Initial build for ALT Linux

