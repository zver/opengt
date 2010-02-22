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

%prep
%setup

%build

%install
%python_install

%files
%doc README
%python_sitelibdir/django_opengt
%python_sitelibdir/opengt*
%_datadir/django_opengt
%_bindir/opengtd

%changelog
* Mon Feb 22 2010 Denis Klimov <zver@altlinux.org> 0.0.1-alt1
- Initial build for ALT Linux

