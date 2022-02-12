import datetime

import pytest
from _pytest.monkeypatch import MonkeyPatch

import fiscalyear
from fiscalyear import (
    FiscalDate,
    FiscalDateTime,
    FiscalDay,
    FiscalMonth,
    FiscalQuarter,
    FiscalYear,
)

# Fiscal calendars to test
US_FEDERAL = ("previous", 10, 1)
UK_PERSONAL = ("same", 4, 6)


class TestCheckYear:
    @pytest.mark.parametrize("value", [-1, 0, 10000])
    def test_invalid_input(self, value: int) -> None:
        with pytest.raises(ValueError):
            fiscalyear._check_year(value)

    @pytest.mark.parametrize("value", [1, 2])
    def test_valid_input(self, value: int) -> None:
        assert int(value) == fiscalyear._check_year(value)


class TestCheckDay:
    @pytest.mark.parametrize("month, day", [(1, -1), (1, 0), (1, 32), (1, 32)])
    def test_invalid_input(self, month: int, day: int) -> None:
        with pytest.raises(ValueError):
            fiscalyear._check_day(month, day)

    @pytest.mark.parametrize("month, day", [(1, 1), (1, 2), (1, 31)])
    def test_valid_input(self, month: int, day: int) -> None:
        assert int(day) == fiscalyear._check_day(month, day)


class TestCheckQuarter:
    @pytest.mark.parametrize("value", [-1, 0, 5])
    def test_invalid_input(self, value: int) -> None:
        with pytest.raises(ValueError):
            fiscalyear._check_quarter(value)

    @pytest.mark.parametrize("value", [1, 2])
    def test_valid_input(self, value: int) -> None:
        assert int(value) == fiscalyear._check_quarter(value)


class TestValidateFiscalCalendarParams:
    @pytest.mark.parametrize(
        "start_year, start_month, start_day",
        [
            ("asdf", 12, 1),
            ("same", -1, 1),
            ("same", 0, 1),
            ("same", 13, 1),
            ("same", 12, 0),
            ("same", 12, -1),
            ("same", 12, 32),
        ],
    )
    def test_invalid_input(
        self, start_year: str, start_month: int, start_day: int
    ) -> None:
        with pytest.raises(ValueError):
            fiscalyear._validate_fiscal_calendar_params(
                start_year, start_month, start_day
            )

    @pytest.mark.parametrize(
        "start_year, start_month, start_day",
        [
            ("same", 1, 1),
            ("same", 1, 31),
            ("same", 12, 1),
            ("previous", 1, 1),
            ("previous", 1, 31),
            ("previous", 12, 1),
        ],
    )
    def test_valid_input(
        self, start_year: str, start_month: int, start_day: int
    ) -> None:
        fiscalyear._validate_fiscal_calendar_params(start_year, start_month, start_day)


class TestSetupFiscalCalendar:
    def test_start_year(self) -> None:
        assert fiscalyear.START_YEAR == "previous"

        fiscalyear.setup_fiscal_calendar(start_year="same")
        assert fiscalyear.START_YEAR == "same"
        fiscalyear.setup_fiscal_calendar(start_year="previous")

        assert fiscalyear.START_YEAR == "previous"

    def test_start_month(self) -> None:
        assert fiscalyear.START_MONTH == 10

        fiscalyear.setup_fiscal_calendar(start_month=4)
        assert fiscalyear.START_MONTH == 4
        fiscalyear.setup_fiscal_calendar(start_month=10)

        assert fiscalyear.START_MONTH == 10

    def test_start_day(self) -> None:
        assert fiscalyear.START_DAY == 1

        fiscalyear.setup_fiscal_calendar(start_day=6)
        assert fiscalyear.START_DAY == 6
        fiscalyear.setup_fiscal_calendar(start_day=1)

        assert fiscalyear.START_DAY == 1

    def test_complex(self) -> None:
        # Test defaults
        day = FiscalDate(2017, 12, 1)
        assert day.fiscal_year == 2018
        assert day.fiscal_quarter == 1

        # Change fiscal year settings
        fiscalyear.setup_fiscal_calendar("same", 1, 1)
        assert day.fiscal_year == 2017
        assert day.fiscal_quarter == 4

        # Restore defaults and re-test
        fiscalyear.setup_fiscal_calendar("previous", 10, 1)
        assert day.fiscal_year == 2018
        assert day.fiscal_quarter == 1


