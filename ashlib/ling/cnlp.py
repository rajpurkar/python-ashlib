import os
import sys
import re

import simplejson
import nltk.tree

import corenlp.jsonrpc
import corenlp.corenlp

## private functions ##########################################################################################################

def _rawParseWithServer(text, server):
    if len(text) <= 600: ## TODO: refine this number
        NUM_ATTEMPTS = 5
        for _ in range(NUM_ATTEMPTS):
            try: return simplejson.loads(server.parse(text))
            except (corenlp.jsonrpc.RPCInternalError, corenlp.jsonrpc.RPCTransportError) as e: pass
    return None

def _rawParse(text):
    server = corenlp.jsonrpc.ServerProxy(corenlp.jsonrpc.JsonRpc20(),
                                     corenlp.jsonrpc.TransportTcpIp(addr=("127.0.0.1", 8080)))
    return _rawParseWithServer(text, server)

def _extractSentences(raw):
    if raw is None:
        return None
    
    try:
        sentences = []
        for sentence in raw["sentences"]:
            sentences.append([])
            for wordContents in sentence["words"]:
                sentences[-1].append(wordContents[0])
        return sentences
    
    except KeyError as e:
        return None

def _extractSyntacticParseTrees(raw):
    if raw is None:
        return None
    
    try:
        trees = []
        for sentence in raw["sentences"]:
            trees.append(nltk.tree.Tree.fromstring(sentence["parsetree"]))
        return trees

    except KeyError as e:
        return None

def _extractCoref(raw):
    # Note: Currently we treat all mentions correferent with
    # the same entity as coreferent.
    
    if raw is None:
        return None
    
    try:
        coref = []
        if "coref" in raw:
            for set in raw["coref"]:
                coref.append([])
                for pair in set:
                    if len(pair) > 2:
                        raise Exception("Coref formatted differently than expected - modify code.")
                    for phrase in pair:
                        term = (phrase[1], phrase[3], phrase[4])
                        if not term in coref[-1]:
                            coref[-1].append(term)
        return coref

    except KeyError as e:
        return None

def _parse(raw):
    if raw is None:
        return (None, None, None)
    sentences = _extractSentences(raw)
    trees = _extractSyntacticParseTrees(raw)
    coref = _extractCoref(raw)
    return (sentences, trees, coref)

## public functions ############################################################################################################

def extractSentences(text):
    return _extractSentences(_rawParse(text))

def extractSyntacticParseTrees(text):
    return _extractSyntacticParseTrees(_rawParse(text))

def extractCoref(text):
    return _extractCoref(_rawParse(text))

def parse(text):
    return _parse(_rawParse(text))

## CoreNLP #####################################################################################################################

class CoreNLP(object):
    
    def __init__(self):
        self.server = corenlp.jsonrpc.ServerProxy(corenlp.jsonrpc.JsonRpc20(),
                                                  corenlp.jsonrpc.TransportTcpIp(addr=("127.0.0.1", 8080)))

    # Public methods:

    def extractSentences(self, text):
        return _extractSentences(self.__rawParse(text))

    def extractSyntacticParseTrees(self, text):
        return _extractSyntacticParseTrees(self.__rawParse(text))

    def extractCoref(self, text):
        return _extractCoref(self.__rawParse(text))

    def parse(self, text):
        return _parse(_rawParseWithServer(text, self.server))
