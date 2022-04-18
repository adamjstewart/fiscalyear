"""Utilities for managing the fiscal calendar."""

import calendar
import contextlib
import datetime
from typing import Iterator, Optional, Union, cast

__author__ = "Adam J. Stewart"
__version__ = "0.4.0"

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


def _validate_fiscal_calendar_params(
    start_year: str, start_month: int, start_day: int
) -> None:
    """Raise an Exception if the calendar parameters are invalid.

    :param start_year: Relationship between the start of the fiscal year and
        the calendar year. Possible values: ``'previous'`` or ``'same'``.
    :param start_month: The first month of the fiscal year
    :param start_day: The first day of the first month of the fiscal year
    :raises ValueError: If ``start_year`` is not ``'previous'`` or ``'same'``
    :raises ValueError: If ``start_month`` or ``start_day`` is out of range
    """
    if start_year not in ["previous", "same"]:
        msg = f"'start_year' must be either 'previous' or 'same', not: '{start_year}'"
        raise ValueError(msg)
    _check_day(start_month, start_day)


def setup_fiscal_calendar(
    start_year: Optional[str] = None,
    start_month: Optional[int] = None,
    start_day: Optional[int] = None,
) -> None:
    """Modify the start of the fiscal calendar.

    :param start_year: Relationship between the start of the fiscal year and
        the calendar year. Possible values: ``'previous'`` or ``'same'``.
    :param start_month: The first month of the fiscal year
    :param start_day: The first day of the first month of the fiscal year
    :raises ValueError: If ``start_year`` is not ``'previous'`` or ``'same'``
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
def fiscal_calendar(
    start_year: Optional[str] = None,
    start_month: Optional[int] = None,
    start_day: Optional[int] = None,
) -> Iterator[None]:
    """A context manager that lets you modify the start of the fiscal calendar
    inside the scope of a with-statement.

    :param start_year: Relationship between the start of the fiscal year and
        the calendar year. Possible values: ``'previous'`` or ``'same'``.
    :param start_month: The first month of the fiscal year
    :param start_day: The first day of the first month of the fiscal year
    :raises ValueError: If ``start_year`` is not ``'previous'`` or ``'same'``
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


def _check_year(year: int) -> int:
    """Check if ``year`` is a valid year.

    :param year: The year to test
    :return: The year
    :raises ValueError: If ``year`` is out of range
    """
    if datetime.MINYEAR <= year <= datetime.MAXYEAR:
        return year
    else:
        raise ValueError(f"year {year} is out of range")


def _check_month(month: int) -> int:
    """Check if ``month`` is a valid month.

    :param month: The month to test
    :return: The month
    :raises ValueError: If ``month`` is out of range
    """
    if 1 <= month <= 12:
        return month
    else:
        raise ValueError(f"month {month} is out of range")


def _check_day(month: int, day: int) -> int:
    """Check if ``day`` is a valid day of month.

    :param month: The month to test
    :param day: The day to test
    :return: The day
    :raises ValueError: If ``month`` or ``day`` is out of range
    """
    month = _check_month(month)

    # Find the last day of the month
    # Use a non-leap year
    max_day = calendar.monthrange(2001, month)[1]

    if 1 <= day <= max_day:
        return day
    else:
        raise ValueError(f"day {day} is out of range")


def _check_fiscal_day(fiscal_year: int, fiscal_day: int) -> int:
    """Check if ``day`` is a valid day of the fiscal year.

    :param fiscal_year: The fiscal year to test
    :param fiscal_day: The fiscal day to test
    :return: The fiscal day
    :raises ValueError: If ``year`` or ``day`` is out of range
    """
    fiscal_year = _check_year(fiscal_year)

    # Find the length of the year
    max_day = 366 if FiscalYear(fiscal_year).isleap else 365
    if 1 <= fiscal_day <= max_day:
        return fiscal_day
    else:
        raise ValueError(f"fiscal_day {fiscal_day} is out of range")


