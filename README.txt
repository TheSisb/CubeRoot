Built a web crawler, indexer, and search engine
Information Retrieval project (COMP479) at Concordia University
Built in a team of 3

== INFO ==

Crawling
- We used websphinx (https://www.cs.cmu.edu/~rcm/websphinx/)

Input Control (what we did with the crawled pages)
- Removed exactly duplicate pages
- Tokenizing
- Weighted DOM
- Stemming
- Stop Word removal
- Case Folding

Our vector space model
- Using numpy we created large arrays of tf-idf values

Clustering
- Using kmeans (k selected based on some stats)
-- Takes the best result
-- Best of 'n' random seeds

Search Engine Queries
- Spell correction
- Tokenize
- Stem
- Stop word removal
- Case fold

Weighing the results
- Create a query vector
- Find nearest cluster ( Euclidean Distance - O(n) )
- Retrieve documents based on Cosine Similarity

