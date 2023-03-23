from setuptools import setup, find_packages


install_requires = [
    'matplotlib',
    'numpy',
    'pymmcore',
    'opencv-python>=4.7.0',
]


setup(name="CSLcamera",
version="0.0.1",
description="A class to control cameras interfaced with Micro-Manager",
author="Alienor Lahlou",
author_email="alienor.lahlou@sony.com",
packages = find_packages(),
install_requires = install_requires,
license="GPLv3",
)