def _check_quarter(quarter: int) -> int:
    """Check if ``quarter`` is a valid quarter.

    :param quarter: The quarter to test
    :return: The quarter
    :raises ValueError: If ``quarter`` is out of range
    """
    if MIN_QUARTER <= quarter <= MAX_QUARTER:
        return quarter
    else:
        raise ValueError(f"quarter {quarter} is out of range")


class _Hashable:
    """A class to make Fiscal objects hashable"""

    def __hash__(self) -> int:
        """Unique hash of an object instance based on __slots__

        :returns: a unique hash
        """
        return hash(tuple(map(lambda x: getattr(self, x), self.__slots__)))


class FiscalYear(_Hashable):
    """A class representing a single fiscal year."""

    __slots__ = ["_fiscal_year"]
    __hash__ = _Hashable.__hash__

    _fiscal_year: int

    def __new__(cls, fiscal_year: int) -> "FiscalYear":
        """Constructor.

        :param fiscal_year: The fiscal year
        :returns: A newly constructed FiscalYear object
        :raises ValueError: If ``fiscal_year`` is out of range
        """
        fiscal_year = _check_year(fiscal_year)

        self = super(FiscalYear, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        return self

    @classmethod
    def current(cls) -> "FiscalYear":
        """Alternative constructor. Returns the current FiscalYear.

        :returns: A newly constructed FiscalYear object
        """
        today = FiscalDate.today()
        return cls(today.fiscal_year)

    def __repr__(self) -> str:
        """Convert to formal string, for repr().

        >>> fy = FiscalYear(2017)
        >>> repr(fy)
        'FiscalYear(2017)'
        """
        return f"{self.__class__.__name__}({self._fiscal_year})"

    def __str__(self) -> str:
        """Convert to informal string, for str().

        >>> fy = FiscalYear(2017)
        >>> str(fy)
        'FY2017'
        """
        return f"FY{self._fiscal_year}"

    # TODO: Implement __format__ so that you can print
    # fiscal year as 17 or 2017 (%y or %Y)

    def __contains__(
        self,
        item: Union[
            "FiscalYear",
            "FiscalQuarter",
            "FiscalMonth",
            "FiscalDay",
            datetime.datetime,
            datetime.date,
        ],
    ) -> bool:
        """:param item: The item to check
        :returns: True if item in self, else False
        """
        if isinstance(item, FiscalYear):
            return self == item
        elif isinstance(item, (FiscalQuarter, FiscalMonth, FiscalDay)):
            return self._fiscal_year == item.fiscal_year
        elif isinstance(item, datetime.datetime):
            return self.start <= item <= self.end
        else:
            return self.start.date() <= item <= self.end.date()

    # Read-only field accessors

    @property
    def fiscal_year(self) -> int:
        """:returns: The fiscal year"""
        return self._fiscal_year

    @property
    def prev_fiscal_year(self) -> "FiscalYear":
        """:returns: The previous fiscal year"""
        return FiscalYear(self._fiscal_year - 1)

    @property
    def next_fiscal_year(self) -> "FiscalYear":
        """:returns: The next fiscal year"""
        return FiscalYear(self._fiscal_year + 1)

    @property
    def start(self) -> "FiscalDateTime":
        """:returns: Start of the fiscal year"""
        return self.q1.start

    @property
    def end(self) -> "FiscalDateTime":
        """:returns: End of the fiscal year"""
        return self.q4.end

    @property
    def q1(self) -> "FiscalQuarter":
        """:returns: The first quarter of the fiscal year"""
        return FiscalQuarter(self._fiscal_year, 1)

    @property
    def q2(self) -> "FiscalQuarter":
        """:returns: The second quarter of the fiscal year"""
        return FiscalQuarter(self._fiscal_year, 2)

    @property
    def q3(self) -> "FiscalQuarter":
        """:returns: The third quarter of the fiscal year"""
        return FiscalQuarter(self._fiscal_year, 3)

    @property
    def q4(self) -> "FiscalQuarter":
        """:returns: The fourth quarter of the fiscal year"""
        return FiscalQuarter(self._fiscal_year, 4)

    @property
    def isleap(self) -> bool:
        """returns: True if the fiscal year contains a leap day, else False"""
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

    def __lt__(self, other: "FiscalYear") -> bool:
        return self._fiscal_year < other._fiscal_year

    def __le__(self, other: "FiscalYear") -> bool:
        return self._fiscal_year <= other._fiscal_year

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FiscalYear):
            return self._fiscal_year == other._fiscal_year
        else:
            raise TypeError(
                f"can't compare '{type(self).__name__}' to '{type(other).__name__}'"
            )

    def __ne__(self, other: object) -> bool:
        if isinstance(other, FiscalYear):
            return self._fiscal_year != other._fiscal_year
        else:
            raise TypeError(
                f"can't compare '{type(self).__name__}' to '{type(other).__name__}'"
            )

    def __gt__(self, other: "FiscalYear") -> bool:
        return self._fiscal_year > other._fiscal_year

    def __ge__(self, other: "FiscalYear") -> bool:
        return self._fiscal_year >= other._fiscal_year


