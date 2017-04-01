"""Utilities for managing the fiscal calendar."""

from __future__ import division

import calendar
import datetime


# The first month at the start of a new fiscal year.
# By default, use the U.S. federal government's fiscal year,
# which starts on October 1st and ends on September 30th.
START_MONTH = 10

# Number of months in each quarter
MONTHS_PER_QUARTER = 12 // 4


class FiscalDate(datetime.date):
    """Wrapper around datetime.date that provides the following
    additional features:

    Attributes:
        fiscal_year: the fiscal year    [int]
        quarter:     the fiscal quarter [int: 1-4]

    Methods:
        is_q1_start: True if date is the first day of the 1st quarter
                     of the fiscal year, else False
        ...
        is_q4_start: True if date is the first day of the 4th quarter
                     of the fiscal year, else False

        is_q1_end:   True if date is the last day of the 1st quarter
                     of the fiscal year, else False
        ...
        is_q4_end:   True if date is the last day of the 4th quarter
                     of the fiscal year, else False

    The fiscal year starts on the first day of October
    and ends on the last day of September. For example, the 2018
    fiscal year starts on 10/1/2017 and ends on 9/30/2018.
    """

    @property
    def fiscal_year(self):
        """Returns the fiscal year."""

        fiscal_year = self.year
        if self.month >= START_MONTH:
            fiscal_year += 1

        return fiscal_year


    @property
    def prev_quarter_fiscal_year(self):
        """Returns the fiscal year of the previous quarter."""

        fiscal_year = self.fiscal_year
        if self.quarter == 1:
            fiscal_year -= 1

        return fiscal_year

    @property
    def next_quarter_fiscal_year(self):
        """Returns the fiscal year of the next quarter."""

        fiscal_year = self.fiscal_year
        if self.quarter == 4:
            fiscal_year += 1

        return fiscal_year

    @property
    def quarter(self):
        """Returns the quarter of the fiscal year."""

        month = self.month
        month -= START_MONTH
        if month < 0:
            month += 12
        quarter = month // MONTHS_PER_QUARTER + 1

        return quarter

    @property
    def prev_quarter(self):
        """Returns the previous quarter."""

        quarter = self.quarter - 1
        if quarter == 0:
            quarter = 4

        return quarter

    @property
    def next_quarter(self):
        """Returns the next quarter."""

        quarter = self.quarter + 1
        if quarter == 5:
            quarter = 1

        return quarter

    def is_quarter_start(self, quarter):
        start = FiscalQuarter(self.fiscal_year, quarter).start.date()

        return self == start

    def is_q1_start(self):
        return self.is_quarter_start(1)

    def is_q2_start(self):
        return self.is_quarter_start(2)

    def is_q3_start(self):
        return self.is_quarter_start(3)

    def is_q4_start(self):
        return self.is_quarter_start(4)

    def is_quarter_end(self, quarter):
        end = FiscalQuarter(self.fiscal_year, quarter).end.date()

        return self == end

    def is_q1_end(self):
        return self.is_quarter_end(1)

    def is_q2_end(self):
        return self.is_quarter_end(2)

    def is_q3_end(self):
        return self.is_quarter_end(3)

    def is_q4_end(self):
        return self.is_quarter_end(4)


class FiscalQuarter:
    def __init__(self, fiscal_year, quarter):
        assert isinstance(fiscal_year, int)
        assert isinstance(quarter, int)
        assert datetime.MINYEAR <= fiscal_year <= datetime.MAXYEAR
        assert 1 <= quarter <= 4

        self.__fiscal_year = fiscal_year
        self.__quarter = quarter

    @property
    def fiscal_year(self):
        return self.__fiscal_year

    @property
    def quarter(self):
        return self.__quarter

    @property
    def start(self):
        # Find the first month of the fiscal quarter
        month = START_MONTH
        month += (self.quarter - 1) * MONTHS_PER_QUARTER
        month %= 12
        if month == 0:
            month = 12

        # Find the calendar year of the start of the fiscal quarter
        year = self.fiscal_year
        if month >= START_MONTH:
            year -= 1

        return datetime.datetime(year, month, 1, 0, 0, 0)

    @property
    def end(self):
        # Find the last month of the fiscal quarter
        month = START_MONTH
        month += self.quarter * MONTHS_PER_QUARTER - 1
        month %= 12
        if month == 0:
            month = 12

        # Find the calendar year of the end of the fiscal quarter
        year = self.fiscal_year
        if month >= START_MONTH:
            year -= 1

        # Find the last day of the last month of the fiscal quarter
        day = calendar.monthrange(year, month)[1]

        return datetime.datetime(year, month, day, 23, 59, 59)


class FiscalYear:
    def __init__(self, fiscal_year):
        self.__fiscal_year = fiscal_year

    @property
    def fiscal_year(self):
        return self.__fiscal_year

    @property
    def start(self):
        return self.q1.start

    @property
    def end(self):
        return self.q4.end

    @property
    def q1(self):
        return FiscalQuarter(self.fiscal_year, 1)

    @property
    def q2(self):
        return FiscalQuarter(self.fiscal_year, 2)

    @property
    def q3(self):
        return FiscalQuarter(self.fiscal_year, 3)

    @property
    def q4(self):
        return FiscalQuarter(self.fiscal_year, 4)
