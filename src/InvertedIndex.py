#!/usr/bin/env python

"""InvertedIndex.py

Inverted index implemented as a dictionary (hash table) using the term as the
key, and a list of 2-value lists as the value:
    { term : [ [docId, termFreq], [docId, termFreq], ... ], ... }

Overrides the __setitem__ method to manage the postings list using regular inserts.

Includes functionality to save to, and load from, a csv file.
"""

import csv

def merge(left, right):
    """ Merge two sorted lists without duplicates
        and combine term frequency """
    result = []
    i, j = 0, 0
    # Typical merge algorithm from merge-sort
    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            result.append(left[i])
            i += 1
        elif left[i][0] > right[j][0]:
            result.append(right[j])
            j += 1
        else:               # Combine term frequency
            result.append( [ left[i][0], left[i][1]+right[j][1] ] )
            i += 1
            j += 1
    result += left[i:]      # Insert rest of left list  OR
    result += right[j:]     # insert rest of right list
    return result

class InvertedIndex(dict):

    def __setitem__(self, key, value):
        """ Overides = operator: set new list or append new docId """
        if isinstance(value, int):
            if key not in self:
                # New term & new document
                dict.__setitem__( self, key, [ [value, 1] ] )
            elif value > self[key][-1][0]:
                # New document
                self[key].append( [value, 1] )
            elif value == self[key][-1][0]:
                # Old document: increment term frequency
                self[key][-1][1] += 1
            else:
                raise TypeError("InvertedIndex postings must be ordered")
        elif isinstance(value, list):
            # Set new postings list for this term
            dict.__setitem__(self, key, value)
        else:
            raise TypeError("InvertedIndex value must be an 'int', or a list")

    def totalFreq(self, term):
        count = 0
        for entry in self[term]:
            count += entry[1]
        return count

    def frequencies(self):
        index = {}
        for term in self:
            index[term] = self.totalFreq(term)
        return index

    def tf(self, term, docId):
        """ Return the term frequency for a given term and docId """
        if not self[term]:
            return 0
        lo = 0
        hi = len(self[term])
        while lo < hi:
            mid = (lo+hi)//2
            midval = self[term][mid][0]
            if midval < docId:
                lo = mid+1
            elif midval > docId:
                hi = mid
            else:
                return self[term][mid][1]
        return 0

    def df(self, term):
        """ Return the document frequency for a given term """
        if self[term]:
            return len(self[term])
        else:
            return 0

# I/O 

def save(savefile, index):
    """ Saves the inverted index as a CSV
    Inspired by: http://www.doughellmann.com/PyMOTW/csv/#using-field-names
    """
    try:
        f = open(savefile, 'wb')
        fields = ('term', 'posting')
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(dict((n,n) for n in fields))
        for key in index:
            # Convert postings list to a string: "docId1:termFreq1,docId2:termFreq2..."
            posting = ','.join( [ ':'.join( [ str(i) for i in doc ] ) for doc in index[key] ] )
            writer.writerow( { fields[0]:key, fields[1]:posting } )
    finally:
        f.close()

def load(loadfile, index):
    """ loads an inverted index from a CSV file
    Inspired by: http://www.doughellmann.com/PyMOTW/csv/#using-field-names
    """
    index.clear()
    try:
        f = open(loadfile, 'rb')
        reader = csv.DictReader(f)
        for row in reader:
            # Convert from string to postings list
            index[row['term']] = [ [ int(i) for i in doc.split(':') ] for doc in row['posting'].split(',') ]
    finally:
        f.close()

# MERGE

def mergeIndex(left, right):
    """ Returns a single merge inverted index from two indexes """
    for key in right:
        if key in left:
            left[key] = merge(left[key], right[key])
        else:
            left[key] = right[key]
    return left

def mergeFile(mergedFile, fileList):
    """
    Final merge for index construction algorithm.
    From a list of partial indexes saved as csv files, merge all
    the files and save the resulting index to mergedfile.
    """
    largeIndex = InvertedIndex()
    smallIndex = InvertedIndex()
    # Trivial merge because I can't find a way to merge the hash
    # without loading everything into memory.
    if fileList:
        for n in range(0, len(fileList)):
            load(fileList[n], smallIndex)
            largeIndex = mergeIndex(largeIndex, smallIndex)
            smallIndex.clear()
    save(mergedFile, largeIndex)
