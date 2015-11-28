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
        words[index] = self.lemmatizer.lemmatize(word, tags[index])
    return words