Hacking on yaprogen
===================

Deploy in development mode
--------------------------

When developing on Yaprogen, it is possible to test the program from a virtual
environment::

  python3 -m venv venv
  source ./venv/bin/activate
  pip3 install docutils
  python setup.py develop

The program will be available as ``venv/bin/yaprogen``.

Translation
-----------

To generate the template::

  $ xgettext -o po/yaprogen.pot -L python -k_ scripts/* yaprogen/*.py

To update the french translation::

  $ msgmerge --update po/fr.po po/yaprogen.pot

.. vim: ft=rst
