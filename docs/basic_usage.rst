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

You can also get the current ``FiscalYear`` with:

.. code-block:: python

   >>> FiscalYear.current()
   FiscalYear(2018)


FiscalQuarter
-------------

The ``FiscalYear`` class also allows you to query information about a specific quarter.

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

You can also get the current ``FiscalQuarter`` with:

.. code-block:: python

   >>> from fiscalyear import *
   >>> FiscalQuarter.current()
   FiscalQuarter(2018, 2)


FiscalDateTime
--------------

The start and end of each quarter are stored as instances of the ``FiscalDateTime`` class. This class provides all of the same features as the ``datetime`` class, with the addition of the ability to query the fiscal year, fiscal month, and quarter.

.. code-block:: python

   >>> c = FiscalDateTime.now()
   >>> c
   FiscalDateTime(2017, 4, 8, 20, 30, 31, 105323)
   >>> c.fiscal_year
   2017
   >>> c.fiscal_month
   7
   >>> c.quarter
   3
   >>> c.next_quarter
   FiscalQuarter(2017, 4)


FiscalDate
----------

If you don't care about the time component of the ``FiscalDateTime`` class, the ``FiscalDate`` class is right for you.

.. code-block:: python

   >>> d = FiscalDate.today()
   >>> d
   FiscalDate(2017, 4, 8)
   >>> d.fiscal_year
   2017
   >>> d.prev_fiscal_year
   FiscalYear(2016)
