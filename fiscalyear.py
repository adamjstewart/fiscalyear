"""Utilities for managing the fiscal calendar."""

from __future__ import division, with_statement

__author__ = 'Adam J. Stewart'
__version__ = '0.1.0'

import calendar
import contextlib
import datetime


# Number of months in each quarter
MONTHS_PER_QUARTER = 12 // 4

MIN_QUARTER = 1
MAX_QUARTER = 4

# These global variables control the start of the fiscal year.
# The default is to use the U.S. federal government's fiscal year,
# but they can be changed to use any other fiscal year.
START_YEAR = 'previous'
START_MONTH = 10
START_DAY = 1


@contextlib.contextmanager
def fiscal_calendar(start_year=None,
                    start_month=None,
                    start_day=None):
    """A context manager that lets you modify the start of the fiscal calendar
    inside the scope of a with-statement.

    :param start_year: Relationship between the start of the fiscal year and
        the calendar year. Possible values: ``'previous'`` or ``'same'``.
    :type start_year: str
    :param start_month: The first month of the fiscal year
    :type start_month: int or str
    :param start_day: The first day of the first month of the fiscal year
    :type start_day: int or str
    :raises AssertionError: If ``start_year`` is not ``'previous'`` or ``'same'``
    :raises TypeError: If ``start_month`` or ``start_day`` is not an int or int-like string
    :raises ValueError: If ``start_month`` or ``start_day`` is out of range
    """
    global START_YEAR
    global START_MONTH
    global START_DAY

    # Use default values if not changed
    if start_year is None:
        start_year = START_YEAR
    if start_month is None:
        start_month = START_MONTH
    if start_day is None:
        start_day = START_DAY

    assert isinstance(start_year, str)
    assert start_year == 'previous' or start_year == 'same'
    start_month = _check_month(start_month)
    start_day = _check_day(start_month, start_day)

    # Backup previous values
    old_start_year = START_YEAR
    old_start_month = START_MONTH
    old_start_day = START_DAY

    # Temporarily change global variables
    START_YEAR = start_year
    START_MONTH = start_month
    START_DAY = start_day

    yield

    # Restore previous values
    START_YEAR = old_start_year
    START_MONTH = old_start_month
    START_DAY = old_start_day


def _check_int(value):
    """Check if value is an int or int-like string.

    :param value: The value to test
    :return: The value
    :rtype: int
    :raises TypeError: If value is not an int or int-like string
    """
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    else:
        raise TypeError('an int or int-like string is required (got %s)' % (
            type(value).__name__))


def _check_year(year):
    """Check if year is a valid year.

    :param year: The year to test
    :return: The year
    :rtype: int
    :raises TypeError: If year is not an int or int-like string
    :raises ValueError: If year is out of range
    """
    year = _check_int(year)

    if datetime.MINYEAR <= year <= datetime.MAXYEAR:
        return year
    else:
        raise ValueError('year must be in %d..%d' % (
            datetime.MINYEAR, datetime.MAXYEAR), year)


def _check_month(month):
    """Check if month is a valid month.

    :param month: The month to test
    :return: The month
    :rtype: int
    :raises TypeError: If month is not an int or int-like string
    :raises ValueError: If month is out of range
    """
    month = _check_int(month)

    if 1 <= month <= 12:
        return month
    else:
        raise ValueError('month must be in %d..%d' % (1, 12), month)


def _check_day(month, day):
    """Check if day is a valid day of month.

    :param month: The month to test
    :param day: The day to test
    :return: The day
    :rtype: int
    :raises TypeError: If month or day is not an int or int-like string
    :raises ValueError: If month or day is out of range
    """
    month = _check_month(month)
    day = _check_int(day)

    # Find the last day of the month
    # Use a non-leap year
    max_day = calendar.monthrange(2001, month)[1]

    if 1 <= day <= max_day:
        return day
    else:
        raise ValueError('day must be in %d..%d' % (1, max_day), day)


def _check_quarter(quarter):
    """Check if quarter is a valid quarter.

    :param quarter: The quarter to test
    :return: The quarter
    :rtype: int
    :raises TypeError: If quarter is not an int or int-like string
    :raises ValueError: If quarter is out of range
    """
    quarter = _check_int(quarter)

    if MIN_QUARTER <= quarter <= MAX_QUARTER:
        return quarter
    else:
        raise ValueError('quarter must be in %d..%d' % (
            MIN_QUARTER, MAX_QUARTER), quarter)


