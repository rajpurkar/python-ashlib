import os
import sys
import re

import cnlp
import token

## functions ################################################################################################

def resolve(text, replacementSelector=None):
    sentences, parseTrees, coref = cnlp.CoreNLP().parse(text)
    if replacementSelector is None: replacementSelector = defaultReplacementSelector
    sentences = __mergeCoreferent(sentences, coref, replacementSelector)
    return " ".join(token.reverseTokenize(sentence) for sentence in sentences)

def __mergeCoreferent(sentences, coref, replacementSelector):
    # Replace all phrases in each set of coreferent
    # noun phrases with the longest phrase in the set.
    # To be specific, replace first word with list
    # containing all words in replacement, and
    # subsequent words with None. Doing so prevents
    # word indexing from changing - consistency is
    # necessary for applying future coreference
    # replacements.
    for set in coref:
        sentence, start, end = replacementSelector(set)
        replacement = sentences[sentence][start:end]
        for phrase in set:
            ## TODO: could check to ensure replacment not None or list, and abort replacement if is.
            sentences[phrase[0]][phrase[1]] = replacement
            for index in range(phrase[1] + 1, phrase[2]):
                sentences[phrase[0]][index] = None

    # Remove None tokens:
    for sentence in sentences:
        index = 0
        while index < len(sentence):
            word = sentence[index]
            if word is None: del sentence[index]
            else: index += 1

    # Expand embedded lists of words:
    for sentence in sentences:
        wordOrListIndex = 0
        while wordOrListIndex < len(sentence):
            wordOrList = sentence[wordOrListIndex]
            if isinstance(wordOrList, list):
                for wordIndex, word in enumerate(wordOrList):
                    sentence.insert(wordOrListIndex + wordIndex + 1, word)
                del sentence[wordOrListIndex]
                wordOrListIndex += len(wordOrList)
            wordOrListIndex += 1

    return sentences

def defaultReplacementSelector(self, coreferentSet):
    # returns longest noun phrase
    return sorted(coreferentSet, key=lambda phrase: (phrase[2] - phrase[1]), reverse=True)[0]

## CoreferenceResolver ####################################################################################

class CoreferenceResolver(object):

    def __init__(self):
        self.cnlp = cnlp.CoreNLP()

    def resolve(self, text, replacementSelector=None):
        return resolve(text, replacementSelector=replacementSelector)

def main():
    resolver = CoreferenceResolver()
    result = resolver.resolve("Hello world.  It is so beautiful")
    print result

if __name__ == "__main__":
    main()