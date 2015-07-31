import os
import sys
import math

## SupervisedLearner ############################################################

class SupervisedLearner(object):
    
    def __init__(self):
        raise NotImplementedError("Subclasses should override.")
    
    def train(self, objects, values):
        raise NotImplementedError("Subclasses should override.")
    
    def predict(self, object):
        raise NotImplementedError("Subclasses should override.")
    
    def featurize(self, object):
        raise NotImplementedError("Subclasses should override.")

## SKLearner ####################################################################

class SKLearner(SupervisedLearner):

    def __init__(self):
        raise NotImplementedError("Subclasses should override.")

    def featureMatrix(self, objects):
        featureMatrix = []
        for object in objects:
            featureMatrix.append(self.featurize(object))
        return featureMatrix

    def addBooleanFeature(self, features, condition):
        features.append(1 if condition else 0)

## SupportVectorMachine #########################################################

class SupportVectorMachine(SKLearner):
    
    def __init__(self):
        raise NotImplementedError("Subclasses should override to set |self.svm|.")
    
    def train(self, objects, values):
        self.svm.fit(self.featureMatrix(objects), values)
    
    def predict(self, object):
        return self.svm.predict(self.featurize(object))[0]
