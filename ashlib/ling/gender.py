#!/usr/bin/env python
# CS124 Homework 5 Jeopardy
# Original written in Java by Sam Bowman (sbowman@stanford.edu)
# Ported to Python by Milind Ganjoo (mganjoo@stanford.edu)

# NOTE: As mentioned above, this class was taken from the
# starter code for the fifth homework assignment in CS 124,
# with modifications.

import os
import sys

import language.person

## constants ##########################################################################################################

MALE = "male"
FEMALE = "female"
NEUTRAL = "neutral"

## functions ##########################################################################################################

def isMale(gender):
    return gender == MALE

def couldBeMale(gender):
    return gender != FEMALE

def isFemale(gender):
    return gender == FEMALE

def couldBeFemale(gender):
    return gender != MALE

## GenderClassifier ###################################################################################################

class GenderClassifier(object):
    
    def __init__(self):
        # To stay current, we use only the most freshly
        # downloaded copies of 1990 census data.
        self.male_names = self.load_dict(os.path.join(os.path.dirname(__file__), "res", "dist.male.first.tsv"))
        self.female_names = self.load_dict(os.path.join(os.path.dirname(__file__), "res", "dist.female.first.tsv"))

    def guessGender(self, name):
        name = name.upper()
        if name in self.male_names:
            if name in self.female_names:
                if self.male_names[name] > 3 * self.female_names[name]:
                    return MALE
                elif 3 * self.male_names[name] < self.female_names[name]:
                    return FEMALE
                else:
                    return NEUTRAL
            else:
                return MALE
        elif name in self.female_names:
            return FEMALE
        return NEUTRAL

    def isMale(self, name):
        return isMale(self.guessGender(name))

    def couldBeMale(self, name):
        return couldBeMale(self.guessGender(name))

    def isFemale(self, name):
        return isFemale(self.guessGender(name))

    def couldBeFemale(self, name):
        return couldBeFemale(self.guessGender(name))

    def load_dict(self, file_name):
        count_dict = {}
        with open(file_name) as f:
            for line in f:
                name, freq = line.split()[:2]
                count_dict[name] = float(freq)
        return count_dict
