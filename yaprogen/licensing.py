# -*- coding: utf-8 -*-
#
# This file is part of Yaprogen
#
# Copyright (C) 2014-2017 Eric Le Bihan <eric.le.bihan.dev@free.fr>
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
   yaprogen.licensing
   ``````````````````

   Licenses management

   :copyright: (C) 2014-2017 Eric Le Bihan
   :license: GPLv3+
"""

import os
from gettext import gettext as _
from .common import get_data_dir


def get_default_notices_dir():
    """Returns the path to the default license notices directory.

    rtype: str
    """
    return os.path.join(get_data_dir(), 'notices')


def _list_available_license_notices():
    directories = [get_default_notices_dir()]
    notices = {}
    if 'YAPROGEN_LICENSE_NOTICES_PATH' in os.environ:
        directories += os.environ['YAPROGEN_LICENSE_NOTICES_PATH'].split(':')
    for directory in directories:
        for entry in os.listdir(directory):
            root, ext = os.path.splitext(entry)
            if ext == '.txt':
                notices[root] = os.path.join(directory, entry)
    return notices


def list_available_licenses():
    """Returns a list of the available licenses.

    returns: the list of licenses
    rtype: list of str
    """
    return sorted(_list_available_license_notices().keys())


def get_license_notice_text(license):
    """Returns the text for the notice for the matching license.

    :returns: the text of the license notice.
    :rtype: str
    """
    notices = _list_available_license_notices()
    if license not in notices:
        raise KeyError(_("Unknown license"))
    with open(notices[license]) as f:
        return f.read()

# vim: ts=4 sw=4 sts=4 et ai