class FiscalQuarter(_Hashable):
    """A class representing a single fiscal quarter."""

    __slots__ = ["_fiscal_year", "_fiscal_quarter"]
    __hash__ = _Hashable.__hash__

    _fiscal_year: int
    _fiscal_quarter: int

    def __new__(cls, fiscal_year: int, fiscal_quarter: int) -> "FiscalQuarter":
        """Constructor.

        :param fiscal_year: The fiscal year
        :param fiscal_quarter: The fiscal quarter
        :returns: A newly constructed FiscalQuarter object
        :raises ValueError: If fiscal_year or fiscal_quarter is out of range
        """
        fiscal_year = _check_year(fiscal_year)
        fiscal_quarter = _check_quarter(fiscal_quarter)

        self = super(FiscalQuarter, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        self._fiscal_quarter = fiscal_quarter
        return self

    @classmethod
    def current(cls) -> "FiscalQuarter":
        """Alternative constructor. Returns the current FiscalQuarter.

        :returns: A newly constructed FiscalQuarter object
        """
        today = FiscalDate.today()
        return cls(today.fiscal_year, today.fiscal_quarter)

    def __repr__(self) -> str:
        """Convert to formal string, for repr().

        >>> q3 = FiscalQuarter(2017, 3)
        >>> repr(q3)
        'FiscalQuarter(2017, 3)'
        """
        return f"{self.__class__.__name__}({self._fiscal_year}, {self._fiscal_quarter})"

    def __str__(self) -> str:
        """Convert to informal string, for str().

        >>> q3 = FiscalQuarter(2017, 3)
        >>> str(q3)
        'FY2017 Q3'
        """
        return f"FY{self._fiscal_year} Q{self._fiscal_quarter}"

    # TODO: Implement __format__ so that you can print
    # fiscal year as 17 or 2017 (%y or %Y)

    def __contains__(
        self,
        item: Union[
            "FiscalQuarter",
            "FiscalMonth",
            "FiscalDay",
            datetime.datetime,
            datetime.date,
        ],
    ) -> bool:
        """Returns True if item in self, else False.

        :param item: The item to check
        """
        if isinstance(item, FiscalQuarter):
            return self == item
        elif isinstance(item, (FiscalMonth, FiscalDay)):
            return self.start <= item.start and item.end <= self.end
        elif isinstance(item, datetime.datetime):
            return self.start <= item <= self.end
        elif isinstance(item, datetime.date):
            return self.start.date() <= item <= self.end.date()

    # Read-only field accessors

    @property
    def fiscal_year(self) -> int:
        """:returns: The fiscal year"""
        return self._fiscal_year

    @property
    def fiscal_quarter(self) -> int:
        """:returns: The fiscal quarter"""
        return self._fiscal_quarter

    @property
    def prev_fiscal_quarter(self) -> "FiscalQuarter":
        """:returns: The previous fiscal quarter"""
        fiscal_year = self._fiscal_year
        fiscal_quarter = self._fiscal_quarter - 1
        if fiscal_quarter == 0:
            fiscal_year -= 1
            fiscal_quarter = 4

        return FiscalQuarter(fiscal_year, fiscal_quarter)

    @property
    def next_fiscal_quarter(self) -> "FiscalQuarter":
        """:returns: The next fiscal quarter"""
        fiscal_year = self._fiscal_year
        fiscal_quarter = self._fiscal_quarter + 1
        if fiscal_quarter == 5:
            fiscal_year += 1
            fiscal_quarter = 1

        return FiscalQuarter(fiscal_year, fiscal_quarter)

    @property
    def start(self) -> "FiscalDateTime":
        """:returns: The start of the fiscal quarter"""

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
    def end(self) -> "FiscalDateTime":
        """:returns: The end of the fiscal quarter"""
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

    def __lt__(self, other: "FiscalQuarter") -> bool:
        return (self._fiscal_year, self._fiscal_quarter) < (
            other._fiscal_year,
            other._fiscal_quarter,
        )

    def __le__(self, other: "FiscalQuarter") -> bool:
        return (self._fiscal_year, self._fiscal_quarter) <= (
            other._fiscal_year,
            other._fiscal_quarter,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FiscalQuarter):
            return (self._fiscal_year, self._fiscal_quarter) == (
                other._fiscal_year,
                other._fiscal_quarter,
            )
        else:
            raise TypeError(
                f"can't compare '{type(self).__name__}' to '{type(other).__name__}'"
            )

    def __ne__(self, other: object) -> bool:
        if isinstance(other, FiscalQuarter):
            return (self._fiscal_year, self._fiscal_quarter) != (
                other._fiscal_year,
                other._fiscal_quarter,
            )
        else:
            raise TypeError(
                f"can't compare '{type(self).__name__}' to '{type(other).__name__}'"
            )

    def __gt__(self, other: "FiscalQuarter") -> bool:
        return (self._fiscal_year, self._fiscal_quarter) > (
            other._fiscal_year,
            other._fiscal_quarter,
        )

    def __ge__(self, other: "FiscalQuarter") -> bool:
        return (self._fiscal_year, self._fiscal_quarter) >= (
            other._fiscal_year,
            other._fiscal_quarter,
        )


class FiscalMonth(_Hashable):
    """A class representing a single fiscal month."""

    __slots__ = ["_fiscal_year", "_fiscal_month"]
    __hash__ = _Hashable.__hash__

    _fiscal_year: int
    _fiscal_month: int

    def __new__(cls, fiscal_year: int, fiscal_month: int) -> "FiscalMonth":
        """Constructor.

        :param fiscal_year: The fiscal year
        :param fiscal_month: The fiscal month
        :returns: A newly constructed FiscalMonth object
        :raises ValueError: If fiscal_year or fiscal_month is out of range
        """
        fiscal_year = _check_year(fiscal_year)
        fiscal_month = _check_month(fiscal_month)

        self = super(FiscalMonth, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        self._fiscal_month = fiscal_month
        return self

    @classmethod
    def current(cls) -> "FiscalMonth":
        """Alternative constructor. Returns the current FiscalMonth.

        :returns: A newly constructed FiscalMonth object
        """
        today = FiscalDate.today()
        return cls(today.fiscal_year, today.fiscal_month)

    def __repr__(self) -> str:
        """Convert to formal string, for repr().

        >>> fm = FiscalMonth(2017, 1)
        >>> repr(fm)
        'FiscalMonth(2017, 1)'
        """
        return f"{self.__class__.__name__}({self._fiscal_year}, {self._fiscal_month})"

    def __str__(self) -> str:
        """Convert to informal string, for str().

        >>> fm = FiscalMonth(2017, 1)
        >>> str(fm)
        'FY2017 FM1'
        """
        return f"FY{self._fiscal_year} FM{self._fiscal_month}"

    # TODO: Implement __format__ so that you can print
    # fiscal year as 17 or 2017 (%y or %Y)

    def __contains__(
        self, item: Union["FiscalMonth", "FiscalDay", datetime.datetime, datetime.date]
    ) -> bool:
        """Returns True if item in self, else False.

        :param item: The item to check
        """
        if isinstance(item, FiscalMonth):
            return self == item
        elif isinstance(item, FiscalDay):
            return self.start <= item.start <= item.end <= self.end
        elif isinstance(item, datetime.datetime):
            return self.start <= item <= self.end
        elif isinstance(item, datetime.date):
            return self.start.date() <= item <= self.end.date()

    # Read-only field accessors

    @property
    def fiscal_year(self) -> int:
        """:returns: The fiscal year"""
        return self._fiscal_year

    @property
    def fiscal_month(self) -> int:
        """:returns: The fiscal month"""
        return self._fiscal_month

    @property
    def start(self) -> "FiscalDateTime":
        """:returns: Start of the fiscal month"""

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
    def end(self) -> "FiscalDateTime":
        """:returns: End of the fiscal month"""
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
    def prev_fiscal_month(self) -> "FiscalMonth":
        """:returns: The previous fiscal month"""
        fiscal_year = self._fiscal_year
        fiscal_month = self._fiscal_month - 1
        if fiscal_month == 0:
            fiscal_year -= 1
            fiscal_month = 12

        return FiscalMonth(fiscal_year, fiscal_month)

    @property
    def next_fiscal_month(self) -> "FiscalMonth":
        """:returns: The next fiscal month"""
        fiscal_year = self._fiscal_year
        fiscal_month = self._fiscal_month + 1
        if fiscal_month == 13:
            fiscal_year += 1
            fiscal_month = 1

        return FiscalMonth(fiscal_year, fiscal_month)

    # Comparisons of FiscalMonth objects with other

    def __lt__(self, other: "FiscalMonth") -> bool:
        return (self._fiscal_year, self._fiscal_month) < (
            other._fiscal_year,
            other._fiscal_month,
        )

    def __le__(self, other: "FiscalMonth") -> bool:
        return (self._fiscal_year, self._fiscal_month) <= (
            other._fiscal_year,
            other._fiscal_month,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FiscalMonth):
            return (self._fiscal_year, self._fiscal_month) == (
                other._fiscal_year,
                other._fiscal_month,
            )
        else:
            raise TypeError(
                f"can't compare '{type(self).__name__}' to '{type(other).__name__}'"
            )

    def __ne__(self, other: object) -> bool:
        if isinstance(other, FiscalMonth):
            return (self._fiscal_year, self._fiscal_month) != (
                other._fiscal_year,
                other._fiscal_month,
            )
        else:
            raise TypeError(
                f"can't compare '{type(self).__name__}' to '{type(other).__name__}'"
            )

    def __gt__(self, other: "FiscalMonth") -> bool:
        return (self._fiscal_year, self._fiscal_month) > (
            other._fiscal_year,
            other._fiscal_month,
        )

    def __ge__(self, other: "FiscalMonth") -> bool:
        return (self._fiscal_year, self._fiscal_month) >= (
            other._fiscal_year,
            other._fiscal_month,
        )


class FiscalDay(_Hashable):
    """A class representing a single fiscal day."""

    __slots__ = ["_fiscal_year", "_fiscal_day"]
    __hash__ = _Hashable.__hash__

    _fiscal_year: int
    _fiscal_day: int

    def __new__(cls, fiscal_year: int, fiscal_day: int) -> "FiscalDay":
        """Constructor.

        :param fiscal_year: The fiscal year
        :param fiscal_day: The fiscal day
        :returns: A newly constructed FiscalDay object
        :raises ValueError: If fiscal_year or fiscal_day is out of range
        """
        fiscal_year = _check_year(fiscal_year)
        fiscal_day = _check_fiscal_day(fiscal_year, fiscal_day)

        self = super(FiscalDay, cls).__new__(cls)
        self._fiscal_year = fiscal_year
        self._fiscal_day = fiscal_day
        return self

    @classmethod
    def current(cls) -> "FiscalDay":
        """Alternative constructor. Returns the current FiscalDay.

        :returns: A newly constructed FiscalDay object
        """
        today = FiscalDate.today()
        return cls(today.fiscal_year, today.fiscal_day)

    def __repr__(self) -> str:
        """Convert to formal string, for repr().

        >>> fd = FiscalDay(2017, 1)
        >>> repr(fd)
        'FiscalDay(2017, 1)'
        """
        return f"{self.__class__.__name__}({self._fiscal_year}, {self._fiscal_day})"

    def __str__(self) -> str:
        """Convert to informal string, for str().

        >>> fd = FiscalDay(2017, 1)
        >>> str(fd)
        'FY2017 FD1'
        """
        return f"FY{self._fiscal_year} FD{self._fiscal_day}"

    # TODO: Implement __format__ so that you can print
    # fiscal year as 17 or 2017 (%y or %Y)

    def __contains__(
        self, item: Union["FiscalDay", datetime.datetime, datetime.date]
    ) -> bool:
        """Returns True if item in self, else False.

        :param item: The item to check
        """
        if isinstance(item, FiscalDay):
            return self == item
        elif isinstance(item, datetime.datetime):
            return self.start <= item <= self.end
        elif isinstance(item, datetime.date):
            return self.start.date() <= item <= self.end.date()

    # Read-only field accessors

    @property
    def fiscal_year(self) -> int:
        """:returns: The fiscal year"""
        return self._fiscal_year

    @property
    def fiscal_quarter(self) -> int:
        """:returns: The fiscal quarter"""
        return self.start.fiscal_quarter

    @property
    def fiscal_month(self) -> int:
        """:returns: The fiscal month"""
        return self.start.fiscal_month

    @property
    def fiscal_day(self) -> int:
        """:returns: The fiscal day"""
        return self._fiscal_day

    @property
    def start(self) -> "FiscalDateTime":
        """:returns: Start of the fiscal day"""

        fiscal_year = FiscalYear(self._fiscal_year)
        days_elapsed = datetime.timedelta(days=self._fiscal_day - 1)
        start = fiscal_year.start + days_elapsed
        return FiscalDateTime(start.year, start.month, start.day, 0, 0, 0)

    @property
    def end(self) -> "FiscalDateTime":
        """:returns: End of the fiscal day"""
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
    def prev_fiscal_day(self) -> "FiscalDay":
        """:returns: The previous fiscal day"""
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
    def next_fiscal_day(self) -> "FiscalDay":
        """:returns: The next fiscal day"""
        fiscal_year = self._fiscal_year
        try:
            fiscal_day = _check_fiscal_day(fiscal_year, self._fiscal_day + 1)
        except ValueError:
            fiscal_year += 1
            fiscal_day = 1

        return FiscalDay(fiscal_year, fiscal_day)

    # Comparisons of FiscalDay objects with other

    def __lt__(self, other: "FiscalDay") -> bool:
        return (self._fiscal_year, self._fiscal_day) < (
            other._fiscal_year,
            other._fiscal_day,
        )

    def __le__(self, other: "FiscalDay") -> bool:
        return (self._fiscal_year, self._fiscal_day) <= (
            other._fiscal_year,
            other._fiscal_day,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FiscalDay):
            return (self._fiscal_year, self._fiscal_day) == (
                other._fiscal_year,
                other._fiscal_day,
            )
        else:
            raise TypeError(
                f"can't compare '{type(self).__name__}' to '{type(other).__name__}'"
            )

    def __ne__(self, other: object) -> bool:
        if isinstance(other, FiscalDay):
            return (self._fiscal_year, self._fiscal_day) != (
                other._fiscal_year,
                other._fiscal_day,
            )
        else:
            raise TypeError(
                f"can't compare '{type(self).__name__}' to '{type(other).__name__}'"
            )

    def __gt__(self, other: "FiscalDay") -> bool:
        return (self._fiscal_year, self._fiscal_day) > (
            other._fiscal_year,
            other._fiscal_day,
        )

    def __ge__(self, other: "FiscalDay") -> bool:
        return (self._fiscal_year, self._fiscal_day) >= (
            other._fiscal_year,
            other._fiscal_day,
        )


class _FiscalMixin:
    """Mixin for FiscalDate and FiscalDateTime that
    provides the following common attributes in addition to
    those provided by datetime.date and datetime.datetime:
    """

    @property
    def fiscal_year(self) -> int:
        """:returns: The fiscal year"""

        fiscal_self = cast(Union["FiscalDate", "FiscalDateTime"], self)

        # The fiscal year can be at most 1 year away from the calendar year
        if fiscal_self in FiscalYear(fiscal_self.year):
            return fiscal_self.year
        elif fiscal_self in FiscalYear(fiscal_self.year + 1):
            return fiscal_self.year + 1
        else:
            return fiscal_self.year - 1

    @property
    def fiscal_quarter(self) -> int:
        """:returns: The fiscal quarter"""
        fiscal_self = cast(Union["FiscalDate", "FiscalDateTime"], self)
        for quarter in range(1, 5):
            q = FiscalQuarter(fiscal_self.fiscal_year, quarter)
            if fiscal_self in q:
                break
        return quarter

    @property
    def fiscal_month(self) -> int:
        """:returns: The fiscal month"""
        fiscal_self = cast(Union["FiscalDate", "FiscalDateTime"], self)
        for month in range(1, 13):
            m = FiscalMonth(fiscal_self.fiscal_year, month)
            if fiscal_self in m:
                break
        return month

    @property
    def fiscal_day(self) -> int:
        """:returns: The fiscal day"""

        fiscal_self = cast(Union["FiscalDate", "FiscalDateTime"], self)

        fiscal_year = FiscalYear(fiscal_self.fiscal_year)
        year_start = fiscal_year.start

        if isinstance(fiscal_self, FiscalDate):
            delta = cast(datetime.date, fiscal_self) - year_start.date()
        else:
            delta = fiscal_self - year_start

        return delta.days + 1

    @property
    def prev_fiscal_year(self) -> FiscalYear:
        """:returns: The previous fiscal year"""
        return FiscalYear(self.fiscal_year - 1)

    @property
    def next_fiscal_year(self) -> FiscalYear:
        """:returns: The next fiscal year"""
        return FiscalYear(self.fiscal_year + 1)

    @property
    def prev_fiscal_quarter(self) -> FiscalQuarter:
        """:returns: The previous fiscal quarter"""
        fiscal_quarter = FiscalQuarter(self.fiscal_year, self.fiscal_quarter)

        return fiscal_quarter.prev_fiscal_quarter

    @property
    def next_fiscal_quarter(self) -> FiscalQuarter:
        """:returns: The next fiscal quarter"""
        fiscal_quarter = FiscalQuarter(self.fiscal_year, self.fiscal_quarter)

        return fiscal_quarter.next_fiscal_quarter

    @property
    def prev_fiscal_month(self) -> FiscalMonth:
        """:returns: The previous fiscal month"""
        fiscal_month = FiscalMonth(self.fiscal_year, self.fiscal_month)

        return fiscal_month.prev_fiscal_month

    @property
    def next_fiscal_month(self) -> FiscalMonth:
        """:returns: The next fiscal month"""
        fiscal_month = FiscalMonth(self.fiscal_year, self.fiscal_month)

        return fiscal_month.next_fiscal_month

    @property
    def prev_fiscal_day(self) -> FiscalDay:
        """:returns: The previous fiscal day"""
        fiscal_day = FiscalDay(self.fiscal_year, self.fiscal_day)

        return fiscal_day.prev_fiscal_day

    @property
    def next_fiscal_day(self) -> FiscalDay:
        """:returns: The next fiscal day"""
        fiscal_day = FiscalDay(self.fiscal_year, self.fiscal_day)

        return fiscal_day.next_fiscal_day


class FiscalDate(datetime.date, _FiscalMixin):
    """A wrapper around the builtin datetime.date class
    that provides the following attributes."""

    pass


class FiscalDateTime(datetime.datetime, _FiscalMixin):
    """A wrapper around the builtin datetime.datetime class
    that provides the following attributes."""

    pass
