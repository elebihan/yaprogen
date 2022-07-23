Changelog
=========

[0.8.0] - 2022-07-23
--------------------

Added
~~~~~

- common-dlang: new common directory
- common-gtk: new common directory
- common-rust: add shell-completion support
- generator: add app_id and app_path variables
- generator: add namespace template variables
- meson-dlang-app: new template
- meson-gtk-app: new template
- meson-gtkrs-app: build-aux: add distributables.txt
- meson-gtkrs-app: new template
- nodejs-cli-app: new template
- script-ruby: new template

Changed
~~~~~~~

- HACKING: tell how to deploy in development mode with VirtualEnv
- README: build using VirtualEnv, install using Wheel
- common-rust: bump some crates
- meson-dlang-app: use dedicated EditorConfig
- meson-gtkrs-app: use company in application name
- meson-rust-app: install shell-completion files
- meson-rust-app: rework build helpers and targets
- meson-rust-app: use Python for build-aux tools
- meson-rust-app: use common build script
- setup.py: needs python >= 3.7, pystache >= 0.6
- templates: meson-*: require meson >= 0.50

Fixed
~~~~~

- generator: fix substitutions in non-template files

[0.6.0] - 2018-10-08
--------------------

Added
~~~~~

- cli: add --spdx command line option
- make-rust-app: new template
- meson-rust-app: new template

Changed
~~~~~~~

- cmake-c-lib: add MAN page generation
- data: notices: use SPDX identifiers
- refactor common files in templates
- change some template names

[0.4.0] - 2017-10-19
--------------------

Added
~~~~~

- new templates:

  * meson-c-lib
  * rust-cli-app

Changed
~~~~~~~

- rename {autotools,cmake,make}-based templates.
- python-app: use setuptools entry points.

[0.2.0] - 2015-03-28
--------------------

Added
~~~~~

- new templates:

  * Autotools and CMAKE based projects
  * Buildroot package
  * Python, Mono applications
  * Shell script
