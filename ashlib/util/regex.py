import os
import sys
import re

def matches(regex, string):
    return not re.match(regex, string) is None

def wordRegex(word):
    ## TODO: can use "\b"? Test because might not work
    ##return "(?<![\w\.\-])" + re.escape(word) + "(?![\w\-])" ## TODO: which version to use?
    return "(?<![\w\.\-])" + word + "(?![\w\-])"

def containsWord(word, string, flags=0):
    return len(re.findall(wordRegex(word), string, flags=flags)) > 0

def findMentions(words, string, flags=0):
    mentions = []
    for word in words:
        if containsWord(word, string, flags=flags):
            mentions.append(word)
    return mentions

def containsOne(words, string, flags=0):
    return len(findMentions(words, string, flags=flags)) > 0
