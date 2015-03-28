#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of Yaprogen
#
# Copyright (C) 2014 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages
from disthelpers import extract_messages, init_catalog, update_catalog
from disthelpers import build, build_catalog, build_man
from glob import glob
import fnmatch
import os
import yaprogen


def collect_data_files(dst_dir, src_dir):
    data_files = []
    for root, directory, filenames in os.walk(src_dir):
        for filename in fnmatch.filter(filenames, '*.*'):
            src = os.path.join(root, filename)
            dst = root.replace(src_dir, dst_dir)
            data_files.append((dst, [src]))
    return data_files

setup(name='yaprogen',
      version=yaprogen.__version__,
      description='Yet Another Project Generator',
      long_description='''
      This program generates the skeleton for different build systems
      to develop a library or a program .
      ''',
      license='GPLv3',
      url='https://github.com/elebihan/yaprogen/',
      platforms=['Any'],
      keywords=['code generator', 'autotools'],
      install_requires=['pystache >= 0.5'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
      ],
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'yaprogen = yaprogen.cli:main',
          ]
      },
      data_files=[
          ('share/zsh/site-functions', glob('shell-completion/zsh/_*')),
      ] + collect_data_files('share/yaprogen', 'data'),
      include_package_data=True,
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      cmdclass={'build': build,
                'build_man': build_man,
                'extract_messages': extract_messages,
                'init_catalog': init_catalog,
                'update_catalog': update_catalog,
                'build_catalog': build_catalog})

# vim: ts=4 sts=4 sw=4 sta et ai
