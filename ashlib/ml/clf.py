import os
import sys
import math

import sklearn.svm
import sklearn.linear_model

sys.path.insert(0, ".")
import util.maths

## Classifier ##############################################################

class Classifier(object):

    def __init__(self):
        raise NotImplementedError("Sublasses should override.")

    def train(self, objects, goldLabels):
        raise NotImplementedError("Sublasses should override.")

    def classify(self, object):
        raise NotImplementedError("Sublasses should override.")

    def confidence(self, object, label):
        raise NotImplementedError("Sublasses should override.")

    def featurize(self, object):
        raise NotImplementedError("Sublasses should override.")

    def accuracy(self, objects, goldLabels):
        if len(objects) == 0 or len(objects) != len(goldLabels):
            raise Exception("Malformed data")

        numCorrect = 0
        for index, object in enumerate(objects):
            if self.classify(object) == goldLabels[index]:
                numCorrect += 1
        return float(numCorrect) / float(len(objects))
                
    '''def f1(self, objects, goldLabels):
        if len(objects) == 0 or len(objects) != len(goldLabels):
            raise Exception("Malformed data")

        tp = fp = fn = 0.0
        
        for index, object in enumerate(objects):
            predicted = self.classify(object)
            gold = goldLabels[index]
            if predicted and gold: tp += 1.0
            elif predicted and (not gold): fp += 1.0
            elif (not predicted) and gold: fn += 1.0
        
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        return util.maths.hmean(precision, recall)'''

    def tuneHyperparameters(self, hyperparameters, trainObjects, trainLabels, tuneObjects, tuneLabels):
        raise NotImplementedError("Not implemented yet.")

## SKLearnClassifier ###################################################

class SKLearnClassifier(Classifier):
    
    def __init__(self):
        self.clf = None
    
    def train(self, objects, labels):
        self.clf.fit(self.featureMatrix(objects), labels)
    
    def featureMatrix(self, objects):
        return self.densify(self.featurize(object) for object in objects)

    def densify(self, featureVectors, default=0):
        matrix = []
        featureMap = {}
        for vector in featureVectors:
            dense = [default] * len(featureMap)
            for featureName in vector:
                if featureName in featureMap:
                    dense[featureMap[featureName]] = vector[featureName]
                else:
                    featureMap[featureName] = len(featureMap)
                    for otherVector in matrix:
                        otherVector.append(default)
            matrix.append(dense)
        return matrix

## SupportVectorMachine #################################################

class SupportVectorMachine(SKLearnClassifier):
    
    def __init__(self, C=1.0):
        self.clf = sklearn.svm.SVC(C=C)
    
    def classify(self, object):
        return self.clf.predict(self.featurize(object))[0]

## LogisticRegressor ####################################################

class LogisticRegressor(Classifier):

    def __init__(self):
        self.clf = sklearn.linear_model.LogisticRegression()

    def classify(self, object):
        return self.clf.predict(self.featurize(object))[0]
