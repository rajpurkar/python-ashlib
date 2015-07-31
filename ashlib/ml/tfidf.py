import os
import sys
import math
import collections

import language.processor
import util.vector

## TFIDFCalculator #########################################################################################

class TFIDFCalculator():

    TYPE_TF_IDF = "tf*idf"
    TYPE_TF_ULMC = "tf*unigram_language_model_cost"

    def __init__(self, type, corpus, weights={}):
        ''' |corpus| should be a list of lists of words,
            and must be supplied if using type tf*idf. '''

        ''' |weights| should be a dictionary of words
            to floats, and is optional no regardless of
            the standard metric being used. Words with
            not associated values are assumed to have
            weight 1. '''

        if not type == self.TYPE_TF_IDF and not type == self.TYPE_TF_ULMC:
            raise Exception("Invalid type specified.")

        self.type = type
        self.corpus = corpus
        self.corpusSize = len(corpus)
        self.languageProcessor = language.processor.LanguageProcessor()
        self.weights = weights

        self.documentFrequencies = collections.Counter()
        for document in corpus:
            words = set(document)
            for word in words:
                self.documentFrequencies[word] += 1

        self.cache = {}

    def normalizedTermFrequencyVector(self, sentence):
        # |sentence| should be a list of words.

        vector = {}

        # Count occurrences
        for word in sentence:
            if word in vector:
                vector[word] += 1.0
            else:
                vector[word] = 1.0

        # Normalize
        for word in vector:
            vector[word] /= float(len(sentence))

        return vector

    def inverseDocumentFrequency(self, word):
        documentFrequency = self.documentFrequencies[word]
        idf = 1.0
        if documentFrequency > 0.0:
            idf += math.log(self.corpusSize / documentFrequency)
        return idf

    def inverseDocumentFrequencyVector(self, sentence):
        # |sentence| should be a list of words
        vector = {}
        for word in sentence:
            vector[word] = self.inverseDocumentFrequency(word)
        return vector

    def unigramLanguageModelCostVector(self, sentence):
        # |sentence| should be a list of words
        vector = {}
        for word in sentence:
            vector[word] = math.cos(self.languageProcessor.languageModel.unigramProb(word) * (math.pi / 2.0))
        return vector

    def tfidfVector(self, sentence):
        tfVector = self.normalizedTermFrequencyVector(sentence)
        idfVector = self.inverseDocumentFrequencyVector(sentence)
        return util.vector.product(util.vector.product(tfVector, idfVector), self.weights, default=1.0)

    def tfulmcVector(self, sentence):
        tfVector = self.normalizedTermFrequencyVector(sentence)
        ulmcVector = self.unigramLanguageModelCostVector(sentence)
        return util.vector.product(util.vector.product(tfVector, ulmcVector), self.weights, default=1.0)

    def cosineSimilarity(self, query, referenceIndex, intersectionOnly=True):
        query = self.languageProcessor.removeStopWords(query)
        reference = self.languageProcessor.removeStopWords(self.corpus[referenceIndex])

        if intersectionOnly:
            # We modify the reference so that it only
            # contains words in the query.
            modifiedReference = []
            for word in reference:
                if word in query:
                    modifiedReference += [word]
            reference = modifiedReference

        if self.type == self.TYPE_TF_IDF:
            queryVector = self.tfidfVector(query)
            referenceVector = self.tfidfVector(reference)
        elif self.type == self.TYPE_TF_ULMC:
            queryVector = self.tfulmcVector(query)
            referenceVector = self.tfulmcVector(reference)

        if util.vector.modulus(queryVector) == 0 or util.vector.modulus(referenceVector) == 0:
            return 0.0
        else:
            return util.vector.cosine(queryVector, referenceVector)

    def angleSimilarity(self, query, referenceIndex, intersectionOnly=True):
        cos = self.cosineSimilarity(query, referenceIndex, intersectionOnly)
        if cos < -1.0: cos = -1.0
        if cos > 1.0: cos = 1.0
        return math.acos(cos)

    def cosineSimilarityBetweenReferences(self, firstReferenceIndex, secondReferenceIndex):
        query = self.languageProcessor.removeStopWords(self.corpus[firstReferenceIndex])
        reference = self.languageProcessor.removeStopWords(self.corpus[secondReferenceIndex])

        if firstReferenceIndex in self.cache:
            queryVector = self.cache[firstReferenceIndex]
        else:
            queryVector = self.tfidfVector(query)
            self.cache[firstReferenceIndex] = queryVector

        if secondReferenceIndex in self.cache:
            referenceVector = self.cache[secondReferenceIndex]
        else:
            referenceVector = self.tfidfVector(reference)
            self.cache[secondReferenceIndex] = referenceVector

        if util.vector.modulus(queryVector) == 0 or util.vector.modulus(referenceVector) == 0: cos = 0.0
        else: cos = util.vector.cosine(queryVector, referenceVector)
        if cos < -1.0: cos = -1.0
        if cos > 1.0: cos = 1.0
        return cos

    def cosineMatrix(self):
        matrix = []
        for index1, document1 in enumerate(self.corpus):
            matrix.append([])
            for index2, document2 in enumerate(self.corpus):
                matrix[-1].append(self.cosineSimilarity(index1, index2))
        return matrix
