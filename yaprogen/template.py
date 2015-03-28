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
   yaprogen.template
   `````````````````

   Template management

   :copyright: (C) 2014 Eric Le Bihan
   :license: GPLv3+
"""

import os
import json
from fnmatch import fnmatch
from .common import get_data_dir
from gettext import gettext as _

def get_default_templates_dir():
    """Returns the path to the default templates directory"""
    return os.path.join(get_data_dir(), 'templates')

def list_templates(directory):
    """List the templates available in a directory.

    :param directory: path to the directory to inspect.
    :type directory: str.

    :returns: the list of templates.
    :rtype: list of :class:`Template`.
    """
    templates = []
    for entry in os.listdir(directory):
        entry = os.path.join(directory, entry)
        if os.path.isdir(entry):
            has_manifest = os.path.exists(os.path.join(entry, 'manifest.json'))
            has_skeleton = os.path.exists(os.path.join(entry, 'skeleton'))
            if has_manifest and has_skeleton:
                templates.append(Template(entry))
    return templates

def list_available_templates():
    """Returns a list of the available templates.

    :returns: the list of templates.
    :rtype: list of :class:`Template`.
    """
    directories = [get_default_templates_dir()]
    templates = []
    names = []
    if 'YAPROGEN_TEMPLATES_PATH' in os.environ:
        directories += os.environ['YAPROGEN_TEMPLATES_PATH'].split(':')
    for directory in reversed(directories):
        if os.path.exists(directory):
            for template in list_templates(directory):
                if template.name not in names:
                    templates.append(template)
                    names.append(template.name)
    return sorted(templates, key=lambda x: x.name)

def lookup_template_by_name(name):
    """Search for a template by its name.

    :param name: name of the template.
    :type name: str.

    :returns: the matching template.
    :rtype: :class:`Template`.
    """
    for entry in list_available_templates():
        if entry.name == name:
            return entry
    raise RuntimeError(_('template not found'))

class Template(object):
    """Represents the template of a project.

    :param path: path to the template.
    :type path: str.
    """
    def __init__(self, path):
        self._path = path
        filename = os.path.join(path, 'manifest.json')
        with open(filename) as f:
            m = json.load(f)
            if 'name' not in m:
                msg = _('{} is not a valid manifest')
                raise RuntimeError(msg.format(filename))
            self._name = m.get('name')
            self._descr = m.get('description', 'No description')
            self._is_library = m.get('is-library', False)
            variables = m.get('variables', [])
            self.extra_variables = dict(map(lambda x: (x, ''), variables))

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def description(self):
        return self._descr

    @property
    def is_library(self):
        return self._is_library

    @property
    def files(self):
        ignores = ('*.swp', '.svn', '*~')
        files = []
        path = os.path.join(self.path, 'skeleton')
        for root, directories, filenames in os.walk(path):
            for fn in filenames:
                if not any(fnmatch(fn, p) for p in ignores):
                    files.append(os.path.join(root, fn))
        files = set(files)
        return sorted(files)

# vim: ts=4 sw=4 sts=4 et ai
