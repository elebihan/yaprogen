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
#

"""
   yaprogen.generator
   ``````````````````

   Implement the template generator

   :copyright: (C) 2014-2017 Eric Le Bihan
   :license: GPLv3+
"""

import os
import re
import shutil
import pystache
from gettext import gettext as _
from datetime import datetime
from .licensing import get_license_notice_text


def split(string):
    crumbs = []
    for chunk in re.split(r'\W+', string):
        pieces = re.findall('[A-Z][^A-Z]*', chunk)
        if pieces:
            crumbs += pieces
        else:
            crumbs.append(chunk)
    return crumbs


def normalize(string):
    fields = split(string)
    return '-'.join(map(lambda x: x.lower(), fields))


def lower(string):
    fields = split(string)
    return '_'.join(map(lambda x: x.lower(), fields))


def upper(string):
    fields = split(string)
    return '_'.join(map(lambda x: x.upper(), fields))


def camelize(string):
    fields = split(string)
    return ''.join(map(lambda x: x.capitalize(), fields))


def namespacify(string):
    fields = split(string)
    if len(fields) == 1:
        return fields[0].lower()
    else:
        end = 3 if len(fields) >= 3 else 2
        ns = ''.join(map(lambda f: f[0].lower(), fields[:end]))
        return ns[0].upper() + ns[1:]


class Generator(object):
    """Generates a project using a template.

    :param name: name of the project.
    :type name: str.

    :param template: a template.
    type template: :class:`yaprogen.template.Template`.
    """
    def __init__(self, name, template):
        self._name = name
        self._template = template
        self.author = None
        self.description = None
        self.license = None
        self.copyright_holder = None
        self.email = None
        self.company = None
        self.homepage = None
        self.quiet = False
        self.enable_cross_platform = False
        self.use_spdx = False
        self._values = {}
        self.overrides = {}

    def _compute_values(self):
        if self.author:
            fields = self.author.split(' ', 1)
            if len(fields) == 2:
                firstname, surname = fields
            else:
                firstname = self.author
                surname = ''
        else:
            firstname, surname = '', ''

        name = normalize(self._name)
        nsname = namespacify(self._name)
        libname = linkname = apiname = toolname = execname = name
        if self._template.is_library:
            if name.startswith('lib'):
                linkname = libname[3:]
                apiname = linkname
            else:
                libname = 'lib' + name
            toolname = apiname + '-tool'
            execname = toolname

        apiname = self.overrides.get('apiname', apiname)
        libname = self.overrides.get('libname', libname)
        linkname = self.overrides.get('linkname', linkname)
        execname = self.overrides.get('execname', execname)
        toolname = self.overrides.get('toolname', toolname)
        nsname = self.overrides.get('nsname', nsname)

        if not self.copyright_holder:
            if self.author:
                if self.email:
                    self.copyright_holder = "{} <{}>".format(self.author,
                                                             self.email)
                else:
                    self.copyright_holder = self.author
            else:
                    self.copyright_holder = _("Unknown")
        copyright_notice = "Copyright (C) {} {}".format(datetime.now().year,
                                                        self.copyright_holder)

        notice_lines = []
        if self.license:
            if self.use_spdx:
                line = "SPDX-License-Identifier: {0}".format(self.license)
                notice_lines.append({'line': line})
            else:
                text = get_license_notice_text(self.license)
                for line in text.split('\n'):
                    notice_lines.append({'line': line})

        description = self.description or _("Insert description here")
        homepage = self.homepage or "https://some/where"

        company_name = self.company or 'unknown'

        app_id = "com.{}.{}".format(company_name, normalize(self._name))
        app_path = "/com/{}/{}".format(company_name, normalize(self._name))

        self._values = {
            'description': description,
            'license_alias': self.license,
            'license_notice': notice_lines,
            'copyright_notice': copyright_notice,
            'copyright_holder': self.copyright_holder,
            'year': datetime.now().year,
            'month': datetime.now().strftime("%B"),
            'day': datetime.now().day,
            'author_name': self.author,
            'author_firstname': firstname,
            'author_surname': surname,
            'author_email': self.email,
            'company_name': self.company,
            'homepage': homepage,
            'project_name': self._name,
            'project_normalized': normalize(self._name),
            'project_lower': lower(self._name),
            'project_upper': upper(self._name),
            'project_camel': camelize(self._name),
            'api_name': apiname,
            'api_lower': lower(apiname),
            'api_upper': upper(apiname),
            'api_camel': camelize(apiname),
            'executable_name': execname,
            'executable_lower': lower(execname),
            'executable_upper': upper(execname),
            'executable_camel': camelize(execname),
            'library_name': libname,
            'library_lower': lower(libname),
            'library_upper': upper(libname),
            'library_camel': camelize(libname),
            'link_name': linkname,
            'ns_name': nsname,
            'ns_normalized': normalize(nsname),
            'ns_lower': lower(nsname),
            'ns_upper': upper(nsname),
            'ns_camel': camelize(nsname),
            'tool_name': toolname,
            'tool_lower': lower(toolname),
            'tool_upper': upper(toolname),
            'is_cross_platform': self.enable_cross_platform,
            'app_id': app_id,
            'app_path': app_path,
        }

        self._values.update(self._template.extra_variables)

    def generate(self, destination):
        """Generates a project in directory.

        :param destination: path to the output directory.
        :type destination: str
        """
        if not os.path.exists(destination):
            os.makedirs(destination)

        self._compute_values()

        path = os.path.join(self._template.path, 'skeleton')

        subs = {
            'xyz-api': 'api_name',
            'xyz_api': 'api_lower',
            'XYZ_API': 'api_upper',
            'XyzApi': 'api_camel',
            'xyz-exec': 'executable_name',
            'xyz_exec': 'executable_lower',
            'XYZ_EXEC': 'executable_upper',
            'XyzExec': 'executable_camel',
            'xyz-lib': 'library_name',
            'xyz_lib': 'library_lower',
            'XYZ_LIB': 'library_upper',
            'XyzLib': 'library_camel',
            'xyz-ns': 'ns_normalized',
            'xyz_ns': 'ns_lower',
            'XYZ_NS': 'ns_upper',
            'XyzNs': 'ns_camel',
            'xyz-app_id': 'app_id',
        }

        for filename in self._template.files:
            target = filename.replace(path, destination)
            for k, v in subs.items():
                target = target.replace(k, self._values[v])
            target = target.replace('xyz',
                                    self._values['project_normalized'])
            if target.endswith('.mustache'):
                target = target.replace('.mustache', '')
                self._convert_file(filename, target)
            else:
                self._copy_file(filename, target)

        cleanfiles = ['.empty']
        for root, directories, filenames in os.walk(destination):
            for fn in filenames:
                if fn in cleanfiles:
                    path = os.path.join(root, fn)
                    if not self.quiet:
                        print(_("Removing {}".format(path)))
                    os.unlink(path)

    def _convert_file(self, src, dst):
        if not self.quiet:
            print(_("Generating {}".format(dst)))

        self._make_parent_dir(dst)

        with open(src, 'r') as f:
            renderer = pystache.Renderer(escape=lambda u: u)
            contents = renderer.render(f.read(), self._values)
        with open(dst, 'w') as f:
            f.write(contents)

        shutil.copymode(src, dst)

    def _copy_file(self, src, dst):
        if not self.quiet:
            print(_("Generating {} (copy)".format(dst)))

        self._make_parent_dir(dst)

        shutil.copy(src, dst)

    def _make_parent_dir(self, filename):
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

# vim: ts=4 sw=4 sts=4 et ai