class FiscalYear(object):
    """A class representing a single fiscal year."""

    __slots__ = '_fiscal_year'

    def __new__(cls, fiscal_year):
        """Constructor.

        :param fiscal_year: The fiscal year
        :type fiscal_year: int or str
        :returns: A newly constructed FiscalYear object
        :rtype: FiscalYear
        :raises TypeError: If fiscal_year is not an int or int-like string
        :raises ValueError: If fiscal_year is out of range
        """
        fiscal_year = _check_year(fiscal_year)

        self = super(FiscalYear, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        return self

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> fy = FiscalYear(2017)
        >>> repr(fy)
        'FiscalYear(2017)'
        """
        return '%s(%d)' % (self.__class__.__name__,
                           self._fiscal_year)

    def __str__(self):
        """Convert to informal string, for str().

        >>> fy = FiscalYear(2017)
        >>> str(fy)
        'FY2017'
        """
        return 'FY%d' % (self._fiscal_year)

    # TODO: Implement __format__ so that you can print
    # fiscal year as 17 or 2017 (%y or %Y)

    def __contains__(self, item):
        """Returns True if item in self, else False.

        :param item: The item to check
        :type item: FiscalYear, FiscalQuarter, FiscalDateTime,
            datetime, FiscalDate, or date
        :rtype: bool
        """
        if isinstance(item, FiscalYear):
            return self == item
        elif isinstance(item, FiscalQuarter):
            return self._fiscal_year == item.fiscal_year
        elif (isinstance(item, FiscalDateTime) or
              isinstance(item, datetime.datetime)):
            return self.start <= item <= self.end
        elif (isinstance(item, FiscalDate) or
              isinstance(item, datetime.date)):
            return self.start.date() <= item <= self.end.date()
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(item).__name__))

    # Read-only field accessors

    @property
    def fiscal_year(self):
        """:returns: The fiscal year
        :rtype: int
        """
        return self._fiscal_year

    @property
    def prev_fiscal_year(self):
        """:returns: The previous fiscal year
        :rtype: FiscalYear
        """
        return FiscalYear(self._fiscal_year - 1)

    @property
    def next_fiscal_year(self):
        """:returns: The next fiscal year
        :rtype: FiscalYear
        """
        return FiscalYear(self._fiscal_year + 1)

    @property
    def start(self):
        """:returns: Start of the fiscal year
        :rtype: FiscalDateTime
        """
        return self.q1.start

    @property
    def end(self):
        """:returns: End of the fiscal year
        :rtype: FiscalDateTime
        """
        return self.q4.end

    @property
    def q1(self):
        """:returns: The first quarter of the fiscal year
        :rtype: FiscalQuarter
        """
        return FiscalQuarter(self._fiscal_year, 1)

    @property
    def q2(self):
        """:returns: The second quarter of the fiscal year
        :rtype: FiscalQuarter
        """
        return FiscalQuarter(self._fiscal_year, 2)

    @property
    def q3(self):
        """:returns: The third quarter of the fiscal year
        :rtype: FiscalQuarter
        """
        return FiscalQuarter(self._fiscal_year, 3)

    @property
    def q4(self):
        """:returns: The fourth quarter of the fiscal year
        :rtype: FiscalQuarter
        """
        return FiscalQuarter(self._fiscal_year, 4)

    # Comparisons of FiscalYear objects with other

    def __lt__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year < other._fiscal_year
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __le__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year <= other._fiscal_year
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __eq__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year == other._fiscal_year
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __ne__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year != other._fiscal_year
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __gt__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year > other._fiscal_year
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year >= other._fiscal_year
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))


class FiscalQuarter(object):
    """A class representing a single fiscal quarter."""

    __slots__ = ['_fiscal_year', '_quarter']

    def __new__(cls, fiscal_year, quarter):
        """Constructor.

        :param fiscal_year: The fiscal year
        :type fiscal_year: int or str
        :param quarter: The fiscal quarter [1 - 4]
        :type quarter: int or str
        :returns: A newly constructed FiscalQuarter object
        :rtype: FiscalQuarter
        :raises TypeError: If fiscal_year or quarter is not
            an int or int-like string
        :raises ValueError: If fiscal_year or quarter is out of range
        """
        fiscal_year = _check_year(fiscal_year)
        quarter = _check_quarter(quarter)

        self = super(FiscalQuarter, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        self._quarter = quarter
        return self

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> q3 = FiscalQuarter(2017, 3)
        >>> repr(q3)
        'FiscalQuarter(2017, 3)'
        """
        return '%s(%d, %d)' % (self.__class__.__name__,
                               self._fiscal_year,
                               self._quarter)

    def __str__(self):
        """Convert to informal string, for str().

        >>> q3 = FiscalQuarter(2017, 3)
        >>> str(q3)
        'FY2017 Q3'
        """
        return 'FY%d Q%d' % (self._fiscal_year,
                             self._quarter)

    # TODO: Implement __format__ so that you can print
    # fiscal year as 17 or 2017 (%y or %Y)

    def __contains__(self, item):
        """Returns True if item in self, else False.

        :param item: The item to check
        :type item: FiscalQuarter, FiscalDateTime, datetime,
            FiscalDate, or date
        :rtype: bool
        """
        if isinstance(item, FiscalQuarter):
            return self == item
        elif (isinstance(item, FiscalDateTime) or
              isinstance(item, datetime.datetime)):
            return self.start <= item <= self.end
        elif (isinstance(item, FiscalDate) or
              isinstance(item, datetime.date)):
            return self.start.date() <= item <= self.end.date()
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(item).__name__))

    # Read-only field accessors

    @property
    def fiscal_year(self):
        """:returns: The fiscal year
        :rtype: int
        """
        return self._fiscal_year

    @property
    def quarter(self):
        """:returns: The fiscal quarter
        :rtype: int
        """
        return self._quarter

    @property
    def prev_quarter(self):
        """:returns: The previous fiscal quarter
        :rtype: FiscalQuarter
        """
        fiscal_year = self._fiscal_year
        quarter = self._quarter - 1
        if quarter == 0:
            fiscal_year -= 1
            quarter = 4

        return FiscalQuarter(fiscal_year, quarter)

    @property
    def next_quarter(self):
        """:returns: The next fiscal quarter
        :rtype: int
        """
        fiscal_year = self._fiscal_year
        quarter = self._quarter + 1
        if quarter == 5:
            fiscal_year += 1
            quarter = 1

        return FiscalQuarter(fiscal_year, quarter)

    @property
    def start(self):
        """:returns: The start of the fiscal quarter
        :rtype: FiscalDateTime
        """

        # Find the first month of the fiscal quarter
        month = START_MONTH
        month += (self._quarter - 1) * MONTHS_PER_QUARTER
        month %= 12
        if month == 0:
            month = 12

        # Find the calendar year of the start of the fiscal quarter
        if START_YEAR == 'previous':
            year = self._fiscal_year - 1
        elif START_YEAR == 'same':
            year = self._fiscal_year
        else:
            raise ValueError("START_YEAR must be either 'previous' or 'same'",
                             START_YEAR)

        if month < START_MONTH:
            year += 1

        return FiscalDateTime(year, month, START_DAY, 0, 0, 0)

    @property
    def end(self):
        """:returns: The end of the fiscal quarter
        :rtype: FiscalDateTime
        """
        # Find the start of the next fiscal quarter
        next_start = self.next_quarter.start

        # Substract 1 second
        end = next_start - datetime.timedelta(seconds=1)

        return FiscalDateTime(end.year, end.month, end.day,
                              end.hour, end.minute, end.second,
                              end.microsecond, end.tzinfo)

    # Comparisons of FiscalQuarter objects with other

    def __lt__(self, other):
        if isinstance(other, FiscalQuarter):
            return ((self._fiscal_year,  self._quarter) <
                    (other._fiscal_year, other._quarter))
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __le__(self, other):
        if isinstance(other, FiscalQuarter):
            return ((self._fiscal_year,  self._quarter) <=
                    (other._fiscal_year, other._quarter))
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __eq__(self, other):
        if isinstance(other, FiscalQuarter):
            return ((self._fiscal_year,  self._quarter) ==
                    (other._fiscal_year, other._quarter))
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __ne__(self, other):
        if isinstance(other, FiscalQuarter):
            return ((self._fiscal_year,  self._quarter) !=
                    (other._fiscal_year, other._quarter))
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __gt__(self, other):
        if isinstance(other, FiscalQuarter):
            return ((self._fiscal_year,  self._quarter) >
                    (other._fiscal_year, other._quarter))
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, FiscalQuarter):
            return ((self._fiscal_year,  self._quarter) >=
                    (other._fiscal_year, other._quarter))
        else:
            raise TypeError("can't compare '%s' to '%s'" % (
                type(self).__name__, type(other).__name__))


