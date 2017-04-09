# fiscalyear
:calendar: Utilities for managing the fiscal calendar

[![Build Status](https://travis-ci.org/adamjstewart/fiscalyear.svg?branch=master)](https://travis-ci.org/adamjstewart/fiscalyear)
[![codecov](https://codecov.io/gh/adamjstewart/fiscalyear/branch/master/graph/badge.svg)](https://codecov.io/gh/adamjstewart/fiscalyear)

## Overview

[fiscalyear](https://github.com/adamjstewart/fiscalyear) is a small, lightweight Python module providing helpful utilities for managing the fiscal calendar. It is designed as an extension of the built-in [datetime](https://docs.python.org/3/library/datetime.html) and [calendar](https://docs.python.org/3/library/calendar.html) modules, adding the ability to query the fiscal year and fiscal quarter of a date or datetime object.

## Usage

fiscalyear provides several useful classes.

### FiscalYear

The `FiscalYear` class provides an object for storing information about the start and end of a particular fiscal year.

```python
>>> from fiscalyear import *
>>> a = FiscalYear(2017)
>>> a.start
FiscalDateTime(2016, 10, 1, 0, 0)
>>> a.end
FiscalDateTime(2017, 9, 30, 23, 59, 59)
```

### FiscalQuarter

The `FiscalYear` class also allows you to query information about a specific quarter.

```python
>>> a.q3.start
FiscalDateTime(2017, 4, 1, 0, 0)
>>> a.q3.end
FiscalDateTime(2017, 6, 30, 23, 59, 59)
```

These objects represent the standalone `FiscalQuarter` class.

```python
>>> b = FiscalQuarter(2017, 3)
>>> b.start
FiscalDateTime(2017, 4, 1, 0, 0)
>>> b.end
FiscalDateTime(2017, 6, 30, 23, 59, 59)
>>> a.q3 == b
True
>>> b in a
True
```

### FiscalDateTime

The start and end of each quarter are stored as instances of the `FiscalDateTime` class. This class provides all of the same features as the `datetime` class, with the addition of the ability to query the fiscal year and quarter.

```python
>>> c = FiscalDateTime.now()
>>> c
FiscalDateTime(2017, 4, 8, 20, 30, 31, 105323)
>>> c.fiscal_year
2017
>>> c.quarter
3
>>> c.next_quarter
FiscalQuarter(2017, 4)
```

### FiscalDate

If you don't care about the time component of the `FiscalDateTime` class, the `FiscalDate` class is right for you.

```python
>>> d = FiscalDate.today()
>>> d
FiscalDate(2017, 4, 8)
>>> d.fiscal_year
2017
>>> d.prev_fiscal_year
FiscalYear(2016)
```

## Installation

`fiscalyear` has no dependencies, making it simple and easy to install. The recommended way to install `fiscalyear` is with `pip`.

```bash
$ pip install fiscalyear
```

For alternate installation methods, see the [Installation Documentation](http://fiscalyear.readthedocs.io/en/latest/installation.html).

## Documentation

Documentation is hosted on [Read the Docs](http://fiscalyear.readthedocs.io/en/latest/index.html).
