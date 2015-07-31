import os
import sys
import math

# All functions in this module were taken from the
# pattern.en library, with minor modifications.

def mean(iterable):
    a = iterable if isinstance(iterable, list) else list(iterable)
    return float(sum(a)) / float(len(a) or 1)

def average(iterable):
    return mean(iterable)

def median(iterable, sort=True):
    s = sorted(iterable) if sort is True else list(iterable)
    n = len(s)
    if n == 0:
        raise ValueError("median() arg is an empty sequence")
    if n % 2 == 0:
        return float(s[(n // 2) - 1] + s[n // 2]) / 2
    return s[n // 2]

def variance(iterable, sample=False):
    a = iterable if isinstance(iterable, list) else list(iterable)
    m = mean(a)
    return sum((x - m) ** 2 for x in a) / (len(a) - int(sample) or 1)

def stdev(iterable, *args, **kwargs):
    return math.sqrt(variance(iterable, *args, **kwargs))

def main():
    # Tests
    assert mean([1, 2, 3, 4 ,5]) == 3
    assert mean([1, 2.5]) == 1.75
    assert median([1, 2, 3, 4, 7]) == 3
    assert median([1, 2, 5, 6]) == 3.5
    assert round(variance([1,3,4,7,8]), 2) == 6.64
    assert round(stdev([1,3,4,7,8]), 2) == 2.58

if __name__ == "__main__":
    main()
