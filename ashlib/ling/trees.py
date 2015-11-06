import os
import sys
import re
import copy

import nltk.tree

from ..util import regex
from ..util import str_
from ..util import list_

import tokenize

## basic ###########################################################################################################

def isWord(tree):
    return isinstance(tree, nltk.tree.Tree) and len(tree) == 1 and isinstance(tree[0], basestring)

def getWord(tree):
    if isWord(tree): return tree[0]
    else: raise ValueError("|tree| must be a valid word tree.")

def wordMatches(tree, matcher):
    return isWord(tree) and str_.matches(getWord(tree), matcher)

def posMatches(tree, matcher):
    if isinstance(tree, nltk.tree.Tree): return str_.matches(tree.label(), matcher)
    else: return False

def isPotentialNounPhrase(tree):
    return posMatches(tree, lambda tag: tag.startswith("N") or tag == "S")

def extractWords(tree):
    return tree.leaves()

def prune(tree, start, end=None):
    if end is None: return nltk.tree.Tree(tree.label(), children=tree[start:])
    else: return nltk.tree.Tree(tree.label(), children=tree[start:end])

def toString(tree):
    return tokenize.reverse(extractWords(tree))

def matchesWord(tree, word):
    return isinstance(tree[0], basestring) and tree[0].lower() == word

def containsPhrase(tree, phrase):
    if isinstance(tree, basestring): return False
    else: return regex.containsPhrase(phrase, tree.leaves(), flags=re.IGNORECASE)

def containsPhrases(tree, phrases):
    return all(containsPhrase(tree, phrase) for phrase in phrases)

def reduceIfPossible(tree, function):
    matches = list_.concatenate(function(child) for child in tree)
    return matches if matches else [tree]

def findPhrase(tree, phrase):
    # |phrase| should be a list/tuple of words (strings)
    # |tree| should be an NLTK tree
    if isinstance(tree, basestring): return []
    if not containsPhrase(tree, phrase): return []
    else: return reduceIfPossible(tree, lambda child: findPhrase(child, phrase))

def findWord(tree, word):
    return findPhrase(tree, [word])

def anonymize(tree):
    tree = copy.deepcopy(tree)
    
    def recurisiveAnonymize(tree):
        for i, child in enumerate(tree):
            if isinstance(child, basestring): tree[i] = ""
            else: recurisiveAnonymize(child)

    recurisiveAnonymize(tree)
    return tree

## Minimum Complete Trees ##########################################################################################

def findMCTs(tree, phrase1, phrase2):
    if isinstance(tree, basestring): return []
    if not nlp.tree.containsPhrases(tree, [phrase1, phrase2]): return []
    else: return nlp.tree.reduceIfPossible(tree, lambda child: findMCTs(child, phrase1, phrase2))

## Path-Enclosed Trees #############################################################################################

def pruneWords(tree, phrase, left):
    ## TODO: won't work for repeated first/last words
    if isinstance(tree, nltk.tree.Tree):
        index = 0 if left else -1
        word = phrase[index].lower()
        while len(tree) != 0:
            child = tree[index]
            if nlp.tree.isWord(child):
                if child[0].lower() == word: break
                else: tree.pop(index)
            else:
                pruneWords(child, phrase, left)
                break

def pruneLeft(tree, phrase):
    if isinstance(tree, nltk.tree.Tree):
        for index, child in enumerate(tree):
            if nlp.tree.containsPhrase(child, phrase):
                for i in range(index): tree.pop(0)
                pruneLeft(tree[0], phrase)
                break

    pruneWords(tree, phrase, True)

def pruneRight(tree, phrase):
    if isinstance(tree, nltk.tree.Tree):
        for index in range(len(tree) - 1, -1, -1):
            child = tree[index]
            if nlp.tree.containsPhrase(child, phrase):
                numIters = len(tree) - index - 1
                for i in range(numIters): tree.pop(-1)
                pruneRight(tree[-1], phrase)
                break

    pruneWords(tree, phrase, False)

def findPT(tree, phrase1, phrase2):
    tree = copy.deepcopy(tree)
    
    for child in tree:
        if nlp.tree.containsPhrase(child, phrase1):
            pruneLeft(tree, phrase1)
            pruneRight(tree, phrase2)
            break
        
        if nlp.tree.containsPhrase(child, phrase2):
            pruneLeft(tree, phrase2)
            pruneRight(tree, phrase1)
            break

    return tree

def findPTs(tree, phrase1, phrase2):
    mcts = findMCTs(tree, phrase1, phrase2)
    return [findPT(mct, phrase1, phrase2) for mct in mcts]

def wordsBetweenPhrases(tree, phrase1, phrase2):
    pt = findPTs(tree)[0] ## TODO: sorta hacky to just use the first
    if phrase1[0].lower() == pt.leaves()[0].lower(): return pt.pos()[len(phrase1):-len(phrase2)]
    else: return pt.pos()[len(phrase2):-len(phrase1)]
