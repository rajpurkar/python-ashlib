import os
import sys

import nltk
import nltk.probability

## LanguageModel ########################################################################################

class LanguageModel(object):
    
    def __init__(self):
        frequencies = nltk.FreqDist(nltk.corpus.brown.words())
        self.model = nltk.probability.LaplaceProbDist(frequencies)
    
    def unigramProb(self, unigram):
        return self.model.prob(unigram)

## StopList #############################################################################################

class StopList(object):
    
    def __init__(self):
        self.words = set(self.__readFile(os.path.join(os.path.dirname(__file__), "res", "english.stop")))
    
    def contains(self, word):
        return word in self.words
    
    def removeStopWords(self, document):
        index = 0
        while index < len(document):
            word = document[index]
            if self.contains(word): del document[index]
            else: index += 1
    
    def __readFile(self, fileName):
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        result = "\n".join(contents).split()
        return result

## EnglishDictionary #####################################################################################

class EnglishDictionary(object):
    
    ## TODO: could consider making this a subclass of set. The challange is overwriting all necessary methods to make the input word lower case, so that the client doesn't have to worry about that.

    def __init__(self):
        self.words = set(line.strip() for line in open(os.path.join(os.path.dirname(__file__), "res", "englishwords.txt")))

    def contains(self, word):
        return word.lower() in self.words

## EnglishTrends #########################################################################################

class EnglishTrends(object):

    ## TODO: like with dictionary, could consider making this a subclass of set. Again, the challange is overwriting all necessary methods to make the input word lower case, so that the client doesn't have to worry about that.

    def __init__(self):
        self.words = set(open(os.path.join(os.path.dirname(__file__), "res", "commonwords.txt")).read().split(','))

    def isCommon(self, word):
        return word.lower() in self.words
