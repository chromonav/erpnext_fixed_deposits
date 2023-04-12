from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpnext_fixed_deposits/__init__.py
from erpnext_fixed_deposits import __version__ as version

setup(
	name="erpnext_fixed_deposits",
	version=version,
	description="erpnext_fixed_deposits",
	author="Hybrowlabs Technologies",
	author_email="chinmay@hybrowlabs.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
