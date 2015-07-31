import os
import sys
import csv
import ntpath

def read(filePath):
    with open(filePath, "r") as file:
        return file.read()

def readlines(filePath):
    with open(filePath, "r") as file:
        return [line.strip() for line in file.readlines()]

def overwrite(filePath, content):
    with open(filePath, "w+") as file:
        file.write(content)

def hidden(path):
    return path.find(".") == 0

def hasExtension(extension, fileName):
    return fileName.endswith("." + extension)

def extractName(filePath):
    return ntpath.basename(filePath)

def csv2mat(path):
    with open(path, "rU") as file:
        return [[item for item in row] for row in csv.reader(file)]
