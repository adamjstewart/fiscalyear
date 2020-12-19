.. image:: https://github.com/adamjstewart/fiscalyear/workflows/pytest/badge.svg?branch=master
   :target: https://github.com/adamjstewart/fiscalyear/actions

.. image:: https://github.com/adamjstewart/fiscalyear/workflows/flake8/badge.svg?branch=master
   :target: https://github.com/adamjstewart/fiscalyear/actions

.. image:: https://github.com/adamjstewart/fiscalyear/workflows/black/badge.svg?branch=master
   :target: https://github.com/adamjstewart/fiscalyear/actions

.. image:: https://codecov.io/gh/adamjstewart/fiscalyear/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/adamjstewart/fiscalyear

.. image:: https://readthedocs.org/projects/fiscalyear/badge/?version=latest
   :target: https://fiscalyear.readthedocs.io

.. image:: https://badge.fury.io/py/fiscalyear.svg
   :target: https://pypi.org/project/fiscalyear/

.. image:: https://anaconda.org/conda-forge/fiscalyear/badges/version.svg
   :target: https://anaconda.org/conda-forge/fiscalyear

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

Overview
========

`fiscalyear <https://github.com/adamjstewart/fiscalyear>`_ is a small, lightweight Python module providing helpful utilities for managing the fiscal calendar. It is designed as an extension of the built-in `datetime <https://docs.python.org/3/library/datetime.html>`_ and `calendar <https://docs.python.org/3/library/calendar.html>`_ modules, adding the ability to query the fiscal year, fiscal quarter, fiscal month, and fiscal day of a date or datetime object.


Basic Usage
===========

``fiscalyear`` provides several useful classes.


FiscalYear
----------

The ``FiscalYear`` class provides an object for storing information about the start and end of a particular fiscal year.

.. code-block:: python

   >>> from fiscalyear import *
   >>> a = FiscalYear(2017)
   >>> a.start
   FiscalDateTime(2016, 10, 1, 0, 0)
   >>> a.end
   FiscalDateTime(2017, 9, 30, 23, 59, 59)
   >>> a.isleap
   False

You can also get the current ``FiscalYear`` with:

.. code-block:: python

   >>> FiscalYear.current()
   FiscalYear(2018)


FiscalQuarter
-------------

The ``FiscalYear`` class also allows you to query information about a specific fiscal quarter.

.. code-block:: python

   >>> a.q3.start
   FiscalDateTime(2017, 4, 1, 0, 0)
   >>> a.q3.end
   FiscalDateTime(2017, 6, 30, 23, 59, 59)


These objects represent the standalone ``FiscalQuarter`` class.

.. code-block:: python

   >>> b = FiscalQuarter(2017, 3)
   >>> b.start
   FiscalDateTime(2017, 4, 1, 0, 0)
   >>> b.end
   FiscalDateTime(2017, 6, 30, 23, 59, 59)
   >>> a.q3 == b
   True
   >>> b in a
   True
   >>> b.next_fiscal_quarter
   FiscalQuarter(2017, 4)

You can also get the current ``FiscalQuarter`` with:

.. code-block:: python

   >>> FiscalQuarter.current()
   FiscalQuarter(2018, 2)


FiscalMonth
-----------

The ``FiscalMonth`` class allows you to keep track of the fiscal month.

.. code-block:: python

   >>> c = FiscalMonth(2017, 9)
   >>> c.start
   FiscalDateTime(2017, 6, 1, 0, 0)
   >>> c.end
   FiscalDateTime(2017, 6, 30, 23, 59, 59)
   >>> c in a
   True
   >>> c in b
   True
   >>> c.next_fiscal_month
   FiscalMonth(2017, 10)

You can also get the current ``FiscalMonth`` with:

.. code-block:: python

   >>> FiscalMonth.current()
   FiscalMonth(2018, 4)


FiscalDay
---------

To keep track of the fiscal day, use the ``FiscalDay`` class.

.. code-block:: python

   >>> d = FiscalDay(2017, 250)
   >>> d.start
   FiscalDateTime(2017, 6, 6, 0, 0)
   >>> d.end
   FiscalDateTime(2017, 6, 6, 23, 59, 59)
   >>> d in a
   True
   >>> d in b
   True
   >>> d in c
   True
   >>> d.next_fiscal_day
   FiscalDay(2017, 251)

You can also get the current ``FiscalDay`` with:

.. code-block:: python

   >>> FiscalDay.current()
   FiscalDay(2018, 94)


FiscalDateTime
--------------

The start and end of each of the above objects are stored as instances of the ``FiscalDateTime`` class. This class provides all of the same features as the ``datetime`` class, with the addition of the ability to query the fiscal year, fiscal quarter, fiscal month, and fiscal day.

.. code-block:: python

   >>> e = FiscalDateTime.now()
   >>> e
   FiscalDateTime(2017, 4, 8, 20, 30, 31, 105323)
   >>> e.fiscal_year
   2017
   >>> e.fiscal_quarter
   3
   >>> e.next_fiscal_quarter
   FiscalQuarter(2017, 4)
   >>> e.fiscal_month
   7
   >>> e.fiscal_day
   190


FiscalDate
----------

If you don't care about the time component of the ``FiscalDateTime`` class, the ``FiscalDate`` class is right for you.

.. code-block:: python

   >>> f = FiscalDate.today()
   >>> f
   FiscalDate(2017, 4, 8)
   >>> f.fiscal_year
   2017
   >>> f.prev_fiscal_year
   FiscalYear(2016)


Installation
============

``fiscalyear`` has no dependencies, making it simple and easy to install. The recommended way to install ``fiscalyear`` is with ``pip``.

.. code-block:: console

   $ pip install fiscalyear


For alternate installation methods, see the `Installation Documentation <http://fiscalyear.readthedocs.io/en/latest/installation.html>`_.


Documentation
=============

Documentation is hosted on `Read the Docs <http://fiscalyear.readthedocs.io/en/latest/index.html>`_.
