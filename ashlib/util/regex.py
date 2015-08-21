import os
import sys
import re

def matches(regex, string):
    return re.match(regex, string) is not None

def wordRegex(word):
    ## TODO: can use "\b"? Test because might not work
    ##return "(?<![\w\.\-])" + re.escape(word) + "(?![\w\-])" ## TODO: which version to use?
    return "(?<![\w\.\-])" + word + "(?![\w\-])"

def containsWord(word, string, flags=0):
    return len(re.findall(wordRegex(word), string, flags=flags)) > 0

def startsWithWord(word, string, flags=0):
    return len(re.findall("^%s(?![\w\-])" % word, string, flags=flags)) > 0

def endsWithWord(word, string, flags=0):
    return len(re.findall("(?<![\w\.\-])%s$" % word, string, flags=flags)) > 0

def findMentions(words, string, flags=0):
    mentions = []
    for word in words:
        if containsWord(word, string, flags=flags):
            mentions.append(word)
    return mentions

def containsOne(words, string, flags=0):
    return len(findMentions(words, string, flags=flags)) > 0
