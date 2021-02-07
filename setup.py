# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in herjimar/__init__.py
from herjimar import __version__ as version

setup(
	name='herjimar',
	version=version,
	description='Modificaciones para Herjimar',
	author='Herjimar',
	author_email='erp@herjimar.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
