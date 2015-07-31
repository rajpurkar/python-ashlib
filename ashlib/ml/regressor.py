import os
import sys
import math

import learner

import sklearn.svm
import sklearn.linear_model

## Regressor ############################################################

class Regressor(learner.SupervisedLearner):

    def __init__(self):
        raise NotImplementedError("Not implemented")

    def train(self, objects, goldValues):
        raise NotImplementedError("Not implemented")

    def predict(self, object):
        raise NotImplementedError("Not implemented")

    def featurize(self, object):
        raise NotImplementedError("Not implemented")

    def evaluate(self, objects, goldValues):
        meanSquaredError = 0.0
        for index, object in enumerate(objects):
            prediction = self.predict(object)
            gold = goldValues[index]
            residual = prediction - gold
            meanSquaredError += math.pow(residual, 2.0)
        if len(objects) > 0:
            meanSquaredError /= len(objects)
        return meanSquaredError

## SupportVectorRegressor ###############################################

class SupportVectorRegressor(Regressor, learner.SupportVectorMachine):

    def __init__(self):
        self.svm = sklearn.svm.SVR()

## LinearRegressor ######################################################

class LinearRegressor(learner.SKLearner):

    def __init__(self):
        self.lr = sklearn.linear_model.LinearRegression()

    def train(self, objects, values):
        self.lr.fit(self.featureMatrix(objects), values)

    def predict(self, object):
        return self.svr.predict(self.featurize(object))
