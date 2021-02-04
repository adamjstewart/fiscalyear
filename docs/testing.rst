Testing
=======

``fiscalyear`` comes with a full test-suite called ``test_fiscalyear``. To run the test-suite, you
will need to install the following packages:

* `pytest <https://docs.pytest.org/en/latest/>`_
* `pytest-mock <https://github.com/pytest-dev/pytest-mock/>`_


Running tests
-------------

Once ``pytest`` is installed, simply ``cd`` to the root directory of ``fiscalyear`` and run the ``pytest`` command.

.. code-block:: console

   $ git clone https://github.com/adamjstewart/fiscalyear.git
   $ cd fiscalyear
   $ pytest
   ============================ test session starts =============================
   platform darwin -- Python 2.7.13, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
   rootdir: /Users/Adam/fiscalyear, inifile:
   plugins: cov-2.3.1
   collected 66 items

   test_fiscalyear.py ..................................................................

   ========================= 66 passed in 0.21 seconds ==========================


``pytest`` provides automatic test detection that locates the ``test_fiscalyear.py`` file and runs tests that begin with ``test_*``.


Continuous Integration (CI)
---------------------------

In order to prevent bugs from being introduced into the code, ``fiscalyear`` uses `GitHub Actions <https://github.com/features/actions>`_ for continuous integration. After every commit or pull request, GitHub Actions automatically runs the test-suite across all supported versions of Python 2 and 3. This has the added benefit of preventing incompatibilities between different Python versions.
