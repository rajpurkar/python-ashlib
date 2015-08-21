import os
import sys

import nltk
import nltk.probability

from ..util import file_

## language model #####################################################################################

UNIGRAM_LANGUAGE_MODEL = [None]

def __unigramLanguageModel():
    if UNIGRAM_LANGUAGE_MODEL[0] is None:
        UNIGRAM_LANGUAGE_MODEL[0] = nltk.probability.LaplaceProbDist(nltk.FreqDist(nltk.corpus.brown.words()))
    return UNIGRAM_LANGUAGE_MODEL[0]

def unigramProbability(word):
    return __unigramLanguageModel().prob(word)

## stop words #########################################################################################

STOP_WORDS = [None]

def __stopWords():
    if STOP_WORDS[0] is None:
        path = os.path.join(os.path.dirname(__file__), "res", "english.stop")
        STOP_WORDS[0] = set(file_.readlines(path))
    return STOP_WORDS[0]

def isStopWord(word):
    return word in __stopWords()
    
def removeStopWords(words):
    index = 0
    while index < len(words):
        word = words[index]
        if word in __stopWords(): del words[index]
        else: index += 1

## dictionary #########################################################################################

ENGLISH_DICTIONARY = [None]

def __englishDictionary():
    if ENGLISH_DICTIONARY[0] is None:
        path = os.path.join(os.path.dirname(__file__), "res", "englishwords.txt")
        ENGLISH_DICTIONARY[0] = set(line.strip() for line in open(path))
    return ENGLISH_DICTIONARY[0]

def isWord(word):
    return word.lower() in __englishDictionary()

## common words #######################################################################################

COMMON_WORDS = [None]

def __commonWords():
    if COMMON_WORDS[0] is None:
        path = os.path.join(os.path.dirname(__file__), "res", "commonwords.txt")
        COMMON_WORDS[0] = set(open(path).read().split(','))
    return COMMON_WORDS[0]
                                    
def isCommon(word):
    return word.lower() in __commonWords()

## punctuation ########################################################################################

PUNCTUATION = [None]

def __punctuation():
    if PUNCTUATION[0] is None:
        PUNCTUATION[0] = set([".", "?", "!", ",", "\"", ":", ";", "'", "-"])
    return PUNCTUATION[0]

def isPunctuation(word):
    return word in PUNCTUATION
