#!/usr/bin/env python

#import os.path
import cgi
import cgitb
cgitb.enable(display=0, logdir="/var/log/cgi-logs/")  # for troubleshooting

print "Content-type: text/html"
print

doesIt = False #os.path.exists("index/fullindex.csv") and os.path.exists("index/doclength.csv") and os.path.exists("index/urls.csv")
                                                       
print doesIt
