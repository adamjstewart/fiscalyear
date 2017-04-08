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
datetime.datetime(2016, 10, 1, 0, 0)
>>> a.end
datetime.datetime(2017, 9, 30, 23, 59, 59)
```

By default, it uses the U.S. federal government's fiscal year, which begins on October 1st of the previous calendar year and ends on September 30th of that year. However, you can easily change this to match the fiscal year of your government, institution, or business. For example, in the United Kingdom, the fiscal year starts on April 1st and ends on March 31st.

```python
>>> import fiscalyear
>>> fiscalyear.START_MONTH = 4
>>> a.start
datetime.datetime(2016, 4, 1, 0, 0)
>>> a.end
datetime.datetime(2017, 3, 31, 23, 59, 59)
```

### FiscalQuarter

The `FiscalYear` class also allows you to query information about a specific quarter.

```python
>>> a.q3.start
datetime.datetime(2017, 4, 1, 0, 0)
>>> a.q3.end
datetime.datetime(2017, 6, 30, 23, 59, 59)
```

These objects represent the standalone `FiscalQuarter` class.

```python
>>> b = FiscalQuarter(2017, 3)
>>> b.start
datetime.datetime(2017, 4, 1, 0, 0)
>>> b.end
datetime.datetime(2017, 6, 30, 23, 59, 59)
>>> a.q3 == b
True
```

### FiscalDate

### FiscalDateTime

## Installation

### pip

### Spack

### source

## Contributing
