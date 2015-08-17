import os
import sys

import file_

def listStdDir(dirPath):
    std = []
    for name in os.listdir(dirPath):
        if not file_.hidden(name):
            std.append(os.path.join(dirPath, name))
    return std

def makeIfNonexistant(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
