from setuptools import setup, find_packages


install_requires = [
    'pyserial',
    'argparse',
    'numpy',
    'matplotlib'
]


setup(name="CSLtools",
version="0.0.1",
description="Basic python functions",
author="Aliénor Lahlou",
author_email="alienor.lahlou@sony.com",
packages = find_packages(),
install_requires = install_requires,
license="GPLv3",
)