#!/usr/bin/python

import cgi
import cgitb
import sys, os, pickle
import src.InvertedIndex as ii
import src.WebIndexer as wi
import src.VectorSpace as vs

print "Content-type: text/html"
print

index = ii.InvertedIndex()
ii.load("index/fullindex.csv", index)
indexer = wi.WebIndexer()
indexer.load()
    
vSpace = vs.VectorSpace(index, indexer)
vSpace.buildVectors()

minK = 2
maxK = 15
n = 2

results = []
if not os.path.exists("index/kmeans"):
    for k in range(minK, maxK+1):
        print k
        w, u, rss = vSpace.kMeansBestOfN(k, n*k)
        results.append(rss)
    pickle.dump(results, open("index/kmeans", "wb"))
else:
    results = pickle.load(open("index/kmeans", "rb"))
    
print '{\n'
for i in range(minK, maxK+1):
    sys.stdout.write('\t"'+str(i)+'" : '+str(results[i-minK]))
    if i != (maxK):
        print ','
print '\n}' 
