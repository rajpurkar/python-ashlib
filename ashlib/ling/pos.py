import os
import sys

import nltk

## TODO: need to add in phrase tags. Also: ROOT, S, etc.

## constants ##################################################################################

VERB_PREFIX = "VB"
ADJECTIVE_PREFIX = "JJ"
NOUN_PREFIX = "NN"
PROPER_NOUN_PREFIX = "NNP"
PRONOUN_PREFIX = "PRP"
WH_PRONOUN_PREFIX = "WP"
ADVERB_PREFIX = "RB"
ARTICLE_TAG = "DT"

STANDARD_TAGS = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]
WORDNET_TAG_MAPPING = { "a" : "JJ", "s" : "JJ", "r" : "RB", "n" : "NN", "v" : "VB" }

## functions ##################################################################################

def root(tag):
    if isVerb(tag):
        return VERB_PREFIX
    if isAdjective(tag):
        return ADJECTIVE_PREFIX
    if isNoun(tag):
        return NOUN_PREFIX
    if isPronoun(tag):
        return PRONOUN_PREFIX
    if isAdverb(tag):
        return ADVERB_PREFIX
    return tag

def isVerb(tag):
    return tag.startswith(VERB_PREFIX)

def isAdjective(tag):
    return tag.startswith(ADJECTIVE_PREFIX)

def isNoun(tag):
    return tag.startswith(NOUN_PREFIX)

def isProperNoun(tag):
    return tag.startswith(PROPER_NOUN_PREFIX)

def isPronoun(tag):
    return tag.startswith(PRONOUN_PREFIX) or tag.startswith(WH_PRONOUN_PREFIX)

def isAdverb(tag):
    return tag.startswith(ADVERB_PREFIX)

def isArticle(tag):
    return tag == ARTICLE_TAG

def tag(words):
    return [pair[1] for pair in nltk.pos_tag(words)]

def standardizeWordnet(tag):
    if tag in WORDNET_TAG_MAPPING:
        return WORDNET_TAG_MAPPING[tag]
    else:
        raise ValueError("Unrecognized Wordnet POS tag.")

## main #######################################################################################

def main():
    assert isVerb("VB")
    assert isVerb("VBD")
    assert isAdjective("JJ")
    assert isAdjective("JJR")
    assert isNoun("NN")
    assert isNoun("NNP")
    assert isProperNoun("NNP")
    assert isPronoun("PRP")
    assert isPronoun("PRP$")
    assert isPronoun("WP")
    assert isPronoun("WP$")
    assert isAdverb("RB")
    assert isAdverb("RBR")

    assert root("VBD") == "VB"

if __name__ == '__main__':
    main()
