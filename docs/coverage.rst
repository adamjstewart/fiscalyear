Coverage
========

``fiscalyear`` uses ``pytest-cov`` to determine the percentage of the code base that is covered by unit tests. You will need to install this package along with ``pytest`` to run the coverage tests yourself.

Running coverage tests
----------------------

Once you have ``pytest`` and ``pytest-cov`` installed, you can run the coverage tests locally.

.. code-block:: console

   $ pytest --cov=fiscalyear
   ============================ test session starts =============================
   platform darwin -- Python 2.7.13, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
   rootdir: /Users/Adam/fiscalyear, inifile:
   plugins: cov-2.3.1
   collected 66 items

   test_fiscalyear.py ..................................................................

   ---------- coverage: platform darwin, python 2.7.13-final-0 ----------
   Name            Stmts   Miss  Cover
   -----------------------------------
   fiscalyear.py     233      0   100%


   ========================= 66 passed in 0.21 seconds ==========================


``fiscalyear`` always strives for 100% coverage, and won't accept pull requests that aren't covered by unit tests.


Continuous Integration (CI)
---------------------------

In addition to unit tests, Travis CI also runs coverage tests. The results of these tests are reported back to `codecov <https://codecov.io/gh>`_ and displayed through a badge on the README.