class TestFiscalCalendar:
    def test_start_year(self) -> None:
        assert fiscalyear.START_YEAR == "previous"

        with fiscalyear.fiscal_calendar(start_year="same"):
            assert fiscalyear.START_YEAR == "same"

        assert fiscalyear.START_YEAR == "previous"

    def test_start_month(self) -> None:
        assert fiscalyear.START_MONTH == 10

        with fiscalyear.fiscal_calendar(start_month=4):
            assert fiscalyear.START_MONTH == 4

        assert fiscalyear.START_MONTH == 10

    def test_start_day(self) -> None:
        assert fiscalyear.START_DAY == 1

        with fiscalyear.fiscal_calendar(start_day=6):
            assert fiscalyear.START_DAY == 6

        assert fiscalyear.START_DAY == 1

    def test_complex(self) -> None:
        assert fiscalyear.START_YEAR == "previous"
        assert fiscalyear.START_MONTH == 10
        assert fiscalyear.START_DAY == 1

        with fiscalyear.fiscal_calendar("same", 4, 6):
            assert fiscalyear.START_YEAR == "same"
            assert fiscalyear.START_MONTH == 4
            assert fiscalyear.START_DAY == 6

        assert fiscalyear.START_YEAR == "previous"
        assert fiscalyear.START_MONTH == 10
        assert fiscalyear.START_DAY == 1

    def test_nested(self) -> None:
        assert fiscalyear.START_YEAR == "previous"
        assert fiscalyear.START_MONTH == 10
        assert fiscalyear.START_DAY == 1

        with fiscalyear.fiscal_calendar(start_year="same"):
            assert fiscalyear.START_YEAR == "same"
            assert fiscalyear.START_MONTH == 10
            assert fiscalyear.START_DAY == 1

            with fiscalyear.fiscal_calendar(start_month=4):
                assert fiscalyear.START_YEAR == "same"
                assert fiscalyear.START_MONTH == 4
                assert fiscalyear.START_DAY == 1

                with fiscalyear.fiscal_calendar(start_day=6):
                    assert fiscalyear.START_YEAR == "same"
                    assert fiscalyear.START_MONTH == 4
                    assert fiscalyear.START_DAY == 6

                assert fiscalyear.START_YEAR == "same"
                assert fiscalyear.START_MONTH == 4
                assert fiscalyear.START_DAY == 1

            assert fiscalyear.START_YEAR == "same"
            assert fiscalyear.START_MONTH == 10
            assert fiscalyear.START_DAY == 1

        assert fiscalyear.START_YEAR == "previous"
        assert fiscalyear.START_MONTH == 10
        assert fiscalyear.START_DAY == 1

    def test_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            with fiscalyear.fiscal_calendar(start_month=0):
                pass

        with pytest.raises(ValueError):
            with fiscalyear.fiscal_calendar(start_month=2, start_day=29):
                pass

    def test_corner_cases(self) -> None:
        # start_day does not exist in all months
        with fiscalyear.fiscal_calendar(start_month=5, start_day=31):
            # Non-leap year
            assert FiscalQuarter(2019, 1).start.day == 31
            assert FiscalQuarter(2019, 1).end.day == 30

            assert FiscalQuarter(2019, 2).start.day == 31
            assert FiscalQuarter(2019, 2).end.day == 29

            assert FiscalQuarter(2019, 3).start.day == 30
            assert FiscalQuarter(2019, 3).end.day == 27

            assert FiscalQuarter(2019, 4).start.day == 28
            assert FiscalQuarter(2019, 4).end.day == 30

            # Leap year
            assert FiscalQuarter(2020, 1).start.day == 31
            assert FiscalQuarter(2020, 1).end.day == 30

            assert FiscalQuarter(2020, 2).start.day == 31
            assert FiscalQuarter(2020, 2).end.day == 29

            assert FiscalQuarter(2020, 3).start.day == 30
            assert FiscalQuarter(2020, 3).end.day == 28

            assert FiscalQuarter(2020, 4).start.day == 29
            assert FiscalQuarter(2020, 4).end.day == 30


