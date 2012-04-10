#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import os.path

doesIt = os.path.exists("index/fullindex.csv") and os.path.exists("index/doclength.csv") and os.path.exists("index/urls.csv")


print "Content-type: text/html"
print

print doesIt
print """<html>
<head>
	<title>Sample CGI Script</title>
</head>

<body>
  <h3> Sample CGI Script </h3>
"""

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

doesIt = False
print doesIt


print """
  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="/test.cgi">
    <p>message: 
	<input type="text" name="message"/>
	<input type='button' value='go' />
	</p>
  </form>

</body>
</html>
""" % cgi.escape(message)
