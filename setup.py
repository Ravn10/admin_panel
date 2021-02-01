# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in admin_panel/__init__.py
from admin_panel import __version__ as version

setup(
	name='admin_panel',
	version=version,
	description='Admin Panel',
	author='firsterp',
	author_email='support@firsterp.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