class _FiscalBase:
    """The base class for FiscalDate and FiscalDateTime that
    provides the following common attributes in addition to
    those provided by datetime.date and datetime.datetime:
    """

    @property
    def fiscal_year(self):
        """:returns: The fiscal year
        :rtype: int
        """

        # The fiscal year can be at most 1 year away from the calendar year
        if self in FiscalYear(self.year):
            return self.year
        elif self in FiscalYear(self.year + 1):
            return self.year + 1
        elif self in FiscalYear(self.year - 1):
            return self.year - 1

    @property
    def prev_fiscal_year(self):
        """:returns: The previous fiscal year
        :rtype: FiscalYear
        """
        return FiscalYear(self.fiscal_year - 1)

    @property
    def next_fiscal_year(self):
        """:returns: The next fiscal year
        :rtype: FiscalYear
        """
        return FiscalYear(self.fiscal_year + 1)

    @property
    def quarter(self):
        """:returns: The quarter of the fiscal year
        :rtype: int
        """
        for quarter in range(1, 5):
            q = FiscalQuarter(self.fiscal_year, quarter)
            if self in q:
                return quarter

    @property
    def prev_quarter(self):
        """:returns: The previous quarter
        :rtype: FiscalQuarter
        """
        quarter = FiscalQuarter(self.fiscal_year, self.quarter)

        return quarter.prev_quarter

    @property
    def next_quarter(self):
        """:returns: The next quarter
        :rtype: FiscalQuarter
        """
        quarter = FiscalQuarter(self.fiscal_year, self.quarter)

        return quarter.next_quarter


class FiscalDate(datetime.date, _FiscalBase):
    """A wrapper around the builtin datetime.date class
    that provides the following attributes."""
    pass


class FiscalDateTime(datetime.datetime, _FiscalBase):
    """A wrapper around the builtin datetime.datetime class
    that provides the following attributes."""
    pass
