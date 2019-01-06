# https://gist.github.com/kennethreitz/973705
# http://docs.python-requests.org/en/master/

import urllib2

body = urllib2.urlopen("http://www.tel.uva.es")
print body.read()

#######################

import requests

response = requests.get("http://www.tel.uva.es")
print response.status_code
print response.text