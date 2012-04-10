#!/usr/bin/python

import os.path, sys, getopt, re
import src.InvertedIndex as ii
import src.Tokeniser as tk
import src.WebIndexer as wi
import src.VectorSpace as vs
import src.SpellingCorrector as sc

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    """
    # Sample: Indexing the collection
    index = ii.InvertedIndex()
    indexer = wi.WebIndexer()
    tokeniser = tk.Tokeniser()
    indexer.spimi(index, tokeniser)
    """
    # Sample: Loading the index (don't need to if you just indexed, see above)
    index = ii.InvertedIndex()
    ii.load("index/fullindex.csv", index)
    indexer = wi.WebIndexer()
    indexer.load()
    
    # Sample: Generating the vector space
    vSpace = vs.VectorSpace(index, indexer)
    vSpace.buildVectors()
    
    # Sample: Simple K-means
    """
    k = 3
    # w: List of K clusters [ [docId, docId, ...], [docId, docId, ...], [docId, docId, ...] ]
    # u: List of K centroids [ vSpace.centroid(w[0]), ..., vSpace.centroid(w[k-1]) ]
    # rss: total RSS value for this clustering scheme
    w, u, rss = vSpace.kMeans(k)
    """
    # Sample: K-means with the smallest RSS using N different seeds
    k = 8
    n = 1
    w, u, rss = vSpace.kMeansBestOfN(k, n)

    # Sample: Tokenise input
    tokeniser = tk.Tokeniser()
    userInput = raw_input("> ").strip()
    terms = tokeniser.tokenise(userInput)
    print terms

    # Sample: Edit distance
    terms = [sc.correct(term) for term in terms]
    print terms

    queryVector = vSpace.buildQueryVector(terms)
    docList = vSpace.nearestCluster(w, u, queryVector)

    # Sample: getting a list of URLs from a list of doc IDs
    urlList = [indexer.urls[docId] for docId in docList]

    count = 1
    for url in urlList:
        print count, ":", url
        count += 1

if __name__ == "__main__":
    sys.exit(main())
