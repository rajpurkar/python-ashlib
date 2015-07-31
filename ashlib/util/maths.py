import os
import sys
import math

def sigmoid(value):
    return 1.0 / (1.0 + math.exp(-value))

def hmean(x, y):
    # Computes the harmonic mean of |x| and |y|
    x = float(x)
    y = float(y)
    return 2.0 * (x * y) / (x + y)
