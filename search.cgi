#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(display=0, logdir="/var/log/cgi-logs/")
import os.path, sys, getopt, re
import src.InvertedIndex as ii
import src.Tokeniser as tk
import src.WebIndexer as wi
import src.VectorSpace as vs
import src.SpellingCorrector as sc

print "Content-type: text/html"
print

form = cgi.FieldStorage()
userInput = form.getvalue("searchQuery", "")

if (userInput != ""):	
	# Sample: Loading the index (don't need to if you just indexed, see above)
    	index = ii.InvertedIndex()
    	ii.load("index/fullindex.csv", index)
    	indexer = wi.WebIndexer()
    	indexer.load()
    	
	# Sample: Generating the vector space
    	vSpace = vs.VectorSpace(index, indexer)
    	vSpace.buildVectors()

	k = 8
	n = 10
	w, u, rss = vSpace.kMeansBestOfN(k, n)

	tokeniser = tk.Tokeniser()

	numberOfResults = 10

	terms = tokeniser.tokenise(userInput)
	terms = [sc.correct(term) for term in terms]

	queryVector = vSpace.buildQueryVector(terms)

	closestCluster = vSpace.nearestCluster(w, u, queryVector)

	docList = vSpace.cosineSort(range(len(vSpace.vectorIndex)), closestCluster, queryVector)[:numberOfResults]

	urlList = [indexer.urls[docId] for docId in docList]

	print '{\n'
	for i in range(len(urlList)):
		sys.stdout.write( '\t"' + str(i+1) + '" : "' + urlList[i] + '"')
		if i != (len(urlList) -1):
			print ','
	print '\n}'
