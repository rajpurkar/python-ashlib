import os
import sys

import file

def listStdDir(dirPath):
    std = []
    for name in os.listdir(dirPath):
        if not file.hidden(name):
            std.append(os.path.join(dirPath, name))
    return std

