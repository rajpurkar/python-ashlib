import os
import sys
import re
import time
import threading
import subprocess
import signal

import nltk.stem.wordnet

import pos

LEMMATIZER = nltk.stem.wordnet.WordNetLemmatizer()

def lemmatize(words):
    tags = pos.tag(words)
    for index, word in enumerate(words):
        try:
            ## TODO: might be missing some wordnet POS tags, and also might be bad even if not
            tag = pos.standardizeWordnet(tags[index])
            words[index] = LEMMATIZER.lemmatize(word, tag)
        except ValueError as error:
            words[index] = LEMMATIZER.lemmatize(word)
    return words