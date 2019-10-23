Advanced Usage
==============

Not every government, business, and institution uses the same `fiscal calendar <https://en.wikipedia.org/wiki/Fiscal_year>`_. By default, the ``fiscalyear`` module uses the fiscal calendar of the `U.S. federal government <https://en.wikipedia.org/wiki/Fiscal_year#Federal_government>`_. For example, the 2017 fiscal year starts on October 1st, 2016 and ends on September 30th, 2017. In contrast, the `United Kingdom <https://en.wikipedia.org/wiki/Fiscal_year#United_Kingdom>`_ fiscal year is completely different. For personal tax purposes, the 2017 fiscal year in the U.K. starts on April 6th, 2017 and ends on April 5th, 2018. The ``fiscalyear`` module allows you to change the start date of the fiscal year to suit your needs.


Changing the fiscal calendar
----------------------------

In order to explain how to change the fiscal calendar, let's use the U.K. personal tax financial year as an example.

.. code-block:: python

   >>> import fiscalyear
   >>> a = fiscalyear.FiscalYear(2017)


Start year
^^^^^^^^^^

The first difference you'll notice between the U.S. and the U.K. fiscal calendars is that in the U.S., the 2017 fiscal year actually starts in 2016, while in the U.K. it starts in 2017. To control this, change the start year from ``'previous'`` to ``'same'``.

.. code-block:: python

   >>> a.start.year
   2016
   >>> fiscalyear.setup_fiscal_calendar(start_year='same')
   >>> a.start.year
   2017


Now that the start year is right, let's change the start month.


Start month
^^^^^^^^^^^

The start month can be any valid month.

.. code-block:: python

   >>> a.start.month
   10
   >>> fiscalyear.setup_fiscal_calendar(start_month=4)
   >>> a.start.month
   4

Finally, let's change the start day.


Start day
^^^^^^^^^

The start day can be any valid day in the chosen month.

.. code-block:: python

   >>> a.start.day
   1
   >>> fiscalyear.setup_fiscal_calendar(start_day=6)
   >>> a.start.day
   6


Putting everything together, we can see that the definition of the start and end of the fiscal calendar has been globally changed for all objects.

.. code-block:: python

   >>> a.start
   FiscalDateTime(2017, 4, 6, 0, 0)
   >>> a.end
   FiscalDateTime(2018, 4, 5, 23, 59, 59)


Of course, we can change all of these variables at the same time like so:

.. code-block:: python

   >>> fiscalyear.setup_fiscal_calendar('same', 4, 6)


Temporarily changing the fiscal calendar
----------------------------------------

If you need to work with multiple fiscal calendars in the same program, it may be beneficial to be able to temporarily change the fiscal calendar. The ``fiscalyear`` module provides a ``fiscal_calendar`` context manager to handle this.

.. code-block:: python

   >>> from fiscalyear import *
   >>> a = FiscalYear(2017)
   >>> a.start
   FiscalDateTime(2016, 10, 1, 0, 0)
   >>> with fiscal_calendar(start_month=6):
   ...     a.start
   ...
   FiscalDateTime(2016, 6, 1, 0, 0)
   >>> a.start
   FiscalDateTime(2016, 10, 1, 0, 0)


To recreate our previous example, this would look like:

.. code-block:: python

   >>> with fiscal_calendar('same', 4, 6):
   ...     a.start
   ...
   FiscalDateTime(2017, 4, 6, 0, 0)


Or in a for-loop:

.. code-block:: python

   calendars = [
       ('previous', 10, 1),
       ('same', 4, 6),
       ...
   ]

   for calendar in calendars:
       with fiscal_calendar(*calendar):
           # do stuff
