import os
import sys
import re
import time
import threading
import subprocess
import signal

import simplejson
import nltk.tree

import corenlp.jsonrpc
import corenlp.corenlp

from ..util import process

## private functions ##########################################################################################################

def _rawParseWithProxy(text, proxy):
    if len(text) <= 600: ## TODO: refine this number
        NUM_ATTEMPTS = 3
        for _ in range(NUM_ATTEMPTS):
            try:
                return simplejson.loads(proxy.parse(text))
            except (corenlp.jsonrpc.RPCInternalError, corenlp.jsonrpc.RPCTransportError, corenlp.jsonrpc.RPCParseError) as error:
                print "CoreNLP Error:", error
    return None

def _rawParse(text):
    proxy = corenlp.jsonrpc.ServerProxy(corenlp.jsonrpc.JsonRpc20(),
                                     corenlp.jsonrpc.TransportTcpIp(addr=("127.0.0.1", 8080)))
    return _rawParseWithProxy(text, proxy)

def _extractSentences(raw):
    if raw is None:
        return None
    
    try:
        return [sentence["text"] for sentence in raw["sentences"]]
    except KeyError as e:
        return None

def _extractSyntacticParseTrees(raw):
    if raw is None:
        return None
    
    try:
        trees = []
        for sentence in raw["sentences"]:
            tree = sentence["parsetree"]
            if tree.rfind("] ") != -1:
                tree = tree[tree.rfind("] ") + 2:]
            trees.append(nltk.tree.Tree.fromstring(tree))
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
    else:
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

## TODO: ultimately, all of the server generation stuff should be done at the global variable level and not the clas level (given current implementation only one instance can exist at a time)

class CoreNLP(object):
    
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8080
    CONSECUTIVE_ERROR_THRESHOLD = 2
    
    def __init__(self, cnlpPath, cnlpVersion):
        self.cnlpPath = cnlpPath
        self.cnlpVersion = cnlpVersion
        self.consecutiveErrorCount = 0
        transport = corenlp.jsonrpc.TransportTcpIp(addr=(self.SERVER_HOST, self.SERVER_PORT))
        self.proxy = corenlp.jsonrpc.ServerProxy(corenlp.jsonrpc.JsonRpc20(), transport)
        self._restartServer()
        self.lock = threading.Lock()

    def _restartServer(self):        
        # Kill old processes serving at our port:
        for pid in process.getServerPIDs(self.SERVER_PORT):
            os.kill(pid, signal.SIGKILL)
        
        spin = [True]
        def handler(signum, stack):
            spin[0] = False
        signal.signal(signal.SIGUSR1, handler)
        
        # Create new server at that port:
        if os.fork() == 0:
            server = corenlp.corenlp.startServer(self.cnlpPath, self.cnlpVersion, self.SERVER_HOST, self.SERVER_PORT)
            os.kill(os.getppid(), signal.SIGUSR1)
            server.serve()
        else:
            while spin[0]: time.sleep(2)
            time.sleep(5) # just to be safe
        
        # The multithreaded version of the above code (not way to kill a thread though):
        '''self.serverThread = threading.Thread(target=self.server.serve)
        self.serverThread.setDaemon(True)
        self.serverThread.start()'''
    
    def _processResult(self, parser, text):
        def errorOcurred(result):
            if result is None:
                return True
            elif isinstance(result, tuple):
                for item in result:
                    if item is None:
                        return True
            return False
        
        self.lock.acquire()
        result = parser(text)
        if errorOcurred(result):
            self.consecutiveErrorCount += 1
        else:
            self.consecutiveErrorCount = 0
        if self.consecutiveErrorCount >= self.CONSECUTIVE_ERROR_THRESHOLD:
            self._restartServer()
            self.consecutiveErrorCount = 0
            result = parser(text)
        self.lock.release()
        return result

    def extractSentences(self, text):
        return self._processResult(lambda text: _extractSentences(self.__rawParse(text)), text)

    def extractSyntacticParseTrees(self, text):
        return self._processResult(lambda text: _extractSyntacticParseTrees(self.__rawParse(text)), text)

    def extractCoref(self, text):
        return self._processResult(lambda text: _extractCoref(self.__rawParse(text)), text)

    def parse(self, text):
        return self._processResult(lambda text: _parse(_rawParseWithProxy(text, self.proxy)), text)
