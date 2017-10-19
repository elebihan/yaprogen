===========
yaprogentut
===========

--------------------------------
Yaprogen template creation guide
--------------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2013 Eric Le Bihan
:Manual section: 7

DESCRIPTION
===========

`yaprogen(1)` generates a skeleton to develop an executable or a library using
predefined templates. This guide will teach you how to create such templates.

FILE HIERARCHY
==============

A template is a directory containing:

- a ``skeleton`` directory, which contains the file hierarchy of the project.
- a ``manifest.json`` file, which contains information about the template.

`yaprogen(1)` will copy all the files and subdirectories of the ``skeleton``
directory into the output directory. Files with the ``*.mustache`` extension
will be considered as template files and will be processed before copy. Files
and directories can be marked for renaming using special names.

If you need an empty directory in your skeleton, create it and add a file
named ``.empty`` in it.

``manifest.json`` is a JSON file which should be formatted as follow::

  {
      "name": "xyz-bar",
      "description": "a short description",
      "author": "John Doe",
      "is-library": true,
      "variables": []
  }

The mandatory fields are:

- "name": the name of the template, that will be used as an argument to the
  ``create`` command. Use an hyphen as a word separator if needed.
- "description": a short description of the template, that will be displayed
  when using the ``list`` command with the *--details* option.
- "author": the name of the author of the template.

The optional fields are:

- "is-library": indicates this is a template of a project to build a shared
  library. The default value is "false".
- "variables": array of extra variables used in the template.

TEMPLATE SYNTAX
===============

The template files use the `Mustache templating system
<http://mustache.github.io>`_. As explained in the documentation, Mustache is
a logic-less template system, unlike Ruby's ERB or Python's Jinja: it does not
feature loops or elaborate conditional statements. It will only replace the
tags in a template file with the values provided.

A tag is indicated by a double pair of curly braces, or "mustaches"::

  {{year}}

In some languages, the curly braces may be used for special cases (e.g. variables
in shell scripts). In this kind of situation, it is possible to temporarily
use another pair of tag delimiter. To use *!!* instead of *{{* and *}}*, add
the following line at the beginning of the template file::

  {{=!! !!=}}

Then, declare tags are followed::

  !!year!!

Tags can be used to mark variables or sections of text to be processed. For
example, the tag *{{year}}* will be replaced by the current year in all the
template files containing it.

The conditional inclusion of a section of text can be marked using a tag. In
the following example, depending on the value of the boolean variable
*is_cross_platform*, a different block will be wriiten in the result file::

  {{#is_cross_platform}}
  This is a cross-platform project
  {{/is_cross_platform}}
  {{^is_cross_platform}}
  This is NOT a cross-platform project
  {{/is_cross_platform}}

TEMPLATE VARIABLES
==================

Only a set of predefined variables can used in the template files.
`yaprogen(1)` will compute the value of each variable using input from the
command line arguments and options.

The following variables can be used in the template files:

- description: short string describing the project
- license_alias: license identifier, as defined at http://spdx.org/
- license_notice: array containing the lines of the license notice
- copyright_notice: copyright notice
- copyright_holder: copyright holder
- year: current year
- author_name: name of the author (e.g. "John Doe")
- author_firstname: first name of the author (e.g. "John")
- author_surname: surname of the author (e.g. "Doe")
- author_email: email address of the author
- company_name: name of the company which employs the author
- project_name: name of the project (e.g. "Frob Baz", "Libxyz")
- project_normalized: normalized project name (e.g. "frob-baz")
- project_lower: project name in lower case, with underscores (e.g. "frob_baz")
- project_upper: project name in upper case, with underscores (e.g. "FROB_BAZ")
- project_camel: project name in camel case (e.g. "FrobBaz")
- api_name: API name, normalized (same as "project_name", stripped from "lib"
  prefix if present)
- api_lower: API name in lower case, with underscores
- api_upper: API name in upper case, with underscores
- api_camel: API name in camel case
- executable_name: executable name, normalized
- executable_lower: executable name in lower case, with underscores
- executable_upper: executable name in upper case, with underscores
- executable_camel: executable name in camel case
- library_name: library name, normalized (e.g. "libfrob-baz")
- library_lower: library name in lower case, with underscores (e.g.
  "libfrob_baz")
- library_upper: library name in upper case, with underscores (e.g.
  "LIBFROB_BAZ")
- library_camel: library name in camel case
- link_name: normalized name of the library, without the 'lib' prefix
  (e.g. "frob-baz")
- tool_name: tool name, normalized (e.g. "frob-baz-tool")
- tool_lower: tool name in lower case, with underscores
- tool_upper: tool name in upper case, with underscores
- is_cross_platform: boolean value for marking cross-platform specific
  sections

FILE AND DIRECTORY VARIABLES
============================

The following variables can be used in file or directory names:

- xyz: project name, normalized
- xyz-api: API name, normalized
- xyz_api: API name in lower case, with underscores
- XYZ_API: API name in upper case, with underscores
- XyzApi: API name in camel case
- xyz-exec: executable/tool name, normalized
- xyz_exec: executable/tool name, in lower case, with underscores
- XYZ_EXEC: executable/tool name, in upper case, with underscores
- XyzExec: executable/tool name, in camel case
- xyz-lib: library name, normalized
- xyz_lib:  library name in lower case, with underscores
- XYZ_LIB:  library name in upper case, with underscores
- XyzLib:  library name in camel case

For example, the file ``/path/to/sometemplate/skeleton/xyz-lib/xyz-api.h.mustache`` will be
processed and the result file will be named ``libquux/quux.h`` if the project name
is "libquux".
