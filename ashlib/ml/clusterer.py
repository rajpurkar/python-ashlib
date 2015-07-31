import os
import sys
import math
import random
import copy
import collections

import util.vector

## Clusterer ###########################################################################################

class Clusterer(object):

    def __init__(self, textProcessor):
        raise NotImplementedError("Subclass should override")

    def cluster(self, points, numClusters):
        raise NotImplementedError("Subclass should override")

    def assignments(self, points, numClusters):
        return self.assignmentsFromClusters(points, self.cluster(points, numClusters, formatData=False), formatData=False)
    
    def assignmentsFromClusters(self, points, indexClusters):
        raise NotImplementedError("Not implemented")
    
    def centroids(self, points, numClusters):
        return self.centroidsFromClusters(points, self.cluster(points, numClusters, formatData=False), formatData=False)
    
    def centroidsFromClusters(self, points, indexClusters):
        pointClusters = []
        for cluster in indexClusters:
            pointClusters.append([points[index] for index in cluster])
        return [self.optimalCentroid(cluster) for cluster in pointClusters]

## KmeansClusterer ######################################################################################

class KmeansClusterer(Clusterer):

    MAX_NUM_ITERATIONS = 50

    def __init__(self):
        raise NotImplementedError("Subclass should override")

    def cluster(self, points, numClusters, formatData=True):
        if formatData: points = self.formatData(points)

        numPoints = len(points)
        numClusters = min(numPoints, numClusters)

        initialCentroidIndices = random.sample(range(numPoints), numClusters)
        centroids = [points[index] for index in initialCentroidIndices]

        for iteration in range(self.MAX_NUM_ITERATIONS):
            clusters = self.optimalClusters(points, centroids)
            previousCentroids = centroids[:]

            for clusterIndex, cluster in enumerate(clusters):
                # we won't update the centroid if there are no points in its cluster
                if len(cluster) > 0.0:
                    centroids[clusterIndex] = self.optimalCentroid([points[pointIndex] for pointIndex in cluster])

            if centroids == previousCentroids: # convergence
                break

        return clusters
    
    def optimalClusters(self, points, centroids):
        raise NotImplementedError("Subclass should override")

    def optimalCentroid(self, cluster):
        raise NotImplementedError("Subclass should override")

## ReconstructionKmeans ###############################################################################

class ReconstructionKmeansClusterer(KmeansClusterer):

    def __init__(self):
        pass
    
    def optimalClusters(self, points, centroids):
        clusters = [[] for index in range(len(centroids))]
        for index, point in enumerate(points):
            errors = [self.loss(point, centroid, []) for centroid in centroids]
            clusters[errors.index(min(errors))].append(index)
        return clusters

    def loss(self, point, centroid, clusteredPoints):
        return mymath.vector.squaredDistance(point, centroid)
    
    def optimalCentroid(self, cluster):
        return mymath.vector.average(cluster)

## CohesionKmeans #####################################################################################

class CohesionKmeans(KmeansClusterer):

    def __init__(self):
        pass

    def optimalClusters(self, points, centroids):
        if not self.greedy: return super(HeatMapClusterer, self).optimalClusters(points, centroids)
        
        # Greedy search:
        
        points = points[:] # deep copy
        clusters = [[]] * len(centroids)
        
        usedPointIndices = set()
        
        for iteration in range(len(points)):
            errors = []
            for pointIndex, point in enumerate(points):
                if not pointIndex in usedPointIndices:
                    pointErrors = []
                    for clusterIndex, centroid in enumerate(centroids):
                        cluster = clusters[clusterIndex]
                        clusteredPoints = [points[pointIndex] for pointIndex in cluster]
                        pointErrors.append(self.loss(point, centroid, clusteredPoints))
                    minError = min(pointErrors)
                    errors.append((pointIndex, minError, pointErrors.index(minError)))
        
            pointIndex, minError, centroidIndex = min(errors, key=lambda triple: triple[1])
            clusters[centroidIndex].append(pointIndex)
            
            usedPointIndices.add(pointIndex)
    
        return clusters
    
    def loss(self, point, centroid, clusteredPoints):
        if not self.greedy: return super(HeatMapClusterer, self).loss(point, centroid, clusteredPoints)
        
        # Basic loss:
        loss = mymath.vector.squaredDistance(point, centroid) * math.pow(self.intensity(point), 2.0)
        
        # Calculating loss based on radial grid:
        
        point = mymath.point.Point.difference(point, centroid)
        
        bucketCounts = []
        
        for otherPoint in clusteredPoints:
            otherPoint = mymath.point.Point.difference(otherPoint, centroid)
            
            if mymath.point.Point.withinSector(point, otherPoint, self.numRadialSectors): ## currently allows for any orientation of sectors
                bucketIndex = int(otherPoint.r / self.radialBucketWidth)
                
                if bucketIndex >= len(bucketCounts):
                    bucketCounts += [0] * (bucketIndex - len(bucketCounts) + 1)
                
                bucketCounts[bucketIndex] += 1
    
        pointBucketIndex = int(point.r / self.radialBucketWidth)
        for bucketIndex in range(pointBucketIndex):
            if bucketIndex >= len(bucketCounts) or bucketCounts[bucketIndex] == 0:
                loss *= 2.0
                
        return loss

    def optimalCentroid(self, cluster):
        intensities = [math.pow(self.intensity(point), 2.0) for point in cluster]
        return mymath.point.Point.fromDict(mymath.vector.weightedAverage(cluster, intensities))
