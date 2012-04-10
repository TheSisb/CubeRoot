#!/usr/bin/env python

from numpy import * #http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
import math, random
import InvertedIndex as ii
import WebIndexer as wi

L = 10

def vectorLength(v):
    return (sum(v**2.0))**0.5
    
def distance(v1, v2):
    return vectorLength(v1 - v2)

def cosine(v1, v2):
    return dot(v1, v2)/(vectorLength(v1)*vectorLength(v2)+1)

def termCount(terms):
    termDict = {}
    for term in terms:
        if term not in termDict:
            termDict[term] = 1
        else:
            termDict[term] += 1
    return termDict

class VectorSpace:
    index = None
    indexer = None
    vectorIndex = None
    numberOfTerms = 0
    numberOfDocs = 0
    
    def __init__(self, iIndex, iIndexer):
        self.index = iIndex
        self.indexer = iIndexer
        self.numberOfTerms = len(self.index)
        self.numberOfDocs = len(self.indexer.docL)
    
    def computeIDF(self, term):
        df = self.index.df(term)
        return math.log( (float(self.numberOfDocs)/df), 10 )

    def buildVectors(self):
        # iterate the index and swap 0 to tfidf where applicable
        self.vectorIndex = zeros( (self.numberOfDocs, self.numberOfTerms) )
        pos = 0
        for term in self.index: #this gives "ball"
            idf = self.computeIDF(term)
            for entry in self.index[term]: #this gives [ [25, 1], [587, 6], .... ]
                self.vectorIndex[entry[0], pos] = entry[1]*idf
            pos += 1
            
    def buildQueryVector(self, terms):
        termDict = termCount(terms)
        vector = zeros( self.numberOfTerms )
        # Returns empty vector if query is empty
        #if not termDict:
        #    return vector
        pos = 0
        for term in self.index:
            if term in termDict:
                vector[pos] = termDict[term]*self.computeIDF(term)
            pos += 1
        return vector

    def length(self, vectorID):
        return vectorLength(self.vectorIndex[vectorID])

    def centroid(self, listOfIDs):
        c = zeros( (self.numberOfTerms) )
        for docId in listOfIDs:
            c = add(c, self.vectorIndex[docId])
        c = c / len(listOfIDs)
        return c

    def randomSeed(self, k):
        w = []
        # Initialize random class lists
        for i in range(k):
            w.append([])
        for docId in self.indexer.docL.keys():
            w[random.randrange(0,k)].append(docId)
        return w

    def calculateClassRSS(self, v, c):
        """v: list of docIds in the class; c: centroid for the class"""
        rss = 0.0
        for docId in v:
            rss += sum( (c - self.vectorIndex[docId])**2.0 )
        return rss

    def calculateRSS(self, w, u):
        """w: list of classes; u: list of centroids"""
        result = 0.0
        for k in range(len(w)):
            result += self.calculateClassRSS(w[k], u[k])
        return result

    def kMeans(self, k):
        # Initial seed and centroid
        w = self.randomSeed(k)
        u = []
        for i in range(k):
            u.append(self.centroid(w[i]))
        thisRSS = self.calculateRSS(w, u)
        prevRSS = 0
        while thisRSS != prevRSS:
            # Set each doc to the class with the nearest centroid
            for i in range(k):
                w[i] = []
            for docId in self.indexer.docL.keys():
                # distances from current docId to all centroids
                distances = [ distance(u[i], self.vectorIndex[docId]) for i in range(k) ]
                j = min(xrange(k), key=distances.__getitem__)
                w[j].append(docId)
            # Calculate the new centroids and RSS
            for i in range(k):
                u[i] = self.centroid(w[i])
            prevRSS = thisRSS
            thisRSS = self.calculateRSS(w, u)
        return w, u, thisRSS

    def kMeansBestOfN(self, k, n):
        rss = 0
        w = u = []
        for i in range(n):
            thisW, thisU, thisRSS = self.kMeans(k)
            if thisRSS < rss or rss == 0:
                rss = thisRSS
                w = thisW
                u = thisU
        return w, u, rss

    def nearestCluster(self, w, u, vector):
        distances = [ distance(u[i], vector) for i in range(len(u)) ]
        j = min(xrange(len(u)), key=distances.__getitem__)
        return w[j]
    
    def queryCosine(self, queryVector, docId, closestCluster):
        if docId in closestCluster:
            return 1.2*cosine(queryVector, self.vectorIndex[docId])
        return cosine(queryVector, self.vectorIndex[docId])

    def cosineSort(self, idList, closestCluster, queryVector):
        return sorted(idList, key=lambda x: self.queryCosine(queryVector, x, closestCluster), reverse=True)
