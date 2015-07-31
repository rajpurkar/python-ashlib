import os
import sys
import unicodedata

def sanitize(string):
    if type(string) is str: return string.decode("ascii")
    elif type(string) is unicode: return unicodedata.normalize("NFKD", string).encode("ascii", "ignore")
    else: return ""

def aggressivelySanitize(string):
    return "".join([char if ord(char) < 128 else "" for char in string])

def isAllCaps(word):
    return word.upper() == word

def isCapitalized(word):
    return len(word) > 0 and isAllCaps(word[0])

def splitOnCaps(string):
    parts = []
    startIndex = 0
    for index in range(len(string)):
        if isCapitalized(string[index]):
            if index > startIndex:
                parts.append(string[startIndex:index])
            startIndex = index
    if startIndex < len(string):
        parts.append(string[startIndex:])
    return parts

def capitalize(string):
    if len(string) > 0: return string[0].upper() + string[1:]
    else: return string

def matches(string, matcher):
    ## TODO: could look at how beatiful soup determines type of arg and copy
    if isinstance(matcher, basestring):
        return string == matcher
    elif callable(matcher):
        return matcher(string)
    else:
        # We check to see if |matcher| is a compiled regular expression:
        try: match = matcher.match(string)
        except AttributeError: raise ValueError("|matcher| must be a string, function or compiled regular expression.")
        else: return not match is None
