import os
import sys
import dill as pickle


def dump(obj, filePath):
    pickle.dump(obj, open(filePath, "wb"))


def load(filePath):
    return pickle.load(open(filePath, "rb"))
