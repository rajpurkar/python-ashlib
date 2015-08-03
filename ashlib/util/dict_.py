import os
import sys
import operator

def maxValue(dictionary):
    if len(dictionary) > 0:
        return max(dictionary.iteritems(), key=operator.itemgetter(1))[1]
    else:
        return None

def maxKey(dictionary):
    if len(dictionary) > 0:
        return max(dictionary.iteritems(), key=operator.itemgetter(1))[0]
    else:
        return None

def toJson(dictionary):
    ## TODO: not sure this is robust to things like escaped quotes, or even "u"s at the end of a string
    ## TODO: also not sure this is a great location for this function, organizationally
    return str(dictionary).replace("u'", "\"").replace("'", "\"")
