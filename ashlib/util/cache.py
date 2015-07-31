import os
import sys
import dill as pickle

def dump(object, filePath):
    file = open(filePath, "w+")
    pickle.dump(object, file)
    file.close()

def load(filePath):
    file = open(filePath, "r")
    object = pickle.load(file)
    file.close()
    return object