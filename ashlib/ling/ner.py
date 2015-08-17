import os
import sys
import collections

import nltk.tag

import corpus

## NERTagger ################################################################################################

class NERTagger(object):

    def __init__(self, taggerPath, taggerVersion):
        self.tagger = nltk.tag.stanford.StanfordNERTagger(os.path.join(taggerPath,
                                                                       "classifiers",
                                                                       "english.all.3class.distsim.crf.ser.gz"),
                                                          os.path.join(taggerPath,
                                                                       "stanford-ner-" + taggerVersion + ".jar"))

    def tags(self, words):
        pairs = self.tagger.tag(["_" if corpus.isPunctuation(word) else word for word in words])
        if len(words) == 1: pairs = [pairs]
        return [pair[1] for pair in pairs]

    def entities(self, words):
        tags = self.tags(words)
        entities = []
        
        def addEntity(entity, tag):
            if entity is not None:
                entities.append((entity, tag))
        
        currentEntity = None
        currentTag = None
        
        for index, tag in enumerate(tags):
            word = words[index]
            if tag == "O":
                addEntity(currentEntity, currentTag)
                currentEntity = None
                currentTag = None
            elif tag == currentTag:
                currentEntity.append(word)
            else:
                currentEntity = [word]
                currentTag = tag

        addEntity(currentEntity, currentTag)
        
        return entities
