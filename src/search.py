#!/usr/bin/python

"""
NAME:
    search.py - a command-line query tool for information retrieval

SYNOPSIS:
    python search.py [OPTIONS]

DESCRIPTION:
    -h, --help
        display a description of different options (this prompt)

    -i, --index
        force a complete reconstruction of the index (this can take a long time)

    -n, --noquery
        does not enter query interface, enables --index

    -b, --blocksize=SIZE
        specify a block SIZE in number of files (2 by default), enables --index

    -f, --folder=FOLDER
        specify a folder containing .sgm file (reuters21578 by default), enables --index

    -s, --stopwords=LISTFILE
        specify a file containing stop words (cornell.stop by default) one on each line, enables --index

    -d, --nodigitfilter
        disable number filtering, enables --index

    -c, --nocasefolding
        disables case folding, enables --index

    -t, --nostemming
        disables stemming, enables --index

    -w, --nostopwords
        disables stopwords (equivalent to --stopwords=''), enables --index

AUTHOR:
    Written by Marc-Andre Faucher
"""

import os.path, sys, getopt, re
import InvertedIndex as ii
import Tokeniser as tk
import ReuterIndexer as ri
import OkapiRanking as ok

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    # Default values
    reconstruct = False         # --index
    query = True                # --noquery
    blocksize = 2               # --blocksize=
    stopwords = "cornell.stop"  # --stopwords= ; --nostopwords
    docfolder = "reuters21578"  # --folder=
    usenumberfilter = True      # --nodigitfilter
    usecasefolding  = True      # --nocasefolding
    usestemming     = True      # --nostemming

    k = 1.2
    b = 2.0

    if argv is None:
        argv = sys.argv
    try:
        # Parse command line options
        try:
            opts, args = getopt.getopt( argv[1:], "hinb:f:s:dctw",
                                        ["help", "index", "noquery",
                                         "blocksize=", "folder=", "stopwords=",
                                         "nodigitfilter", "nocasefolding",
                                         "nostemming", "nostopwords"] )
        except getopt.error, msg:
            raise Usage(msg)
        # Process options
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print __doc__
                sys.exit(0)
            if opt in ("-i", "--index"):
                reconstruct = True
            if opt in ("-n", "--noquery"):
                query = False
                reconstruct = True
            if opt in ("-b", "--blocksize"):
                blocksize = int(arg)
                reconstruct = True
            if opt in ("-f", "--folder"):
                docfolder = arg
                reconstruct = True
            if opt in ("-s", "--stopwords"):
                stopwords = arg
                reconstruct = True
            if opt in ("-d", "--nodigitfilter"):
                usenumberfilter = False
                reconstruct = True
            if opt in ("-c", "--nocasefolding"):
                usecasefolding = False
                reconstruct = True
            if opt in ("-t", "--nostemming"):
                usestemming = False
                reconstruct = True
            if opt in ("-w", "--nostopwords"):
                stopwords = ''
                reconstruct = True
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    # Index construction
    index       = ii.InvertedIndex()
    indexer     = ri.ReuterIndexer(folder=docfolder, blockSize=blocksize)
    tokeniser   = tk.Tokeniser(stopList=stopwords, useNumberFilter=usenumberfilter, 
                               useCaseFolding=usecasefolding, useStemming=usestemming)
    
    if reconstruct:
        print "Building inverted index..."
        indexer.spimi(index, tokeniser)
        ri.save("index/doclength.csv", indexer.docL)
    else:
        print "Loading inverted index..."
        ii.load("index/fullindex.csv", index)
        ri.load("index/doclength.csv", indexer.docL)

    if not query:
        return 0
    
    bm25        = ok.OkapiRanking(index, indexer)
    rsvK = 1.2
    rsvB = 0.75
    topN = 10

    # Start of query loop
    helpString = """
    Enter a search query below:
                    
    <digit> : Display document with given ID
          p : Display all results
          k : Change the value of 'k' constant
          b : Change the value of 'b' constant
          n : Change the number of documents to print (top n)
          h : Help (display this text)
          q : Quit"""

    print helpString
    userInput = ""
    lastResults = None

    while (userInput != "q"):
        try:
            userInput = raw_input("> ").strip()

            # Process options
            if userInput == 'q':                # Exit
                pass
            elif userInput == '':               # None
                print "Enter 'h' for help; 'q' to exit."
            elif userInput == 'h':              # Help
                print helpString
            elif re.match(r'\d+', userInput):   # Print document
                indexer.display(int(userInput), folder=docfolder)
            elif userInput == 'p':              # Print results
                if lastResults is not None:
                    for i in range(topN):
                        print i+1, "- Document", str(lastResults[i])
                        indexer.display(lastResults[i], folder=docfolder)
                else:
                    print "You must make a query before printing the results."
            elif userInput.find('k ') == 0:
                userInput = userInput.lstrip('k ')
                try:
                    rsvK = float(userInput)
                except ValueError:
                    print "Incorrect value"
                if rsvK > 2:
                    rsvK = 2.0
                elif rsvK < 1.2:
                    rsvK = 1.2
                print "k =", rsvK
            elif userInput.find('b ') == 0:
                userInput = userInput.lstrip('b ')
                try:
                    rsvB = float(userInput)
                except ValueError:
                    print "Incorrect value"
                if rsvB >= 1:
                    rsvB = 0.99
                elif rsvB <= 0:
                    rsvB = 0.01
                print "b =", rsvB
            elif userInput.find('n ') == 0:
                userInput = userInput.lstrip('n ')
                try:
                    topN = int(userInput)
                except ValueError:
                    print "Incorrect value"
                if rsvB < 1:
                    rsvB = 1
                elif rsvB < 20:
                    rsvB = 20
                print "n =", topN
            else:                               # Process query
                terms = tokeniser.tokenise(userInput)
                lastResults = bm25.rsv(terms, k=rsvK, b=rsvB, n=topN)
                print lastResults
        except Exception, e:
            print e
            pass

if __name__ == "__main__":
    sys.exit(main())
