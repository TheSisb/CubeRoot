#!/usr/bin/env python

import cgi
import cgitb
import os.path, sys, getopt, re
import src.InvertedIndex as ii
import src.Tokeniser as tk
import src.WebIndexer as wi
import src.VectorSpace as vs
import src.SpellingCorrector as sc

print "Content-type: text/html"
print

# form stuff
# flag1 = form.getValue('flag1', 'False')

index = ii.InvertedIndex()
indexer = wi.WebIndexer()
tokeniser = tk.Tokeniser()
indexer.spimi(index, tokeniser)

vSpace = vs.VectorSpace(index, indexer)
vSpace.buildVectors()

k = 3
w, u, rss = vSpace.kMeans(k)

print pimp
