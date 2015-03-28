========
yaprogen
========

-----------------------------
Yet Another Project Generator
-----------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2013 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

yaprogen [OPTIONS] <command> [<arg>, ...]

yaprogen list

yaprogen create [OPTIONS] <template> <project name>

DESCRIPTION
===========

`yaprogen(1)` generates a skeleton to develop a program or a library using
templates, based on the `Mustache templating system
<http://mustache.github.io/>`_.

A template is a directory containing a skeleton and a manifest. The skeleton
is the set of ``*.mustache`` files to be updated using parameters provided by
the user. The manifest is a JSON file describing the template (name, brief
description, ...).

By default, `yaprogen(1)` looks for templates in
``/usr/share/yaprogen/templates``. Use `yaprogen list` to get a list of the
available templates. It is possible to add custom templates. The paths to the
new templates is to provided via the *$YAPROGEN_TEMPLATES_PATH* environment
variable. The paths must be separated using a column. If a custom template
derives from a default one, with the same name, it will be selected instead of
the default one. If several directories defines the same template, the one
from the last directory will be selected.  Use `yaprogen list --details` to
see the source of each available template.

To create a project, use the `yaprogen create` command. By default the project
will be generated in the current directory, in the ``output`` subdirectory.
Use the *--output* option to specify another destination.

To add a license notice in the header of the source files generated, use the
*--license* option. By default, `yaprogen(1)` looks for the notice text in
text files from ``/usr/share/yaprogen/notices``. Additional paths for notices
can be set via the *$YAPROGEN_LICENSE_NOTICES_PATH* environment variable.

The values for the user parameters used with the template are read from the
``$HOME/.config/yaprogen.conf`` file. They can be overriden using the options
of the `yaprogen create` command. See `yaprogen.conf(5)` for its syntax.

If `yaprogen create` is invoked with a template which uses extra variables
(declared as an array named "variables" in the manifest), the program will
interactively query the associated values from the user.

OPTIONS
=======

-v, --version   display program version and exit

COMMANDS
========

The following commands are available:

list [OPTIONS]
~~~~~~~~~~~~~~

List all the availables templates. Use the *--details* option to see the
source directory of each template.

Options:

-d, --details    display details for each template

create [OPTIONS] <template> <project>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new project named *project* using the template *template*.

Options:

-a NAME, --author NAME             set author name
-c NAME, --copyright-holder NAME   set copyright holder
-C NAME, --company NAME            set company name
-d TEXT, --description TEXT        set short description of the project
-e ADDRESS, --email ADDRESS        set email address of the author
-l LICENSE, --license LICENSE      set license of the project
-o DIR, --output DIR               set output directory
-O KV, --override KV               override value of variable K with V
-p, --cross-platform               enable cross-platform support in template
-q, --quiet                        be quiet

The following variables can be overridden using the *--override* option:
apiname, execname, toolname. Use ':' to separate K from V.

Example:

  $ yaprogen create -o $HOME/Projects autotools superprogram

SEE ALSO
========

- ``yaprogen.conf(5)``
- ``yaprogentut(7)``

