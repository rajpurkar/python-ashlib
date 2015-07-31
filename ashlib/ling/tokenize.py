import os
import sys

import nltk
import nltk.tokenize

def characters(text, ignoreSpaces=False, ignorePunctuation=True):
    text = text.replace("\n", "").replace("\t", "")
    if ignoreSpaces:
        text = text.replace(" ", "")
    if ignorePunctuation:
        return [char for char in text if not self.isPunctuation(char)]
    else:
        return [char for char in text]

def words(sentence):
    return nltk.tokenize.word_tokenize(sentence)

def reverse(words):
    ## TODO: this is really shitty. Should look for a library that already does this.
    ## TODO: could make so if word starts with ' just append it, but haven't through whether or not there are significant cases in which that woudl fuck up
    words = list(words)
    text = ""
    for index, word in enumerate(words):
        if index == 0: text += word
        elif word == "'s": text += word
        elif word == "n't": text += word
        elif word == "'ve": text += word
        elif word == "'ll": text += word
        elif word in [",", ".", "?", "!", ":", ";"]: text += word
        elif index > 0 and words[index - 1] == "``": text += word
        elif word == "''": text += word
        else: text += " " + word
    return text

def sentences(text):
    initial = nltk.tokenize.sent_tokenize(text.replace(".\"", "\n").replace(u".\u201D", "\n"))
    sentences = []
    for sentence in initial:
        sentences.append(sentence.replace("\n", " "))
    return sentences

def paragraphs(text):
    paragraphs = []
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if len(paragraph) > 0:
            paragraphs.append(paragraph)
    return paragraphs
