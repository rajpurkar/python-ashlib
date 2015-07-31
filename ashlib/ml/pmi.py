import sys
import os
import collections

class PMICalculator():

    def __init__(self):
        self.labelCounts = None
        self.wordCounts = None
        self.jointCounts = None
        self.numPairs = None

    def train(self, corpus, smoothingFactor = 0.0):
        self.labelCounts = collections.defaultdict(lambda: smoothingFactor)
        self.wordCounts = collections.defaultdict(lambda: smoothingFactor)
        self.jointCounts = collections.defaultdict(lambda: collections.defaultdict(lambda: smoothingFactor))
        self.numPairs = 0

        for label, document in corpus:
            for word in document:
                weight = 1.0
                self.labelCounts[label] += 1
                self.wordCounts[word] += 1
                self.jointCounts[label][word] += 1
                self.numPairs += 1

    def keySet(self, label):
        return self.jointCounts[label].keys()

    def pmi(self, label, word):
        jointProb = float(self.jointCounts[label][word]) / float(self.numPairs)
        labelProb = float(self.labelCounts[label]) / float(self.numPairs)
        wordProb = float(self.wordCounts[word]) / float(self.numPairs)
        return jointProb / (labelProb * wordProb)

    def count(self, word):
        return self.wordCounts[word]

def main():
	pass

if __name__ == "__main__":
    main()
