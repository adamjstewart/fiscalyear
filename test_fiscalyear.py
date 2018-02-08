from __future__ import with_statement

import datetime
import fiscalyear
import pytest


# Fiscal calendars to test
US_FEDERAL = ('previous', 10, 1)
UK_PERSONAL = ('same', 4, 6)

# Default to U.S.
fiscalyear.START_YEAR, fiscalyear.START_MONTH, fiscalyear.START_DAY = US_FEDERAL


class TestCheckInt(object):
    @pytest.mark.parametrize("value, exception", [
        ('asdf', TypeError),
        ("-999", TypeError),                # Shouldn't this be valid?
        (float(), TypeError),
        (object(), TypeError),
    ])
    def test_invalid_input(self, value, exception):
        with pytest.raises(exception):
            fiscalyear._check_int(value)

    @pytest.mark.parametrize("value", [1, 2, 0, -1, -2, "1", "0", "999"])
    def test_valid_input(self, value):
        assert int(value) == fiscalyear._check_int(value)


class TestCheckYear(object):
    @pytest.mark.parametrize("value, exception", [
        ('asdf', TypeError),
        (float(), TypeError),
        (object(), TypeError),
        ("-1", TypeError),
        (-1, ValueError),
        (0, ValueError),
        ("0", ValueError),
        (10000, ValueError),
        ("10000", ValueError),
    ])
    def test_invalid_input(self, value, exception):
        with pytest.raises(exception):
            fiscalyear._check_year(value)

    @pytest.mark.parametrize("value", [1, 2, "1", "999"])
    def test_valid_input(self, value):
        assert int(value) == fiscalyear._check_year(value)


class TestCheckDay(object):
    @pytest.mark.parametrize("month, day, exception", [
        (1, 'asdf', TypeError),
        (1, "-999", TypeError),                # Shouldn't this be valid?
        (1, float(), TypeError),
        (1, object(), TypeError),
        (1, -1, ValueError),
        (1, "-1", TypeError),
        (1, 0, ValueError),
        (1, "0", ValueError),
        (1, 32, ValueError),
        (1, 32, ValueError),
    ])
    def test_invalid_input(self, month, day, exception):
        with pytest.raises(exception):
            fiscalyear._check_day(month, day)

    @pytest.mark.parametrize("month, day", [(1, 1), (1, 2), (1, "1"), (1, 31), (1, "31")])
    def test_valid_input(self, month, day):
        assert int(day) == fiscalyear._check_day(month, day)


class TestCheckQuarter(object):
    @pytest.mark.parametrize("value, exception", [
        ('asdf', TypeError),
        (float(), TypeError),
        (object(), TypeError),
        ("-1", TypeError),
        (-1, ValueError),
        (0, ValueError),
        ("0", ValueError),
        (5, ValueError),
        ("5", ValueError),
    ])
    def test_invalid_input(self, value, exception):
        with pytest.raises(exception):
            fiscalyear._check_quarter(value)

    @pytest.mark.parametrize("value", [1, 2, "1", "4"])
    def test_valid_input(self, value):
        assert int(value) == fiscalyear._check_quarter(value)
