Hacking on yaprogen
===================

Translation
-----------

To generate the template::

  $ xgettext -o po/yaprogen.pot -L python -k_ scripts/* yaprogen/*.py

To update the french translation::

  $ msgmerge --update po/fr.po po/yaprogen.pot

.. vim: ft=rst
