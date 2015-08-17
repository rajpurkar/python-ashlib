import os
import sys
import math

import scipy.stats.stats
import numpy

# All functions in this module were taken from the
# pattern.en library, with minor modifications.

def mean(iterable):
    a = iterable if isinstance(iterable, list) else list(iterable)
    return float(sum(a)) / float(len(a) or 1)

def average(iterable):
    return mean(iterable)

def ema(iterable, window):
    weights = numpy.exp(numpy.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  numpy.convolve(values, weights)[:len(values)]
    a[:window] = a[window]
    return a[-1]

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

def covariance(iterable1, iterable2):
    return numpy.cov(iterable1, iterable2)[0][1] ## TODO: I don't think this is write - I think I should stack the iterables and feed them in as one arg (maybe transpose that)

def correlation(iterable1, iterable2):
    return scipy.stats.stats.pearsonr(iterable1, iterable2)[0]

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
