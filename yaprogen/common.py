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

"""
   yaprogen.common
   ```````````````

   Common functions/classes

   :copyright: (C) 2014 Eric Le Bihan
   :license: GPLv3+
"""

import configparser
import os
from gettext import bindtextdomain, textdomain

def get_data_dir():
    """Returns the data directory.

    rtype: str
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(root_dir, '..')

    if os.path.exists(os.path.join(root_dir, '.git')):
        data_dir = os.path.join(root_dir, 'data')
    else:
        upper, lower = root_dir.split('lib')
        data_dir = os.path.join(upper, 'share', 'yaprogen')

    return os.path.normpath(data_dir)

def get_default_notices_dir():
    """Returns the path to the default license notices directory.

    rtype: str
    """
    return os.path.join(get_data_dir(), 'notices')

def list_available_licenses():
    """Returns a list of the available licenses.

    returns: the list of licenses
    rtype: list of str
    """
    directories = [get_default_notices_dir()]
    licenses = []
    if 'YAPROGEN_LICENSE_NOTICES_PATH' in os.env:
        directories += os.environ['YAPROGEN_LICENSE_NOTICES_PATH'].split(':')
        for directory in directories:
            for entry in os.listdir(directory):
                root, ext = os.path.splitext(entry)
                if ext == '.txt':
                    licenses.append(root)
    return set(sorted(licenses))

class Configuration:
    """Stores the configuration of the application."""
    def __init__(self):
        self.author_name = None
        self.author_email = None
        self.company_name = None
        self.preferred_license = None

    def load_from_file(self, filename):
        """Loads the configuration for file.

        :param filename: path to the configuration file.
        :type filename: str.
        """
        parser = configparser.ConfigParser()
        parser.readfp(open(filename))
        self.author_name = parser.get('Creation', 'AuthorName')
        self.author_email = parser.get('Creation', 'AuthorEmail')
        self.company_name = parser.get('Creation', 'CompanyName')
        self.preferred_license = parser.get('Creation', 'PreferredLicense',
                                            fallback='GPLv2+')

def load_configuration():
    """Load configuration from the user configuration file.

    :returns: the configuration.
    :rtype: :class:`Config`.
    """
    config = Configuration()
    filename = os.path.expanduser('~/.config/yaprogen.conf')
    if os.path.exists(filename):
        config.load_from_file(filename)
    return config

def setup_i18n():
    """Set up internationalization."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if 'lib' not in root_dir:
        return
    root_dir, mod_dir = root_dir.split('lib', 1)
    locale_dir = os.path.join(root_dir, 'share', 'locale')

    bindtextdomain('yaprogen', locale_dir)
    textdomain('yaprogen')

# vim: ts=4 sw=4 sts=4 et ai