class TestFiscalYear:
    @pytest.fixture(scope="class")
    def a(self) -> FiscalYear:
        return FiscalYear(2016)

    @pytest.fixture(scope="class")
    def b(self) -> FiscalYear:
        return FiscalYear(2017)

    @pytest.fixture(scope="class")
    def c(self) -> FiscalQuarter:
        return FiscalQuarter(2017, 2)

    @pytest.fixture(scope="class")
    def d(self) -> FiscalMonth:
        return FiscalMonth(2017, 1)

    @pytest.fixture(scope="class")
    def e(self) -> FiscalYear:
        return FiscalYear(2015)

    def test_basic(self, a: FiscalYear) -> None:
        assert a.fiscal_year == 2016

    def test_current(self, monkeypatch: MonkeyPatch) -> None:
        def today() -> FiscalDate:
            return FiscalDate(2016, 10, 1)

        monkeypatch.setattr(FiscalDate, "today", today)
        current = FiscalYear.current()
        assert current == FiscalYear(2017)

    def test_repr(self, a: FiscalYear) -> None:
        assert repr(a) == "FiscalYear(2016)"

    def test_str(self, a: FiscalYear) -> None:
        assert str(a) == "FY2016"

    def test_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            FiscalYear(0)

        with pytest.raises(ValueError):
            FiscalYear(-2017)

    def test_prev_fiscal_year(self, a: FiscalYear, b: FiscalYear) -> None:
        assert a == b.prev_fiscal_year

    def test_next_fiscal_year(self, a: FiscalYear, b: FiscalYear) -> None:
        assert a.next_fiscal_year == b

    def test_start(self, a: FiscalYear) -> None:
        assert a.start == a.q1.start

        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.start == datetime.datetime(2015, 10, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.start == datetime.datetime(2016, 4, 6, 0, 0, 0)

    def test_end(self, a: FiscalYear) -> None:
        assert a.end == a.q4.end

        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.end == datetime.datetime(2016, 9, 30, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.end == datetime.datetime(2017, 4, 5, 23, 59, 59)

    def test_q1(self, a: FiscalYear) -> None:
        assert a.q1 == FiscalQuarter(2016, 1)

    def test_q2(self, a: FiscalYear) -> None:
        assert a.q2 == FiscalQuarter(2016, 2)

    def test_q3(self, a: FiscalYear) -> None:
        assert a.q3 == FiscalQuarter(2016, 3)

    def test_q4(self, a: FiscalYear) -> None:
        assert a.q4 == FiscalQuarter(2016, 4)

    def test_is_leap(self, a: FiscalYear, b: FiscalYear, e: FiscalYear) -> None:
        # default US start_year='previous', start_month=10
        assert isinstance(a.isleap, bool)
        assert isinstance(e.isleap, bool)

        with fiscalyear.fiscal_calendar(start_year="previous", start_month=1):
            assert not a.isleap
            assert b.isleap

        with fiscalyear.fiscal_calendar(start_year="same", start_month=3):
            assert not a.isleap
            assert e.isleap

        with fiscalyear.fiscal_calendar(start_year="same", start_month=1):
            assert a.isleap
            assert not e.isleap

    def test_contains(
        self, a: FiscalYear, b: FiscalYear, c: FiscalYear, d: FiscalYear
    ) -> None:
        assert b in b
        assert c not in a
        assert c in b
        assert d in b

        assert FiscalDateTime(2016, 1, 1, 0, 0, 0) in a
        assert datetime.datetime(2016, 1, 1, 0, 0, 0) in a
        assert FiscalDate(2016, 1, 1) in a
        assert datetime.date(2016, 1, 1) in a

    def test_less_than(self, a: FiscalYear, b: FiscalYear) -> None:
        assert a < b

    def test_less_than_equals(self, a: FiscalYear, b: FiscalYear) -> None:
        assert a <= b <= b

    def test_equals(self, b: FiscalYear) -> None:
        assert b == b

        with pytest.raises(TypeError):
            b == 1

    def test_not_equals(self, a: FiscalYear, b: FiscalYear) -> None:
        assert a != b

        with pytest.raises(TypeError):
            a != 1

    def test_greater_than(self, a: FiscalYear, b: FiscalYear) -> None:
        assert b > a

    def test_greater_than_equals(self, a: FiscalYear, b: FiscalYear) -> None:
        assert b >= b >= a

    def test_hash(self, a: FiscalYear, b: FiscalYear, e: FiscalYear) -> None:
        assert hash(a) == hash(a)
        assert hash(a) != hash(b) != hash(e)


class TestFiscalQuarter:
    @pytest.fixture(scope="class")
    def a(self) -> FiscalQuarter:
        return FiscalQuarter(2016, 4)

    @pytest.fixture(scope="class")
    def b(self) -> FiscalQuarter:
        return FiscalQuarter(2017, 1)

    @pytest.fixture(scope="class")
    def c(self) -> FiscalQuarter:
        return FiscalQuarter(2017, 2)

    @pytest.fixture(scope="class")
    def d(self) -> FiscalQuarter:
        return FiscalQuarter(2017, 3)

    @pytest.fixture(scope="class")
    def e(self) -> FiscalQuarter:
        return FiscalQuarter(2017, 4)

    @pytest.fixture(scope="class")
    def f(self) -> FiscalQuarter:
        return FiscalQuarter(2018, 1)

    def test_basic(self, a: FiscalQuarter) -> None:
        assert a.fiscal_year == 2016
        assert a.fiscal_quarter == 4

    def test_current(self, monkeypatch: MonkeyPatch) -> None:
        def today() -> FiscalDate:
            return FiscalDate(2016, 10, 1)

        monkeypatch.setattr(FiscalDate, "today", today)
        current = FiscalQuarter.current()
        assert current == FiscalQuarter(2017, 1)

    def test_repr(self, a: FiscalQuarter) -> None:
        assert repr(a) == "FiscalQuarter(2016, 4)"

    def test_str(self, a: FiscalQuarter) -> None:
        assert str(a) == "FY2016 Q4"

    def test_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            FiscalQuarter(2017, 0)

        with pytest.raises(ValueError):
            FiscalQuarter(2017, 5)

        with pytest.raises(ValueError):
            FiscalQuarter(0, 2)

    def test_deprecated(self, a: FiscalQuarter) -> None:
        with pytest.deprecated_call():
            a.quarter
            a.prev_quarter
            a.next_quarter

    def test_prev_fiscal_quarter(
        self,
        a: FiscalQuarter,
        b: FiscalQuarter,
        c: FiscalQuarter,
        d: FiscalQuarter,
        e: FiscalQuarter,
        f: FiscalQuarter,
    ) -> None:
        assert a == b.prev_fiscal_quarter
        assert b == c.prev_fiscal_quarter
        assert c == d.prev_fiscal_quarter
        assert d == e.prev_fiscal_quarter
        assert e == f.prev_fiscal_quarter

    def test_next_fiscal_quarter(
        self,
        a: FiscalQuarter,
        b: FiscalQuarter,
        c: FiscalQuarter,
        d: FiscalQuarter,
        e: FiscalQuarter,
        f: FiscalQuarter,
    ) -> None:
        assert a.next_fiscal_quarter == b
        assert b.next_fiscal_quarter == c
        assert c.next_fiscal_quarter == d
        assert d.next_fiscal_quarter == e
        assert e.next_fiscal_quarter == f

    def test_start(self, a: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(start_month=3):
            assert a.start == datetime.datetime(2015, 12, 1, 0, 0)

    def test_end(self, a: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(start_month=1, start_year="same"):
            assert a.end == datetime.datetime(2016, 12, 31, 23, 59, 59)

    def test_bad_start_year(self, a: FiscalQuarter) -> None:
        backup_start_year = fiscalyear.START_YEAR
        fiscalyear.START_YEAR = "hello world"

        with pytest.raises(ValueError):
            a.start

        fiscalyear.START_YEAR = backup_start_year

    def test_q1_start(self, b: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert b.start == datetime.datetime(2016, 10, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert b.start == datetime.datetime(2017, 4, 6, 0, 0, 0)

    def test_q1_end(self, b: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert b.end == datetime.datetime(2016, 12, 31, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert b.end == datetime.datetime(2017, 7, 5, 23, 59, 59)

    def test_q2_start(self, c: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert c.start == datetime.datetime(2017, 1, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert c.start == datetime.datetime(2017, 7, 6, 0, 0, 0)

    def test_q2_end(self, c: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert c.end == datetime.datetime(2017, 3, 31, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert c.end == datetime.datetime(2017, 10, 5, 23, 59, 59)

    def test_q3_start(self, d: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert d.start == datetime.datetime(2017, 4, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert d.start == datetime.datetime(2017, 10, 6, 0, 0, 0)

    def test_q3_end(self, d: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert d.end == datetime.datetime(2017, 6, 30, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert d.end == datetime.datetime(2018, 1, 5, 23, 59, 59)

    def test_q4_start(self, e: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert e.start == datetime.datetime(2017, 7, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert e.start == datetime.datetime(2018, 1, 6, 0, 0, 0)

    def test_q4_end(self, e: FiscalQuarter) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert e.end == datetime.datetime(2017, 9, 30, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert e.end == datetime.datetime(2018, 4, 5, 23, 59, 59)

    def test_contains(self, a: FiscalQuarter, f: FiscalQuarter) -> None:
        assert a not in f
        assert f in f

        assert FiscalDateTime(2016, 8, 1, 0, 0, 0) in a
        assert datetime.datetime(2016, 8, 1, 0, 0, 0) in a
        assert FiscalDate(2016, 8, 1) in a
        assert datetime.date(2016, 8, 1) in a

    def test_less_than(
        self,
        a: FiscalQuarter,
        b: FiscalQuarter,
        c: FiscalQuarter,
        d: FiscalQuarter,
        e: FiscalQuarter,
        f: FiscalQuarter,
    ) -> None:
        assert a < b < c < d < e < f

    def test_less_than_equals(
        self,
        a: FiscalQuarter,
        b: FiscalQuarter,
        c: FiscalQuarter,
        d: FiscalQuarter,
        e: FiscalQuarter,
        f: FiscalQuarter,
    ) -> None:
        assert a <= b <= c <= d <= e <= f

    def test_equals(self, f: FiscalQuarter) -> None:
        assert f == f

        with pytest.raises(TypeError):
            f == 1

    def test_not_equals(
        self, b: FiscalQuarter, c: FiscalQuarter, f: FiscalQuarter
    ) -> None:
        # Same year, different quarter
        assert b != c

        # Same quarter, different year
        assert b != f

        with pytest.raises(TypeError):
            b != 1

    def test_greater_than(
        self,
        a: FiscalQuarter,
        b: FiscalQuarter,
        c: FiscalQuarter,
        d: FiscalQuarter,
        e: FiscalQuarter,
        f: FiscalQuarter,
    ) -> None:
        assert f > e > d > c > b > a

    def test_greater_than_equals(
        self,
        a: FiscalQuarter,
        b: FiscalQuarter,
        c: FiscalQuarter,
        d: FiscalQuarter,
        e: FiscalQuarter,
        f: FiscalQuarter,
    ) -> None:
        assert f >= e >= d >= c >= b >= a

    def test_hash(self, a: FiscalQuarter, b: FiscalQuarter, c: FiscalQuarter) -> None:
        assert hash(a) == hash(a)
        assert hash(a) != hash(b) != hash(c)


class TestFiscalMonth:
    @pytest.fixture(scope="class")
    def a(self) -> FiscalMonth:
        return FiscalMonth(2016, 1)

    @pytest.fixture(scope="class")
    def b(self) -> FiscalMonth:
        return FiscalMonth(2016, 2)

    @pytest.fixture(scope="class")
    def c(self) -> FiscalMonth:
        return FiscalMonth(2016, 12)

    @pytest.fixture(scope="class")
    def d(self) -> FiscalQuarter:
        return FiscalQuarter(2017, 1)

    def test_basic(self, a: FiscalMonth) -> None:
        assert a.fiscal_year == 2016
        assert a.fiscal_month == 1

    def test_current(self, monkeypatch: MonkeyPatch) -> None:
        def today() -> FiscalDate:
            return FiscalDate(2016, 10, 1)

        monkeypatch.setattr(FiscalDate, "today", today)
        current = FiscalMonth.current()
        assert current == FiscalMonth(2017, 1)

    def test_repr(self, a: FiscalMonth) -> None:
        assert repr(a) == "FiscalMonth(2016, 1)"

    def test_str(self, a: FiscalMonth) -> None:
        assert str(a) == "FY2016 FM1"

    def test_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            FiscalMonth(2016, 0)

        with pytest.raises(ValueError):
            FiscalMonth(2016, -12)

    def test_prev_fiscal_year(self, a: FiscalMonth, b: FiscalMonth) -> None:
        assert a == b.prev_fiscal_month
        assert a.prev_fiscal_month == FiscalMonth(2015, 12)

    def test_next_fiscal_year(self, a: FiscalMonth, b: FiscalMonth) -> None:
        assert a.next_fiscal_month == b

    def test_start(self, a: FiscalMonth, c: FiscalMonth) -> None:
        assert a.start == FiscalYear(a.fiscal_year).start
        assert c.start == FiscalDateTime(2016, 9, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.start == datetime.datetime(2015, 10, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.start == datetime.datetime(2016, 4, 6, 0, 0, 0)
            assert FiscalMonth(2016, 12).start == datetime.datetime(2017, 3, 6, 0, 0, 0)

    def test_end(self, c: FiscalMonth) -> None:
        assert c.end == FiscalYear(c.fiscal_year).end

        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert c.end == datetime.datetime(2016, 9, 30, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert c.end == datetime.datetime(2017, 4, 5, 23, 59, 59)

    def test_contains(self, a: FiscalMonth, b: FiscalMonth, d: FiscalQuarter) -> None:
        assert b in b
        assert a not in d
        assert b in b

        assert FiscalDateTime(2015, 10, 1, 0, 0, 0) in a
        assert datetime.datetime(2015, 10, 1, 0, 0, 0) in a
        assert FiscalDate(2015, 10, 1) in a
        assert datetime.date(2015, 10, 1) in a

    def test_less_than(self, a: FiscalMonth, b: FiscalMonth) -> None:
        assert a < b

    def test_less_than_equals(self, a: FiscalMonth, b: FiscalMonth) -> None:
        assert a <= b

    def test_equals(self, b: FiscalMonth) -> None:
        assert b == b

        with pytest.raises(TypeError):
            b == 1

    def test_not_equals(self, a: FiscalMonth, b: FiscalMonth) -> None:
        assert a != b

        with pytest.raises(TypeError):
            a != 1

    def test_greater_than(self, a: FiscalMonth, b: FiscalMonth) -> None:
        assert b > a

    def test_greater_than_equals(self, a: FiscalMonth, b: FiscalMonth) -> None:
        assert b >= a

    def test_hash(self, a: FiscalMonth, b: FiscalMonth, c: FiscalMonth) -> None:
        assert hash(a) == hash(a)
        assert hash(a) != hash(b) != hash(c)


class TestFiscalDay:
    @pytest.fixture(scope="class")
    def a(self) -> FiscalDay:
        return FiscalDay(2016, 1)

    @pytest.fixture(scope="class")
    def b(self) -> FiscalDay:
        return FiscalDay(2016, 2)

    @pytest.fixture(scope="class")
    def c(self) -> FiscalDay:
        return FiscalDay(2016, 366)

    @pytest.fixture(scope="class")
    def d(self) -> FiscalDay:
        return FiscalDay(2017, 1)

    def test_basic(self, a: FiscalDay) -> None:
        assert a.fiscal_year == 2016
        assert a.fiscal_day == 1

        assert a.fiscal_month == 1
        assert a.fiscal_quarter == 1

    def test_current(self, monkeypatch: MonkeyPatch) -> None:
        def today() -> FiscalDate:
            return FiscalDate(2016, 10, 1)

        monkeypatch.setattr(FiscalDate, "today", today)
        current = FiscalDay.current()
        assert current == FiscalDay(2017, 1)

    def test_repr(self, a: FiscalDay) -> None:
        assert repr(a) == "FiscalDay(2016, 1)"

    def test_str(self, a: FiscalDay) -> None:
        assert str(a) == "FY2016 FD1"

    def test_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            FiscalDay(2016, 0)

        with pytest.raises(ValueError):
            FiscalDay(2016, -364)

    def test_prev_fiscal_day(self, a: FiscalDay, b: FiscalDay, d: FiscalDay) -> None:
        assert a == b.prev_fiscal_day
        assert a.prev_fiscal_day == FiscalDay(2015, 365)
        assert d.prev_fiscal_day == FiscalDay(2016, 366)

    def test_next_fiscal_day(self, a: FiscalDay, b: FiscalDay) -> None:
        assert a.next_fiscal_day == b

    def test_start(self, a: FiscalDay, c: FiscalDay) -> None:
        assert a.start == FiscalYear(a.fiscal_year).start
        assert c.start == FiscalDateTime(2016, 9, 30, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.start == datetime.datetime(2015, 10, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.start == datetime.datetime(2016, 4, 6, 0, 0, 0)

    def test_end(self, c: FiscalDay) -> None:
        assert c.end == FiscalYear(c.fiscal_year).end

        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert c.end == datetime.datetime(2016, 9, 30, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert c.end == datetime.datetime(2017, 4, 5, 23, 59, 59)

    def test_leap_year(self) -> None:
        assert FiscalDate(2016, 1, 1).fiscal_day == 93
        assert FiscalDate(2016, 2, 29).fiscal_day == 152
        assert FiscalDate(2017, 3, 1).fiscal_day == 152
        assert FiscalDate(2016, 9, 30).fiscal_day == 366
        assert FiscalDate(2017, 9, 30).fiscal_day == 365
        assert FiscalDate(2018, 9, 30).fiscal_day == 365

    def test_contains(self, a: FiscalDay, b: FiscalDay, d: FiscalDay) -> None:
        assert b in b
        assert a not in d

        assert FiscalDateTime(2015, 10, 1, 0, 0, 0) in a
        assert datetime.datetime(2015, 10, 1, 0, 0, 0) in a
        assert FiscalDate(2015, 10, 1) in a
        assert datetime.date(2015, 10, 1) in a

        assert b in FiscalMonth(2016, 1)
        assert b in FiscalQuarter(2016, 1)
        assert b in FiscalYear(2016)

    def test_less_than(self, a: FiscalDay, b: FiscalDay) -> None:
        assert a < b

    def test_less_than_equals(self, a: FiscalDay, b: FiscalDay) -> None:
        assert a <= b

    def test_equals(self, b: FiscalDay) -> None:
        assert b == b

        with pytest.raises(TypeError):
            b == 1

    def test_not_equals(self, a: FiscalDay, b: FiscalDay) -> None:
        assert a != b

        with pytest.raises(TypeError):
            a != 1

    def test_greater_than(self, a: FiscalDay, b: FiscalDay) -> None:
        assert b > a

    def test_greater_than_equals(self, a: FiscalDay, b: FiscalDay) -> None:
        assert b >= a

    def test_hash(self, a: FiscalDay, b: FiscalDay, d: FiscalDay) -> None:
        assert hash(a) == hash(a)
        assert hash(a) != hash(b) != hash(d)


class TestFiscalDate:
    @pytest.fixture(scope="class")
    def a(self) -> FiscalDate:
        return FiscalDate(2017, 1, 1)

    @pytest.fixture(scope="class")
    def b(self) -> FiscalDate:
        return FiscalDate(2017, 11, 15)

    def test_basic(self, a: FiscalDate) -> None:
        assert a.year == 2017
        assert a.month == 1
        assert a.day == 1

        assert a.fiscal_year == 2017
        assert a.fiscal_month == 4
        assert a.fiscal_quarter == 2

    def test_fiscal_periods(self, a: FiscalDate, b: FiscalDate) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.fiscal_year == 2017
            assert a.fiscal_month == 4
            assert b.fiscal_year == 2018
            assert b.fiscal_month == 2

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.fiscal_year == 2016
            assert a.fiscal_month == 9
            assert b.fiscal_year == 2017
            assert b.fiscal_month == 8

    def test_prev_fiscal_year(self, a: FiscalDate) -> None:
        assert a.prev_fiscal_year == FiscalYear(2016)

    def test_next_fiscal_year(self, a: FiscalDate) -> None:
        assert a.next_fiscal_year == FiscalYear(2018)

    def test_prev_fiscal_quarter(self, a: FiscalDate, b: FiscalDate) -> None:
        assert a.prev_fiscal_quarter == FiscalQuarter(2017, 1)
        assert b.prev_fiscal_quarter == FiscalQuarter(2017, 4)

    def test_next_fiscal_quarter(self, a: FiscalDate, b: FiscalDate) -> None:
        assert a.next_fiscal_quarter == FiscalQuarter(2017, 3)
        assert b.next_fiscal_quarter == FiscalQuarter(2018, 2)

    def test_prev_fiscal_month(self, a: FiscalDate) -> None:
        assert a.prev_fiscal_month == FiscalMonth(2017, 3)

    def test_next_fiscal_month(self, a: FiscalDate) -> None:
        assert a.next_fiscal_month == FiscalMonth(2017, 5)

    def test_prev_fiscal_day(self, a: FiscalDate) -> None:
        assert a.prev_fiscal_day == FiscalDay(2017, 92)

    def test_next_fiscal_day(self, a: FiscalDate) -> None:
        assert a.next_fiscal_day == FiscalDay(2017, 94)

    def test_deprecated(self, a: FiscalDate) -> None:
        with pytest.deprecated_call():
            a.quarter
            a.prev_quarter
            a.next_quarter


class TestFiscalDateTime:
    @pytest.fixture(scope="class")
    def a(self) -> FiscalDateTime:
        return FiscalDateTime(2017, 1, 1, 0, 0, 0)

    @pytest.fixture(scope="class")
    def b(self) -> FiscalDateTime:
        return FiscalDateTime(2017, 11, 15, 12, 4, 30)

    def test_basic(self, a: FiscalDateTime) -> None:
        assert a.year == 2017
        assert a.month == 1
        assert a.day == 1
        assert a.hour == 0
        assert a.minute == 0
        assert a.second == 0

        assert a.fiscal_year == 2017
        assert a.fiscal_quarter == 2

    def test_fiscal_periods(self, a: FiscalDateTime, b: FiscalDateTime) -> None:
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.fiscal_year == 2017
            assert a.fiscal_month == 4
            assert b.fiscal_year == 2018
            assert b.fiscal_month == 2

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.fiscal_year == 2016
            assert a.fiscal_month == 9
            assert b.fiscal_year == 2017
            assert b.fiscal_month == 8

    def test_prev_fiscal_year(self, a: FiscalDateTime) -> None:
        assert a.prev_fiscal_year == FiscalYear(2016)

    def test_next_fiscal_year(self, a: FiscalDateTime) -> None:
        assert a.next_fiscal_year == FiscalYear(2018)

    def test_prev_fiscal_quarter(self, a: FiscalDateTime, b: FiscalDateTime) -> None:
        assert a.prev_fiscal_quarter == FiscalQuarter(2017, 1)
        assert b.prev_fiscal_quarter == FiscalQuarter(2017, 4)

    def test_next_fiscal_quarter(self, a: FiscalDateTime, b: FiscalDateTime) -> None:
        assert a.next_fiscal_quarter == FiscalQuarter(2017, 3)
        assert b.next_fiscal_quarter == FiscalQuarter(2018, 2)

    def test_prev_fiscal_month(self, a: FiscalDateTime) -> None:
        assert a.prev_fiscal_month == FiscalMonth(2017, 3)

    def test_next_fiscal_month(self, a: FiscalDateTime) -> None:
        assert a.next_fiscal_month == FiscalMonth(2017, 5)

    def test_prev_fiscal_day(self, a: FiscalDateTime) -> None:
        assert a.prev_fiscal_day == FiscalDay(2017, 92)

    def test_next_fiscal_day(self, a: FiscalDateTime) -> None:
        assert a.next_fiscal_day == FiscalDay(2017, 94)

    def test_deprecated(self, a: FiscalDateTime) -> None:
        with pytest.deprecated_call():
            a.quarter
            a.prev_quarter
            a.next_quarter
