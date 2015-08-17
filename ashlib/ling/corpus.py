import os
import sys

import nltk
import nltk.probability

from ..util import file_

## language model #####################################################################################

UNIGRAM_LANGUAGE_MODEL = nltk.probability.LaplaceProbDist(nltk.FreqDist(nltk.corpus.brown.words()))

def unigramProbability(word):
    return UNIGRAM_LANGUAGE_MODEL.prob(word)

## stop words #########################################################################################

STOP_WORDS = set(file_.readlines(os.path.join(os.path.dirname(__file__), "res", "english.stop")))

def isStopWord(word):
    return word in STOP_WORDS
    
def removeStopWords(words):
    index = 0
    while index < len(words):
        word = words[index]
        if word in STOP_WORDS: del words[index]
        else: index += 1

## dictionary #########################################################################################

ENGLISH_DICTIONARY = set(line.strip() for line in open(os.path.join(os.path.dirname(__file__), "res", "englishwords.txt")))

def isWord(word):
    return word.lower() in ENGLISH_DICTIONARY

## common words #######################################################################################

COMMON_WORDS = set(open(os.path.join(os.path.dirname(__file__), "res", "commonwords.txt")).read().split(','))

def isCommon(word):
    return word.lower() in COMMON_WORDS

## punctuation ########################################################################################

PUNCTUATION = set([".", "?", "!", ",", "\"", ":", ";", "'", "-"])

def isPunctuation(word):
    return word in PUNCTUATION
