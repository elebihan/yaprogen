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

import os
import sys
import argparse
import traceback
from yaprogen import __version__
from yaprogen.common import setup_i18n, load_configuration
from yaprogen.licensing import list_available_licenses
from yaprogen.generator import Generator
from yaprogen.template import list_available_templates, lookup_template_by_name
from gettext import gettext as _

setup_i18n()


def parse_cmd_list(args):
    for template in list_available_templates():
        if args.with_details:
            text = "{0.name:<24} -- {0.description:<48} -- {0.path}"
        else:
            text = "{0.name:<24} -- {0.description:<48}"
        print(text.format(template))


def parse_cmd_create(args):
    config = load_configuration()
    template = lookup_template_by_name(args.template)

    if template.extra_variables:
        print(_("Please enter a value for each of the following variables:"))
        for name in template.extra_variables:
            value = input("{}? ".format(name))
            template.extra_variables[name] = value

    gen = Generator(args.project, template)
    gen.overrides = dict(map(lambda x: x.split(':'), args.overrides))
    gen.quiet = args.quiet
    gen.author = args.author or config.author_name
    gen.company = args.company or config.company_name
    gen.email = args.email or config.author_email
    gen.description = args.description
    gen.copyright_holder = args.copyright_holder
    gen.license = args.license or config.preferred_license
    gen.enable_cross_platform = args.cross_platform
    gen.generate(args.output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version',
                        action='version',
                        version=__version__)
    subparsers = parser.add_subparsers(dest='command')
    p = subparsers.add_parser('list',
                              help=_('list available templates'))
    p.add_argument('-d', '--details',
                   dest='with_details',
                   action='store_true',
                   default=False,
                   help=_('display details about each template'))
    p.set_defaults(func=parse_cmd_list)

    p = subparsers.add_parser('create',
                              help=_('create a new project'))
    p.add_argument('-a', '--author',
                   metavar=_('NAME'),
                   help=_('set author name'))
    p.add_argument('-c', '--copyright-holder',
                   metavar=_('NAME'),
                   help=_('set copyright holder'))
    p.add_argument('-C', '--company',
                   metavar=_('NAME'),
                   help=_('set company name'))
    p.add_argument('-d', '--description',
                   metavar=_('TEXT'),
                   help=_('set short description of the project'))
    p.add_argument('-e', '--email',
                   metavar=_('ADDRESS'),
                   help=_('set email address of the author'))
    p.add_argument('-l', '--license',
                   metavar=_('LICENSE'),
                   choices=list_available_licenses(),
                   help=_('set license of the project'))
    p.add_argument('-o', '--output',
                   metavar='DIR',
                   default=os.path.join(os.getcwd(), 'output'),
                   help=_('set output directory'))
    p.add_argument('-p', '--cross-platform',
                   action='store_true',
                   default=False,
                   help=_('enable cross-platform support in template'))
    p.add_argument('-q', '--quiet',
                   action='store_true',
                   default=False,
                   help=_('be quiet'))
    p.add_argument('-O', '--override',
                   action='append',
                   dest='overrides',
                   default=[],
                   metavar='K:V',
                   help=_('override value of variable K with V'))
    p.add_argument('template',
                   help=_('name of the template'))
    p.add_argument('project',
                   help=_('name of the project'))
    p.set_defaults(func=parse_cmd_create)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.error(_('Missing command'))
    else:
        try:
            rc = 0
            args.func(args)
        except Exception as e:
            if 'YAPROGEN_SHOW_STACK_TRACES' in os.environ:
                traceback.print_exc()
            else:
                print(_("Error: {}").format(e), file=sys.stderr)
            rc = 1
        return rc

# vim: ts=4 sw=4 sts=4 et ai
