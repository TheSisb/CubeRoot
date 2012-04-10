#!/usr/bin/env python

"""Tokeniser.py

String parser used in information retrieval to tokenise documents and queries.
Performs the following lossy compression on the dictionary:
    - Case folding
    - Number removal
    - Stemming
    - Stop word removal

Tokeniser.tokenise(string) parses string and returns a list of tokens.

Class structure inspired by:
    http://blog.josephwilk.net/projects/
      building-a-vector-space-search-engine-in-python.html
"""

import re
import PorterStemmer as ps

class Tokeniser:
    numberFilter = True
    caseFolding  = True
    stopWords = []
    stemmer = None
    
    def __init__(self, stopList='cornell.stop',
                 useNumberFilter=True, useCaseFolding=True,
                 useStopList=True, useStemming=True):
        """ Tokeniser constructor
        Optionally specify a stopword list:
            - 'google.stop' : 61  words
              (From Google's search stop words, plus single letters)
            - 'cornell.stop': 572 words
              (From ftp://ftp.cs.cornell.edu/pub/smart/english.stop)
        """
        self.numberFilter = useNumberFilter
        self.caseFolding  = useCaseFolding
        if useStopList:
            try:
                f = open(stopList, 'rb')
                self.stopWords = sorted( f.read().split() )
            finally:
                f.close()
        if useStemming:
            self.stemmer = ps.PorterStemmer()
        
    def filterStopWords(self, term, lo=0, hi=None):
        """ binary search used to filter stopwords """
        if hi is None:
            hi = len(self.stopWords)
        while lo < hi:
            mid = (lo+hi)//2
            midval = self.stopWords[mid]
            if midval < term:
                lo = mid+1
            elif midval > term:
                hi = mid
            else:
                return False
        return True

    def tokenise(self, string):
        """ Find all terms, case fold, remove stop words, and stem """
        regexTerm = None

        # Number Filtering
        if self.numberFilter:
            regexTerm = re.compile(r'\b[a-zA-Z]+\b')
        else:
            regexTerm = re.compile(r'\b[a-zA-Z0-9]+\b')
        terms = regexTerm.findall(string)

        # Case Folding
        if self.caseFolding:
            terms = [term.lower() for term in terms]

        # Stop word removal
        terms = filter(self.filterStopWords, terms)

        # Stemming
        if self.stemmer is not None:
            terms = [ self.stemmer.stem(term, 0, len(term)-1) for term in terms ]

        return terms