class TestFiscalCalendar:

    def test_start_year(self):
        assert fiscalyear.START_YEAR == 'previous'

        with fiscalyear.fiscal_calendar(start_year='same'):
            assert fiscalyear.START_YEAR == 'same'

        assert fiscalyear.START_YEAR == 'previous'

    def test_start_month(self):
        assert fiscalyear.START_MONTH == 10

        with fiscalyear.fiscal_calendar(start_month=4):
            assert fiscalyear.START_MONTH == 4

        assert fiscalyear.START_MONTH == 10

    def test_start_day(self):
        assert fiscalyear.START_DAY == 1

        with fiscalyear.fiscal_calendar(start_day=6):
            assert fiscalyear.START_DAY == 6

        assert fiscalyear.START_DAY == 1

    def test_complex(self):
        assert fiscalyear.START_YEAR == 'previous'
        assert fiscalyear.START_MONTH == 10
        assert fiscalyear.START_DAY == 1

        with fiscalyear.fiscal_calendar('same', 4, 6):
            assert fiscalyear.START_YEAR == 'same'
            assert fiscalyear.START_MONTH == 4
            assert fiscalyear.START_DAY == 6

        assert fiscalyear.START_YEAR == 'previous'
        assert fiscalyear.START_MONTH == 10
        assert fiscalyear.START_DAY == 1

    def test_nested(self):
        assert fiscalyear.START_YEAR == 'previous'
        assert fiscalyear.START_MONTH == 10
        assert fiscalyear.START_DAY == 1

        with fiscalyear.fiscal_calendar(start_year='same'):
            assert fiscalyear.START_YEAR == 'same'
            assert fiscalyear.START_MONTH == 10
            assert fiscalyear.START_DAY == 1

            with fiscalyear.fiscal_calendar(start_month=4):
                assert fiscalyear.START_YEAR == 'same'
                assert fiscalyear.START_MONTH == 4
                assert fiscalyear.START_DAY == 1

                with fiscalyear.fiscal_calendar(start_day=6):
                    assert fiscalyear.START_YEAR == 'same'
                    assert fiscalyear.START_MONTH == 4
                    assert fiscalyear.START_DAY == 6

                assert fiscalyear.START_YEAR == 'same'
                assert fiscalyear.START_MONTH == 4
                assert fiscalyear.START_DAY == 1

            assert fiscalyear.START_YEAR == 'same'
            assert fiscalyear.START_MONTH == 10
            assert fiscalyear.START_DAY == 1

        assert fiscalyear.START_YEAR == 'previous'
        assert fiscalyear.START_MONTH == 10
        assert fiscalyear.START_DAY == 1

    def test_wrong_type(self):
        with pytest.raises(TypeError):
            with fiscalyear.fiscal_calendar(start_month=6.5):
                pass

        with pytest.raises(TypeError):
            with fiscalyear.fiscal_calendar(start_day='hello world'):
                pass

    def test_out_of_range(self):
        with pytest.raises(ValueError):
            with fiscalyear.fiscal_calendar(start_month=0):
                pass

        with pytest.raises(ValueError):
            with fiscalyear.fiscal_calendar(start_month=2, start_day=29):
                pass


