"""Utilities for managing the fiscal calendar."""

from __future__ import division, with_statement

__author__ = "Adam J. Stewart"
__version__ = "0.3.2"

import calendar
import contextlib
import datetime
import sys
import warnings


if not sys.warnoptions:
    warnings.simplefilter("default")

# Number of months in each quarter
MONTHS_PER_QUARTER = 12 // 4

MIN_QUARTER = 1
MAX_QUARTER = 4

# These global variables control the start of the fiscal year.
# The default is to use the U.S. federal government's fiscal year,
# but they can be changed to use any other fiscal year.
START_YEAR = "previous"
START_MONTH = 10
START_DAY = 1


def _validate_fiscal_calendar_params(start_year, start_month, start_day):
    """Raise an Exception if the calendar parameters are invalid.

    :param start_year: Relationship between the start of the fiscal year and
        the calendar year. Possible values: ``'previous'`` or ``'same'``.
    :type start_year: str
    :param start_month: The first month of the fiscal year
    :type start_month: int or str
    :param start_day: The first day of the first month of the fiscal year
    :type start_day: int or str
    :raises TypeError: If ``start_year`` is not a ``str``.
    :raises ValueError: If ``start_year`` is not ``'previous'`` or ``'same'``
    :raises ValueError: If ``start_month`` or ``start_day`` is not an int or
        int-like string
    :raises ValueError: If ``start_month`` or ``start_day`` is out of range
    """
    if not isinstance(start_year, str):
        raise TypeError("'start_year' must be a 'str', not: '%s'" % type(str))
    if start_year not in ("previous", "same"):
        msg = "'start_year' must be either 'previous' or 'same', not: '%s'"
        raise ValueError(msg % start_year)
    _check_day(start_month, start_day)


def setup_fiscal_calendar(start_year=None, start_month=None, start_day=None):
    """Modify the start of the fiscal calendar.

    :param start_year: Relationship between the start of the fiscal year and
        the calendar year. Possible values: ``'previous'`` or ``'same'``.
    :type start_year: str
    :param start_month: The first month of the fiscal year
    :type start_month: int or str
    :param start_day: The first day of the first month of the fiscal year
    :type start_day: int or str
    :raises ValueError: If ``start_year`` is not ``'previous'`` or ``'same'``
    :raises TypeError: If ``start_month`` or ``start_day`` is not an int or
        int-like string
    :raises ValueError: If ``start_month`` or ``start_day`` is out of range
    """
    global START_YEAR, START_MONTH, START_DAY

    # If arguments are omitted, use the currently active values.
    start_year = START_YEAR if start_year is None else start_year
    start_month = START_MONTH if start_month is None else start_month
    start_day = START_DAY if start_day is None else start_day

    _validate_fiscal_calendar_params(start_year, start_month, start_day)

    START_YEAR = start_year
    START_MONTH = start_month
    START_DAY = start_day


@contextlib.contextmanager
def fiscal_calendar(start_year=None, start_month=None, start_day=None):
    """A context manager that lets you modify the start of the fiscal calendar
    inside the scope of a with-statement.

    :param start_year: Relationship between the start of the fiscal year and
        the calendar year. Possible values: ``'previous'`` or ``'same'``.
    :type start_year: str
    :param start_month: The first month of the fiscal year
    :type start_month: int or str
    :param start_day: The first day of the first month of the fiscal year
    :type start_day: int or str
    :raises ValueError: If ``start_year`` is not ``'previous'`` or ``'same'``
    :raises TypeError: If ``start_month`` or ``start_day`` is not an int or
        int-like string
    :raises ValueError: If ``start_month`` or ``start_day`` is out of range
    """
    # If arguments are omitted, use the currently active values.
    start_year = START_YEAR if start_year is None else start_year
    start_month = START_MONTH if start_month is None else start_month
    start_day = START_DAY if start_day is None else start_day

    # Temporarily change global variables
    previous_values = (START_YEAR, START_MONTH, START_DAY)
    setup_fiscal_calendar(start_year, start_month, start_day)

    yield

    # Restore previous values
    setup_fiscal_calendar(*previous_values)


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
        raise TypeError(
            "an int or int-like string is required (got %s)" % (type(value).__name__)
        )


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
        raise ValueError(
            "year must be in %d..%d" % (datetime.MINYEAR, datetime.MAXYEAR), year
        )


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
        raise ValueError("month must be in %d..%d" % (1, 12), month)


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
        raise ValueError("day must be in %d..%d" % (1, max_day), day)


