#!/usr/bin/env python

import re
import os
import sys
from setuptools import setup
from setuptools import find_packages

# Fix for tox to run OK. Adds in path to find README and requirements files
for path in sys.path:
    if "meraki_tools" in path:
        __file__ = os.path.join(re.findall(".*meraki_tools", path)[0],
                                "setup.py")


with open(
        # Use absolute path of README.md file
        os.path.join(
            os.path.split(os.path.abspath(__file__))[0], "README.md"),
        "r") as readme:
    long_description = readme.read()
    readme.close()
with open(
        os.path.join(
            os.path.split(os.path.abspath(__file__))[0], "requirements.txt"),
        "r") as req_file:
    install_requires = []
    for package in req_file.read().split("\n"):
        if package:
            install_requires.append(package)
    req_file.close()

setup(name='meraki_tools',
      version="0.0.1",
      description='Various Meraki API Tools',
      long_description=long_description,
      author='John W Kerns',
      author_email='jkerns@packetsar.com',
      url='https://github.com/PackeTsar/meraki_tools',
      license="GNU",
      packages=find_packages(),
      install_requires=install_requires,
      entry_points={
          }
      )
