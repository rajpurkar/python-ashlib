import os
import sys
import math
import collections
import copy

import mymath

def itemSum(vector1, vector2):
    result = copy.deepcopy(vector1)
    for key in vector2:
        if key in result: result[key] += vector2[key]
        else: result[key] = vector2[key]
    return result

def itemDifference(vector1, vector2):
    result = copy.deepcopy(vector1)
    for key in vector2:
        if key in result: result[key] -= vector2[key]
        else: result[key] = -vector2[key]
    return result

def dotProduct(vector1, vector2):
    total = 0.0
    for key in vector1:
        if key in vector2: total += vector1[key] * vector2[key]
    return total

def product(d1, d2, default=0.0):
    if default != 0.0 and default != 1.0:
        raise Exception("Default value must be 0 or 1.")
    prod = {}
    for key in d1:
        if key in d2:
            prod[key] = d1[key] * d2[key]
        else:
            prod[key] = d1[key]
    for key in d2:
        if key in d1:
            prod[key] = d1[key] * d2[key]
        else:
            prod[key] = d2[key]
    return prod

def modulus(d1):
    return math.sqrt(dotProduct(d1, d1))

def cosine(d1, d2):
    return dotProduct(d1, d2) / (modulus(d1) * modulus(d2))

def angle(d1, d2):
    cos = cosine(d1, d2)
    if cos > 1.0: cos = 1.0
    if cos < -1.0: cos = -1.0
    return math.acos(cos)

def unit(d1):
    unit = {}
    mod = modulus(d1)
    for key in d1:
        unit[key] = float(d1[key]) / mod
    return unit

def average(vectors):
    sums = collections.Counter()
    for vector in vectors:
        for key in vector:
            sums[key] += float(vector[key])
    return {key:(sums[key] / len(vectors)) for key in sums}

def weightedAverage(vectors, weights):
    total = sum(weights)
    sums = collections.Counter()
    for index, vector in enumerate(vectors):
        for key in vector:
            sums[key] += float(vector[key]) * weights[index]
    return {key:(sums[key] / total) for key in sums}

def squaredDistance(vector1, vector2):
    first = dotProduct(vector1, vector1)
    second = dotProduct(vector2, vector2)
    third = dotProduct(vector1, vector2)
    return first + second - 2.0 * third

def distance(vector1, vector2):
    return math.sqrt(squaredDistance(vector1, vector2))

def toInt(vector):
    for key in vector:
        vector[key] = int(vector[key])
    return vector

def normalize(vector):
    total = sum(vector.itervalues())
    for key in vector:
        vector[key] = float(vector[key]) / float(total)
    return vector

def increment(d1, scale, d2):
    # Taken from the CS 221 pset 2 (sentiment) util file.
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

def scale(d1, factor):
    increment(d1, factor - 1, d1)