class TestFiscalYear:

    @pytest.fixture(scope='class')
    def a(self):
        return fiscalyear.FiscalYear(2016)

    @pytest.fixture(scope='class')
    def b(self):
        return fiscalyear.FiscalYear(2017)

    @pytest.fixture(scope='class')
    def c(self):
        return fiscalyear.FiscalYear('2017')

    @pytest.fixture(scope='class')
    def d(self):
        return fiscalyear.FiscalQuarter(2017, 2)

    def test_basic(self, a):
        assert a.fiscal_year == 2016

    def test_repr(self, a):
        assert repr(a) == 'FiscalYear(2016)'

    def test_str(self, a):
        assert str(a) == 'FY2016'

    def test_from_string(self, c):
        assert c.fiscal_year == 2017

    def test_wrong_type(self):
        with pytest.raises(TypeError):
            fiscalyear.FiscalYear(2017.5)

        with pytest.raises(TypeError):
            fiscalyear.FiscalYear('hello world')

    def test_out_of_range(self):
        with pytest.raises(ValueError):
            fiscalyear.FiscalYear(0)

        with pytest.raises(ValueError):
            fiscalyear.FiscalYear(-2017)

    def test_prev_fiscal_year(self, a, b):
        assert a == b.prev_fiscal_year

    def test_next_fiscal_year(self, a, b):
        assert a.next_fiscal_year == b

    def test_start(self, a):
        assert a.start == a.q1.start

        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.start == datetime.datetime(2015, 10, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.start == datetime.datetime(2016, 4, 6, 0, 0, 0)

    def test_end(self, a):
        assert a.end == a.q4.end

        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.end == datetime.datetime(2016, 9, 30, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.end == datetime.datetime(2017, 4, 5, 23, 59, 59)

    def test_q1(self, a):
        assert a.q1 == fiscalyear.FiscalQuarter(2016, 1)

    def test_q2(self, a):
        assert a.q2 == fiscalyear.FiscalQuarter(2016, 2)

    def test_q3(self, a):
        assert a.q3 == fiscalyear.FiscalQuarter(2016, 3)

    def test_q4(self, a):
        assert a.q4 == fiscalyear.FiscalQuarter(2016, 4)

    def test_contains(self, a, b, c, d):
        assert b in c
        assert d not in a
        assert d in b

        assert fiscalyear.FiscalDateTime(2016, 1, 1, 0, 0, 0) in a
        assert datetime.datetime(2016, 1, 1, 0, 0, 0) in a
        assert fiscalyear.FiscalDate(2016, 1, 1) in a
        assert datetime.date(2016, 1, 1) in a

        with pytest.raises(TypeError):
            'hello world' in a

    def test_less_than(self, a, b):
        assert a < b

        with pytest.raises(TypeError):
            a < 1

    def test_less_than_equals(self, a, b, c):
        assert a <= b <= c

        with pytest.raises(TypeError):
            a <= 1

    def test_equals(self, b, c):
        assert b == c

        with pytest.raises(TypeError):
            b == 1

    def test_not_equals(self, a, b):
        assert a != b

        with pytest.raises(TypeError):
            a != 1

    def test_greater_than(self, a, b):
        assert b > a

        with pytest.raises(TypeError):
            a > 1

    def test_greater_than_equals(self, a, b, c):
        assert c >= b >= a

        with pytest.raises(TypeError):
            a >= 1


class TestFiscalQuarter:

    @pytest.fixture(scope='class')
    def a(self):
        return fiscalyear.FiscalQuarter(2016, 4)

    @pytest.fixture(scope='class')
    def b(self):
        return fiscalyear.FiscalQuarter(2017, 1)

    @pytest.fixture(scope='class')
    def c(self):
        return fiscalyear.FiscalQuarter(2017, 2)

    @pytest.fixture(scope='class')
    def d(self):
        return fiscalyear.FiscalQuarter(2017, 3)

    @pytest.fixture(scope='class')
    def e(self):
        return fiscalyear.FiscalQuarter(2017, 4)

    @pytest.fixture(scope='class')
    def f(self):
        return fiscalyear.FiscalQuarter(2018, 1)

    @pytest.fixture(scope='class')
    def g(self):
        return fiscalyear.FiscalQuarter('2018', '1')

    def test_basic(self, a):
        assert a.fiscal_year == 2016
        assert a.quarter == 4

    def test_repr(self, a):
        assert repr(a) == 'FiscalQuarter(2016, 4)'

    def test_str(self, a):
        assert str(a) == 'FY2016 Q4'

    def test_from_string(self, g):
        assert g.fiscal_year == 2018
        assert g.quarter == 1

    def test_wrong_type(self):
        with pytest.raises(TypeError):
            fiscalyear.FiscalQuarter(2017.5, 1.2)

        with pytest.raises(TypeError):
            fiscalyear.FiscalQuarter('hello', 'world')

    def test_out_of_range(self):
        with pytest.raises(ValueError):
            fiscalyear.FiscalQuarter(2017, 0)

        with pytest.raises(ValueError):
            fiscalyear.FiscalQuarter(2017, 5)

        with pytest.raises(ValueError):
            fiscalyear.FiscalQuarter(0, 2)

    def test_prev_quarter(self, a, b, c, d, e, f):
        assert a == b.prev_quarter
        assert b == c.prev_quarter
        assert c == d.prev_quarter
        assert d == e.prev_quarter
        assert e == f.prev_quarter

    def test_next_quarter(self, a, b, c, d, e, f):
        assert a.next_quarter == b
        assert b.next_quarter == c
        assert c.next_quarter == d
        assert d.next_quarter == e
        assert e.next_quarter == f

    def test_start(self, a):
        with fiscalyear.fiscal_calendar(start_month=3):
            assert a.start == datetime.datetime(2015, 12, 1, 0, 0)

    def test_end(self, a):
        with fiscalyear.fiscal_calendar(start_month=1, start_year='same'):
            assert a.end == datetime.datetime(2016, 12, 31, 23, 59, 59)

    def test_bad_start_year(self, a):
        backup_start_year = fiscalyear.START_YEAR
        fiscalyear.START_YEAR = 'hello world'

        with pytest.raises(ValueError):
            a.start

        fiscalyear.START_YEAR = backup_start_year

    def test_q1_start(self, b):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert b.start == datetime.datetime(2016, 10, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert b.start == datetime.datetime(2017, 4, 6, 0, 0, 0)

    def test_q1_end(self, b):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert b.end == datetime.datetime(2016, 12, 31, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert b.end == datetime.datetime(2017, 7, 5, 23, 59, 59)

    def test_q2_start(self, c):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert c.start == datetime.datetime(2017, 1, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert c.start == datetime.datetime(2017, 7, 6, 0, 0, 0)

    def test_q2_end(self, c):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert c.end == datetime.datetime(2017, 3, 31, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert c.end == datetime.datetime(2017, 10, 5, 23, 59, 59)

    def test_q3_start(self, d):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert d.start == datetime.datetime(2017, 4, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert d.start == datetime.datetime(2017, 10, 6, 0, 0, 0)

    def test_q3_end(self, d):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert d.end == datetime.datetime(2017, 6, 30, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert d.end == datetime.datetime(2018, 1, 5, 23, 59, 59)

    def test_q4_start(self, e):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert e.start == datetime.datetime(2017, 7, 1, 0, 0, 0)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert e.start == datetime.datetime(2018, 1, 6, 0, 0, 0)

    def test_q4_end(self, e):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert e.end == datetime.datetime(2017, 9, 30, 23, 59, 59)

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert e.end == datetime.datetime(2018, 4, 5, 23, 59, 59)

    def test_contains(self, a, f, g):
        assert a not in f
        assert f in g

        assert fiscalyear.FiscalDateTime(2016, 8, 1, 0, 0, 0) in a
        assert datetime.datetime(2016, 8, 1, 0, 0, 0) in a
        assert fiscalyear.FiscalDate(2016, 8, 1) in a
        assert datetime.date(2016, 8, 1) in a

        with pytest.raises(TypeError):
            fiscalyear.FiscalYear(2016) in a

    def test_less_than(self, a, b, c, d, e, f):
        assert a < b < c < d < e < f

        with pytest.raises(TypeError):
            a < 1

    def test_less_than_equals(self, a, b, c, d, e, f, g):
        assert a <= b <= c <= d <= e <= f <= g

        with pytest.raises(TypeError):
            a <= 1

    def test_equals(self, f, g):
        assert f == g

        with pytest.raises(TypeError):
            f == 1

    def test_not_equals(self, b, c, g):
        # Same year, different quarter
        assert b != c

        # Same quarter, different year
        assert b != g

        with pytest.raises(TypeError):
            b != 1

    def test_greater_than(self, a, b, c, d, e, f):
        assert f > e > d > c > b > a

        with pytest.raises(TypeError):
            a > 1

    def test_greater_than_equals(self, a, b, c, d, e, f, g):
        assert g >= f >= e >= d >= c >= b >= a

        with pytest.raises(TypeError):
            a >= 1

class TestFiscalDate:

    @pytest.fixture(scope='class')
    def a(self):
        return fiscalyear.FiscalDate(2017, 1, 1)

    @pytest.fixture(scope='class')
    def b(self):
        return fiscalyear.FiscalDate(2017, 8, 31)

    @pytest.fixture(scope='class')
    def c(self):
        return fiscalyear.FiscalDate(2017, 11, 15)

    def test_basic(self, a):
        assert a.year == 2017
        assert a.month == 1
        assert a.day == 1

        assert a.fiscal_year == 2017
        assert a.quarter == 2

    def test_fiscal_year(self, a, c):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.fiscal_year == 2017
            assert c.fiscal_year == 2018

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.fiscal_year == 2016
            assert c.fiscal_year == 2017

    def test_prev_fiscal_year(self, a):
        assert a.prev_fiscal_year == fiscalyear.FiscalYear(2016)

    def test_next_fiscal_year(self, a):
        assert a.next_fiscal_year == fiscalyear.FiscalYear(2018)

    def test_prev_quarter(self, a, c):
        assert a.prev_quarter == fiscalyear.FiscalQuarter(2017, 1)
        assert c.prev_quarter == fiscalyear.FiscalQuarter(2017, 4)

    def test_next_quarter(self, a, c):
        assert a.next_quarter == fiscalyear.FiscalQuarter(2017, 3)
        assert c.next_quarter == fiscalyear.FiscalQuarter(2018, 2)


class TestFiscalDateTime:

    @pytest.fixture(scope='class')
    def a(self):
        return fiscalyear.FiscalDateTime(2017, 1, 1, 0, 0, 0)

    @pytest.fixture(scope='class')
    def b(self):
        return fiscalyear.FiscalDateTime(2017, 8, 31, 23, 59, 59)

    @pytest.fixture(scope='class')
    def c(self):
        return fiscalyear.FiscalDateTime(2017, 11, 15, 12, 4, 30)

    def test_basic(self, a):
        assert a.year == 2017
        assert a.month == 1
        assert a.day == 1
        assert a.hour == 0
        assert a.minute == 0
        assert a.second == 0

        assert a.fiscal_year == 2017
        assert a.quarter == 2

    def test_fiscal_year(self, a, c):
        with fiscalyear.fiscal_calendar(*US_FEDERAL):
            assert a.fiscal_year == 2017
            assert c.fiscal_year == 2018

        with fiscalyear.fiscal_calendar(*UK_PERSONAL):
            assert a.fiscal_year == 2016
            assert c.fiscal_year == 2017

    def test_prev_fiscal_year(self, a):
        assert a.prev_fiscal_year == fiscalyear.FiscalYear(2016)

    def test_next_fiscal_year(self, a):
        assert a.next_fiscal_year == fiscalyear.FiscalYear(2018)

    def test_prev_quarter(self, a, c):
        assert a.prev_quarter == fiscalyear.FiscalQuarter(2017, 1)
        assert c.prev_quarter == fiscalyear.FiscalQuarter(2017, 4)

    def test_next_quarter(self, a, c):
        assert a.next_quarter == fiscalyear.FiscalQuarter(2017, 3)
        assert c.next_quarter == fiscalyear.FiscalQuarter(2018, 2)
