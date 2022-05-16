========================================
yaprogen - yet another project generator
========================================

`yaprogen(1)` is a simple software project generator, which scaffolds some
source code depending on a chosen template.

Requirements
============

- Python 3.7 or above.

Build
=====

Building is performed from the cloned repository in a `Python virtual
environment`_::

  python3 -m venv venv
  source ./venv/bin/activate
  pip3 install docutils
  python setup.py bdist_wheel
  deactivate

This generates a Wheel file ``dist/yaprogen-X.Y.Z-py3-none-any.whl``, where
"X.Y.Z" is the current version.

Installation
============

To install the generated Wheel file for all users, execute::

  sudo python3 -m pip install dist/yaprogen-X.Y.Z-py3-none-any.whl

To install the generated Wheel file for the current user, execute::

  python3 -m pip install --user dist/yaprogen-X.Y.Z-py3-none-any.whl

Usage
=====

For further details, proceed to the `tutorial <man/yaprogentut.7.rst>`_ or read
the `manual <man/yaprogen.1.rst>`_.

License
=======

`GPL-3.0 <https://choosealicense.com/licenses/gpl-3.0/>`_

.. _Python virtual environment: https://docs.python.org/3/library/venv.html
