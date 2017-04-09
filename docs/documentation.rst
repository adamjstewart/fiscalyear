Documentation
=============

``fiscalyear`` uses `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ and the `Read the Docs Theme <https://docs.readthedocs.io/en/latest/theme.html>`_ to generate its documentation. The documentation is proudly hosted on `Read the Docs <https://readthedocs.org/>`_.


Building the documentation
--------------------------

To build the documentation, you'll need to have ``sphinx`` and ``sphinx_rtd_theme`` installed. Then, ``cd`` to the ``docs`` directory and use the ``Makefile`` to build everything.

.. code-block:: console

   $ cd docs
   $ make html


Building the documentation with setuptools
------------------------------------------

Alternatively, the documentation can be built with the following command:

.. code-block:: console

   $ python setup.py build_sphinx


Continuous Integration (CI)
---------------------------

Every time a change is made to the documentation and pushed to GitHub, Read the Docs automatically rebuilds the documentation, keeping everything in sync and up-to-date.
