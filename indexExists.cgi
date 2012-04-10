#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(display=0, logdir="/var/log/cgi-logs/")
import os.path

doesIt = os.path.exists("index/fullindex.csv") and os.path.exists("index/doclength.csv") and os.path.exists("index/urls.csv")

print "Content-type: text/html"
print

print doesIt
