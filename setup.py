#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='PyOI',
      version='4.0.1.1',
      description='Collection of Python tools for PTE-PMMC projects',
      author='Laércio de Sousa',
      author_email='lbsousajr@gmail.com',
      license='GNU GPLv3',
      url='https://github.com/oiteam/pmmc-pte-pyoi.git',
      packages=['pyoi'],
      scripts=['bin/pai', 'bin/sei', 'bin/arie', 'bin/arie2', 'bin/arie3', 'bin/arie4'])
