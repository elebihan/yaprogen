=============
yaprogen.conf
=============

-------------------------------
Configuration file for Yaprogen
-------------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2013 Eric Le Bihan
:Manual section: 5

DESCRIPTION
===========

The ``yaprogen.conf`` file contains the configuration parameters for
`yaprogen(1)`. It uses a structure similar to Microsoft Windows INI files.

The default location for this file is ``~/.config/yaprogen.conf``.

SYNTAX
======

The file contains sections, led by a *[section]* header followed by
*key=value* pairs. Lines beginning with '#' are considered as comments.

Example::

  # Configuration file
  [Creation]
  AuthorName = Homer Simpson
  AuthorEmail = homer.simpson@burnselectrics.com
  PreferredLicense = LGPLv2.1+

SECTIONS
========

Here is the list of potential sections.

Creation
--------

* AuthorName: name of the author
* AuthorEmail: e-mail address of the author
* CompanyName: name of the company which employs the author
* PreferredLicense: preferred license for the projects

SEE ALSO
========

- ``yaprogen(1)``

.. vim: ft=rst
