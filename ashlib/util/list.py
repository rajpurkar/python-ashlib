import os
import sys
import urllib

def concatenate(lists):
    concatenation = []
    for aList in lists:
        concatenation += aList
    return concatenation

def first(aList):
    return None if len(aList) == 0 else aList[0]

def last(aList):
    return None if len(aList) == 0 else aList[-1]

def conditionHoldsForAllItems(condition, aList):
    for item in aList:
        if not condition(item):
            return False
    return True

def containsAnyOf(items, aList):
    for item in items:
        if item in aList:
            return True
    return False

def count(aList, condition=lambda item: True):
    return sum(condition(item) for item in aList)

def replace(aList, modifier):
    for index, item in enumerate(aList):
        aList[index] = modifier(item)
    return aList

def iprint(aList):
    print "["
    for item in aList:
        print " ", item
    print "]"

def permutations(lists):
    if len(lists) > 0:
        perms = [[item] for item in lists[0]]
        for index in range(1, len(lists)):
            newPerms = []
            for perm in perms:
                for item in lists[index]:
                    newPerms.append(perm + [item])
            perms = newPerms
        return perms

    else:
        return []
