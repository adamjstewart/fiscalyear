Testing
=======

``fiscalyear`` comes with a full test-suite called ``test_fiscalyear``. To run the test-suite, you will need to install the `pytest <https://docs.pytest.org/en/latest/>`_ package.


Running tests
-------------

Once ``pytest`` is installed, simply ``cd`` to the root directory of ``fiscalyear`` and run the ``pytest`` command.

.. code-block:: console

   $ git clone https://github.com/adamjstewart/fiscalyear.git
   $ cd fiscalyear
   $ pytest
   ==================================================================== test session starts =====================================================================
   platform darwin -- Python 2.7.13, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
   rootdir: /Users/Adam/fiscalyear, inifile:
   plugins: cov-2.3.1
   collected 66 items

   test_fiscalyear.py ..................................................................

   ================================================================= 66 passed in 0.37 seconds ==================================================================


``pytest`` provides automatic test detection that locates the ``test_fiscalyear.py`` file and runs tests that begin with ``test_*``.


Running tests during installation
---------------------------------

Unit tests can optionally be run during installation as well. To build, test, and install the ``fiscalyear`` module, run:

.. code-block:: console

   $ python setup.py build
   $ python setup.py test
   $ python setup.py install --prefix=/path/to/installation/prefix


This also requires the ``pytest-runner`` package to be installed.


Continuous Integration (CI)
---------------------------

In order to prevent bugs from being introduced into the code, ``fiscalyear`` uses `Travis CI <https://docs.travis-ci.com/>`_ for continuous integration. After every commit or pull request, Travis automatically runs the test-suite across all supported versions of Python 2 and 3. This has the added benefit of preventing incompatibilities between different Python versions.
