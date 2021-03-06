#!/usr/bin/python

# This file is part of opengt.
# Author: Denis Klimov

__author__ = "Denis Klimov"
__version__ = "0.0.1"
__date__ = "Mon Feb 22 13:06:04 YEKT 2010"
__copyright__ = "Copyright (c) 2009 Denis Klimov"
__license__ = "GPLv3"

from distutils.core import setup
from glob import glob

longdesc = '''Open geo tracker django modules and daemon for receive,
parse and save data from trackers.'''

setup(
	name = "opengt",
	version = __version__,
	description = "Open geo tracking system",
	long_description = longdesc, 
	author = __author__, 
	author_email = "zver@altlinux.org", 
	url = "http://spo.tyumen.ru",
	license = __license__, 
	platforms = "Posix",
	scripts = ['opengtd/opengtd'],
	packages = [
			'opengt',
			'opengt/protocols',
			'django_opengt',
			'django_opengt/tracker',
			'django_opengt/tracker/templatetags',
	],
	data_files=[
				('share/django_opengt/media/js/jscolor', glob('django_opengt/media/js/jscolor/*')),
				('share/django_opengt/', ['opengt.nginx.sample']),
#				('/etc/init.d', ['opengtd/opengtd.init']),
	]
)

