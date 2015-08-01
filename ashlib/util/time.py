import os
import sys

import datetime
import dateutil.parser

def today():
    return datetime.datetime.today()

def withinDays(date, referenceDate, days):
    date = date.replace(tzinfo=None)
    referenceDate.replace(tzinfo=None)
    delta = datetime.timedelta(days=days)
    return date >= referenceDate - delta

def withinDaysOfToday(date, days):
    return withinDays(date, today(), days)

def withinWeekOf(date, referenceDate):
    return withinDays(date, referenceDate, 7)

def inLastWeek(date):
    return withinWeekOf(date, today())

def withinDayOf(date, referenceDate):
    return withinDays(date, referenceDate, 1)

def inLastDay(date):
    return withinDayOf(date, today())