def _check_fiscal_day(fiscal_year, fiscal_day):
    """Check if day is a valid day of the fiscal year.

    :param fiscal_year: The fiscal year to test
    :param fiscal_day: The fiscal day to test
    :return: The fiscal day
    :rtype: int
    :raises TypeError: If year or day is not an int or int-like string
    :raises ValueError: If year or day is out of range
    """
    fiscal_year = _check_year(fiscal_year)
    fiscal_day = _check_int(fiscal_day)

    # Find the length of the year
    max_day = 366 if FiscalYear(fiscal_year).isleap else 365
    if 1 <= fiscal_day <= max_day:
        return fiscal_day
    else:
        raise ValueError("day must be in %d..%d" % (1, max_day), fiscal_day)


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
        raise ValueError(
            "quarter must be in %d..%d" % (MIN_QUARTER, MAX_QUARTER), quarter
        )


class FiscalYear(object):
    """A class representing a single fiscal year."""

    __slots__ = "_fiscal_year"

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

    @classmethod
    def current(cls):
        """Alternative constructor. Returns the current FiscalYear.

        :returns: A newly constructed FiscalYear object
        :rtype: FiscalYear
        """
        today = FiscalDate.today()
        return cls(today.fiscal_year)

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> fy = FiscalYear(2017)
        >>> repr(fy)
        'FiscalYear(2017)'
        """
        return "%s(%d)" % (self.__class__.__name__, self._fiscal_year)

    def __str__(self):
        """Convert to informal string, for str().

        >>> fy = FiscalYear(2017)
        >>> str(fy)
        'FY2017'
        """
        return "FY%d" % (self._fiscal_year)

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
        elif isinstance(item, (FiscalQuarter, FiscalMonth, FiscalDay)):
            return self._fiscal_year == item.fiscal_year
        elif isinstance(item, datetime.datetime):
            return self.start <= item <= self.end
        elif isinstance(item, datetime.date):
            return self.start.date() <= item <= self.end.date()
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(item).__name__)
            )

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

    @property
    def isleap(self):
        """returns: True if the fiscal year contains a leap day, else False
        :rtype: bool
        """
        fiscal_year = FiscalYear(self._fiscal_year)
        starts_on_or_before_possible_leap_day = (
            fiscal_year.start.month,
            fiscal_year.start.day,
        ) < (3, 1)

        if START_YEAR == "previous":
            if starts_on_or_before_possible_leap_day:
                calendar_year = self._fiscal_year - 1
            else:
                calendar_year = self._fiscal_year
        elif START_YEAR == "same":
            if starts_on_or_before_possible_leap_day:
                calendar_year = self._fiscal_year
            else:
                calendar_year = self._fiscal_year + 1

        return calendar.isleap(calendar_year)

    # Comparisons of FiscalYear objects with other

    def __lt__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year < other._fiscal_year
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __le__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year <= other._fiscal_year
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __eq__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year == other._fiscal_year
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __ne__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year != other._fiscal_year
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __gt__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year > other._fiscal_year
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __ge__(self, other):
        if isinstance(other, FiscalYear):
            return self._fiscal_year >= other._fiscal_year
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )


class FiscalQuarter(object):
    """A class representing a single fiscal quarter."""

    __slots__ = ["_fiscal_year", "_fiscal_quarter"]

    def __new__(cls, fiscal_year, fiscal_quarter):
        """Constructor.

        :param fiscal_year: The fiscal year
        :type fiscal_year: int or str
        :param fiscal_quarter: The fiscal quarter
        :type fiscal_quarter: int or str
        :returns: A newly constructed FiscalQuarter object
        :rtype: FiscalQuarter
        :raises TypeError: If fiscal_year or fiscal_quarter is not
            an int or int-like string
        :raises ValueError: If fiscal_year or fiscal_quarter is out of range
        """
        fiscal_year = _check_year(fiscal_year)
        fiscal_quarter = _check_quarter(fiscal_quarter)

        self = super(FiscalQuarter, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        self._fiscal_quarter = fiscal_quarter
        return self

    @classmethod
    def current(cls):
        """Alternative constructor. Returns the current FiscalQuarter.

        :returns: A newly constructed FiscalQuarter object
        :rtype: FiscalQuarter
        """
        today = FiscalDate.today()
        return cls(today.fiscal_year, today.fiscal_quarter)

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> q3 = FiscalQuarter(2017, 3)
        >>> repr(q3)
        'FiscalQuarter(2017, 3)'
        """
        return "%s(%d, %d)" % (
            self.__class__.__name__,
            self._fiscal_year,
            self._fiscal_quarter,
        )

    def __str__(self):
        """Convert to informal string, for str().

        >>> q3 = FiscalQuarter(2017, 3)
        >>> str(q3)
        'FY2017 Q3'
        """
        return "FY%d Q%d" % (self._fiscal_year, self._fiscal_quarter)

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
        elif isinstance(item, (FiscalMonth, FiscalDay)):
            return self.start <= item.start and item.end <= self.end
        elif isinstance(item, datetime.datetime):
            return self.start <= item <= self.end
        elif isinstance(item, datetime.date):
            return self.start.date() <= item <= self.end.date()
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(item).__name__)
            )

    # Read-only field accessors

    @property
    def fiscal_year(self):
        """:returns: The fiscal year
        :rtype: int
        """
        return self._fiscal_year

    @property
    def fiscal_quarter(self):
        """:returns: The fiscal quarter
        :rtype: int
        """
        return self._fiscal_quarter

    @property
    def quarter(self):
        warnings.warn(
            "FiscalQuarter.quarter is deprecated, "
            "use FiscalQuarter.fiscal_quarter instead",
            DeprecationWarning,
        )
        return self.fiscal_quarter

    @property
    def prev_fiscal_quarter(self):
        """:returns: The previous fiscal quarter
        :rtype: FiscalQuarter
        """
        fiscal_year = self._fiscal_year
        fiscal_quarter = self._fiscal_quarter - 1
        if fiscal_quarter == 0:
            fiscal_year -= 1
            fiscal_quarter = 4

        return FiscalQuarter(fiscal_year, fiscal_quarter)

    @property
    def prev_quarter(self):
        warnings.warn(
            "FiscalQuarter.prev_quarter is deprecated, "
            "use FiscalQuarter.prev_fiscal_quarter instead",
            DeprecationWarning,
        )
        return self.prev_fiscal_quarter

    @property
    def next_fiscal_quarter(self):
        """:returns: The next fiscal quarter
        :rtype: FiscalQuarter
        """
        fiscal_year = self._fiscal_year
        fiscal_quarter = self._fiscal_quarter + 1
        if fiscal_quarter == 5:
            fiscal_year += 1
            fiscal_quarter = 1

        return FiscalQuarter(fiscal_year, fiscal_quarter)

    @property
    def next_quarter(self):
        warnings.warn(
            "FiscalQuarter.next_quarter is deprecated, "
            "use FiscalQuarter.next_fiscal_quarter instead",
            DeprecationWarning,
        )
        return self.next_fiscal_quarter

    @property
    def start(self):
        """:returns: The start of the fiscal quarter
        :rtype: FiscalDateTime
        """

        # Find the first month of the fiscal quarter
        month = START_MONTH
        month += (self._fiscal_quarter - 1) * MONTHS_PER_QUARTER
        month %= 12
        if month == 0:
            month = 12

        # Find the calendar year of the start of the fiscal quarter
        if START_YEAR == "previous":
            year = self._fiscal_year - 1
        elif START_YEAR == "same":
            year = self._fiscal_year
        else:
            raise ValueError(
                "START_YEAR must be either 'previous' or 'same'", START_YEAR
            )

        if month < START_MONTH:
            year += 1

        # Find the last day of the month
        # If START_DAY is later, choose last day of month instead
        max_day = calendar.monthrange(year, month)[1]
        day = min(START_DAY, max_day)

        return FiscalDateTime(year, month, day, 0, 0, 0)

    @property
    def end(self):
        """:returns: The end of the fiscal quarter
        :rtype: FiscalDateTime
        """
        # Find the start of the next fiscal quarter
        next_start = self.next_fiscal_quarter.start

        # Substract 1 second
        end = next_start - datetime.timedelta(seconds=1)

        return FiscalDateTime(
            end.year,
            end.month,
            end.day,
            end.hour,
            end.minute,
            end.second,
            end.microsecond,
            end.tzinfo,
        )

    # Comparisons of FiscalQuarter objects with other

    def __lt__(self, other):
        if isinstance(other, FiscalQuarter):
            return (self._fiscal_year, self._fiscal_quarter) < (
                other._fiscal_year,
                other._fiscal_quarter,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __le__(self, other):
        if isinstance(other, FiscalQuarter):
            return (self._fiscal_year, self._fiscal_quarter) <= (
                other._fiscal_year,
                other._fiscal_quarter,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __eq__(self, other):
        if isinstance(other, FiscalQuarter):
            return (self._fiscal_year, self._fiscal_quarter) == (
                other._fiscal_year,
                other._fiscal_quarter,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __ne__(self, other):
        if isinstance(other, FiscalQuarter):
            return (self._fiscal_year, self._fiscal_quarter) != (
                other._fiscal_year,
                other._fiscal_quarter,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __gt__(self, other):
        if isinstance(other, FiscalQuarter):
            return (self._fiscal_year, self._fiscal_quarter) > (
                other._fiscal_year,
                other._fiscal_quarter,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __ge__(self, other):
        if isinstance(other, FiscalQuarter):
            return (self._fiscal_year, self._fiscal_quarter) >= (
                other._fiscal_year,
                other._fiscal_quarter,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )


class FiscalMonth(object):
    """A class representing a single fiscal month."""

    __slots__ = ["_fiscal_year", "_fiscal_month"]

    def __new__(cls, fiscal_year, fiscal_month):
        """Constructor.

        :param fiscal_year: The fiscal year
        :type fiscal_year: int or str
        :param fiscal_month: The fiscal month
        :type fiscal_month: int or str
        :returns: A newly constructed FiscalMonth object
        :rtype: FiscalMonth
        :raises TypeError: If fiscal_year or fiscal_month is not
            an int or int-like string
        :raises ValueError: If fiscal_year or fiscal_month is out of range
        """
        fiscal_year = _check_year(fiscal_year)
        fiscal_month = _check_month(fiscal_month)

        self = super(FiscalMonth, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        self._fiscal_month = fiscal_month
        return self

    @classmethod
    def current(cls):
        """Alternative constructor. Returns the current FiscalMonth.

        :returns: A newly constructed FiscalMonth object
        :rtype: FiscalMonth
        """
        today = FiscalDate.today()
        return cls(today.fiscal_year, today.fiscal_month)

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> fm = FiscalMonth(2017, 1)
        >>> repr(fm)
        'FiscalMonth(2017, 1)'
        """
        return "%s(%d, %d)" % (
            self.__class__.__name__,
            self._fiscal_year,
            self._fiscal_month,
        )

    def __str__(self):
        """Convert to informal string, for str().

        >>> fm = FiscalMonth(2017, 1)
        >>> str(fm)
        'FY2017 FM1'
        """
        return "FY%d FM%d" % (self._fiscal_year, self._fiscal_month)

    # TODO: Implement __format__ so that you can print
    # fiscal year as 17 or 2017 (%y or %Y)

    def __contains__(self, item):
        """Returns True if item in self, else False.

        :param item: The item to check
        :type item: FiscalMonth, FiscalDateTime,
            datetime, FiscalDate, or date
        :rtype: bool
        """
        if isinstance(item, FiscalMonth):
            return self == item
        elif isinstance(item, FiscalDay):
            return self.start <= item.start <= item.end <= self.end
        elif isinstance(item, datetime.datetime):
            return self.start <= item <= self.end
        elif isinstance(item, datetime.date):
            return self.start.date() <= item <= self.end.date()
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(item).__name__)
            )

    # Read-only field accessors

    @property
    def fiscal_year(self):
        """:returns: The fiscal year
        :rtype: int
        """
        return self._fiscal_year

    @property
    def fiscal_month(self):
        """:returns: The fiscal month
        :rtype: int
        """
        return self._fiscal_month

    @property
    def start(self):
        """:returns: Start of the fiscal month
        :rtype: FiscalDateTime
        """

        calendar_month = (START_MONTH + self._fiscal_month - 1) % 12
        if calendar_month == 0:
            calendar_month = 12

        month_is_on_or_after_start_month = calendar_month >= START_MONTH

        if START_YEAR == "previous":
            if month_is_on_or_after_start_month:
                calendar_year = self._fiscal_year - 1
            else:
                calendar_year = self._fiscal_year
        elif START_YEAR == "same":
            if month_is_on_or_after_start_month:
                calendar_year = self._fiscal_year
            else:
                calendar_year = self._fiscal_year + 1

        return FiscalDateTime(calendar_year, calendar_month, START_DAY)

    @property
    def end(self):
        """:returns: End of the fiscal month
        :rtype: FiscalDateTime
        """
        # Find the start of the next fiscal quarter
        next_start = self.next_fiscal_month.start

        # Substract 1 second
        end = next_start - datetime.timedelta(seconds=1)

        return FiscalDateTime(
            end.year,
            end.month,
            end.day,
            end.hour,
            end.minute,
            end.second,
            end.microsecond,
            end.tzinfo,
        )

    @property
    def prev_fiscal_month(self):
        """:returns: The previous fiscal month
        :rtype: FiscalMonth
        """
        fiscal_year = self._fiscal_year
        fiscal_month = self._fiscal_month - 1
        if fiscal_month == 0:
            fiscal_year -= 1
            fiscal_month = 12

        return FiscalMonth(fiscal_year, fiscal_month)

    @property
    def next_fiscal_month(self):
        """:returns: The next fiscal month
        :rtype: FiscalMonth
        """
        fiscal_year = self._fiscal_year
        fiscal_month = self._fiscal_month + 1
        if fiscal_month == 13:
            fiscal_year += 1
            fiscal_month = 1

        return FiscalMonth(fiscal_year, fiscal_month)

    # Comparisons of FiscalMonth objects with other

    def __lt__(self, other):
        if isinstance(other, FiscalMonth):
            return (self._fiscal_year, self._fiscal_month) < (
                other._fiscal_year,
                other._fiscal_month,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __le__(self, other):
        if isinstance(other, FiscalMonth):
            return (self._fiscal_year, self._fiscal_month) <= (
                other._fiscal_year,
                other._fiscal_month,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __eq__(self, other):
        if isinstance(other, FiscalMonth):
            return (self._fiscal_year, self._fiscal_month) == (
                other._fiscal_year,
                other._fiscal_month,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __ne__(self, other):
        if isinstance(other, FiscalMonth):
            return (self._fiscal_year, self._fiscal_month) != (
                other._fiscal_year,
                other._fiscal_month,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __gt__(self, other):
        if isinstance(other, FiscalMonth):
            return (self._fiscal_year, self._fiscal_month) > (
                other._fiscal_year,
                other._fiscal_month,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __ge__(self, other):
        if isinstance(other, FiscalMonth):
            return (self._fiscal_year, self._fiscal_month) >= (
                other._fiscal_year,
                other._fiscal_month,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )


class FiscalDay(object):
    """A class representing a single fiscal day."""

    __slots__ = ["_fiscal_year", "_fiscal_day"]

    def __new__(cls, fiscal_year, fiscal_day):
        """Constructor.

        :param fiscal_year: The fiscal year
        :type fiscal_year: int or str
        :param fiscal_day: The fiscal day
        :type fiscal_day: int or str
        :returns: A newly constructed FiscalDay object
        :rtype: FiscalDay
        :raises TypeError: If fiscal_year or fiscal_day is not
            an int or int-like string
        :raises ValueError: If fiscal_year or fiscal_day is out of range
        """
        fiscal_year = _check_year(fiscal_year)
        fiscal_day = _check_fiscal_day(fiscal_year, fiscal_day)

        self = super(FiscalDay, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        self._fiscal_day = fiscal_day
        return self

    @classmethod
    def current(cls):
        """Alternative constructor. Returns the current FiscalDay.

        :returns: A newly constructed FiscalDay object
        :rtype: FiscalDay
        """
        today = FiscalDate.today()
        return cls(today.fiscal_year, today.fiscal_day)

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> fd = FiscalDay(2017, 1)
        >>> repr(fd)
        'FiscalDay(2017, 1)'
        """
        return "%s(%d, %d)" % (
            self.__class__.__name__,
            self._fiscal_year,
            self._fiscal_day,
        )

    def __str__(self):
        """Convert to informal string, for str().

        >>> fd = FiscalDay(2017, 1)
        >>> str(fd)
        'FY2017 FD1'
        """
        return "FY%d FD%d" % (self._fiscal_year, self._fiscal_day)

    # TODO: Implement __format__ so that you can print
    # fiscal year as 17 or 2017 (%y or %Y)

    def __contains__(self, item):
        """Returns True if item in self, else False.

        :param item: The item to check
        :type item: FiscalDay, FiscalDateTime,
            datetime, FiscalDate, or date
        :rtype: bool
        """
        if isinstance(item, FiscalDay):
            return self == item
        elif isinstance(item, datetime.datetime):
            return self.start <= item <= self.end
        elif isinstance(item, datetime.date):
            return self.start.date() <= item <= self.end.date()
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(item).__name__)
            )

    # Read-only field accessors

    @property
    def fiscal_year(self):
        """:returns: The fiscal year
        :rtype: int
        """
        return self._fiscal_year

    @property
    def fiscal_quarter(self):
        """:returns: The fiscal quarter
        :rtype: int
        """
        return self.start.fiscal_quarter

    @property
    def fiscal_month(self):
        """:returns: The fiscal month
        :rtype: int
        """
        return self.start.fiscal_month

    @property
    def fiscal_day(self):
        """:returns: The fiscal day
        :rtype: int
        """
        return self._fiscal_day

    @property
    def start(self):
        """:returns: Start of the fiscal day
        :rtype: FiscalDateTime
        """

        fiscal_year = FiscalYear(self._fiscal_year)
        days_elapsed = datetime.timedelta(days=self._fiscal_day - 1)
        start = fiscal_year.start + days_elapsed
        return FiscalDateTime(start.year, start.month, start.day, 0, 0, 0)

    @property
    def end(self):
        """:returns: End of the fiscal day
        :rtype: FiscalDateTime
        """
        # Find the start of the next fiscal quarter
        next_start = self.next_fiscal_day.start

        # Substract 1 second
        end = next_start - datetime.timedelta(seconds=1)

        return FiscalDateTime(
            end.year,
            end.month,
            end.day,
            end.hour,
            end.minute,
            end.second,
            end.microsecond,
            end.tzinfo,
        )

    @property
    def prev_fiscal_day(self):
        """:returns: The previous fiscal day
        :rtype: FiscalDay
        """
        fiscal_year = self._fiscal_year
        fiscal_day = self._fiscal_day - 1
        if fiscal_day == 0:
            fiscal_year -= 1
            try:
                fiscal_day = _check_fiscal_day(fiscal_year, 366)
            except ValueError:
                fiscal_day = _check_fiscal_day(fiscal_year, 365)

        return FiscalDay(fiscal_year, fiscal_day)

    @property
    def next_fiscal_day(self):
        """:returns: The next fiscal day
        :rtype: FiscalDay
        """
        fiscal_year = self._fiscal_year
        try:
            fiscal_day = _check_fiscal_day(fiscal_year, self._fiscal_day + 1)
        except ValueError:
            fiscal_year += 1
            fiscal_day = 1

        return FiscalDay(fiscal_year, fiscal_day)

    # Comparisons of FiscalDay objects with other

    def __lt__(self, other):
        if isinstance(other, FiscalDay):
            return (self._fiscal_year, self._fiscal_day) < (
                other._fiscal_year,
                other._fiscal_day,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __le__(self, other):
        if isinstance(other, FiscalDay):
            return (self._fiscal_year, self._fiscal_day) <= (
                other._fiscal_year,
                other._fiscal_day,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __eq__(self, other):
        if isinstance(other, FiscalDay):
            return (self._fiscal_year, self._fiscal_day) == (
                other._fiscal_year,
                other._fiscal_day,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __ne__(self, other):
        if isinstance(other, FiscalDay):
            return (self._fiscal_year, self._fiscal_day) != (
                other._fiscal_year,
                other._fiscal_day,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __gt__(self, other):
        if isinstance(other, FiscalDay):
            return (self._fiscal_year, self._fiscal_day) > (
                other._fiscal_year,
                other._fiscal_day,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )

    def __ge__(self, other):
        if isinstance(other, FiscalDay):
            return (self._fiscal_year, self._fiscal_day) >= (
                other._fiscal_year,
                other._fiscal_day,
            )
        else:
            raise TypeError(
                "can't compare '%s' to '%s'"
                % (type(self).__name__, type(other).__name__)
            )


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
    def fiscal_quarter(self):
        """:returns: The fiscal quarter
        :rtype: int
        """
        for quarter in range(1, 5):
            q = FiscalQuarter(self.fiscal_year, quarter)
            if self in q:
                return quarter

    @property
    def quarter(self):
        warnings.warn(
            "FiscalDate(Time).quarter is deprecated, "
            "use FiscalDate(Time).fiscal_quarter instead",
            DeprecationWarning,
        )
        return self.fiscal_quarter

    @property
    def fiscal_month(self):
        """:returns: The fiscal month
        :rtype: int
        """
        for month in range(1, 13):
            m = FiscalMonth(self.fiscal_year, month)
            if self in m:
                return month

    @property
    def fiscal_day(self):
        """:returns: The fiscal day
        :rtype: int
        """
        fiscal_year = FiscalYear(self.fiscal_year)
        year_start = fiscal_year.start

        if isinstance(self, FiscalDate):
            year_start = year_start.date()

        return (self - year_start).days + 1

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
    def prev_fiscal_quarter(self):
        """:returns: The previous fiscal quarter
        :rtype: FiscalQuarter
        """
        fiscal_quarter = FiscalQuarter(self.fiscal_year, self.fiscal_quarter)

        return fiscal_quarter.prev_fiscal_quarter

    @property
    def prev_quarter(self):
        warnings.warn(
            "FiscalDate(Time).prev_quarter is deprecated, "
            "use FiscalDate(Time).prev_fiscal_quarter instead",
            DeprecationWarning,
        )
        return self.prev_fiscal_quarter

    @property
    def next_fiscal_quarter(self):
        """:returns: The next fiscal quarter
        :rtype: FiscalQuarter
        """
        fiscal_quarter = FiscalQuarter(self.fiscal_year, self.fiscal_quarter)

        return fiscal_quarter.next_fiscal_quarter

    @property
    def next_quarter(self):
        warnings.warn(
            "FiscalDate(Time).next_quarter is deprecated, "
            "use FiscalDate(Time).next_fiscal_quarter instead",
            DeprecationWarning,
        )
        return self.next_fiscal_quarter

    @property
    def prev_fiscal_month(self):
        """:returns: The previous fiscal month
        :rtype: FiscalMonth
        """
        fiscal_month = FiscalMonth(self.fiscal_year, self.fiscal_month)

        return fiscal_month.prev_fiscal_month

    @property
    def next_fiscal_month(self):
        """:returns: The next fiscal month
        :rtype: FiscalMonth
        """
        fiscal_month = FiscalMonth(self.fiscal_year, self.fiscal_month)

        return fiscal_month.next_fiscal_month

    @property
    def prev_fiscal_day(self):
        """:returns: The previous fiscal day
        :rtype: FiscalDay
        """
        fiscal_day = FiscalDay(self.fiscal_year, self.fiscal_day)

        return fiscal_day.prev_fiscal_day

    @property
    def next_fiscal_day(self):
        """:returns: The next fiscal day
        :rtype: FiscalDay
        """
        fiscal_day = FiscalDay(self.fiscal_year, self.fiscal_day)

        return fiscal_day.next_fiscal_day


class FiscalDate(datetime.date, _FiscalBase):
    """A wrapper around the builtin datetime.date class
    that provides the following attributes."""

    pass


class FiscalDateTime(datetime.datetime, _FiscalBase):
    """A wrapper around the builtin datetime.datetime class
    that provides the following attributes."""

    pass
