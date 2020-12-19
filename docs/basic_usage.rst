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
