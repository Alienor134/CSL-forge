from setuptools import setup, find_packages


install_requires = [
    'pyserial',
    'argparse'
]


setup(name="CSLserial",
version="0.0.1",
description="Serial interface Arduino-Python",
author="Peter Hanappe",
author_email="peter@hanappe.com",
packages = find_packages(),
install_requires = install_requires,
license="GPLv3",
)