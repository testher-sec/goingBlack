# https://gist.github.com/kennethreitz/973705
# http://docs.python-requests.org/en/master/

import urllib2

url = "http://www.tel.uva.es"
headers = {}
headers['User-Agent'] = "Googlebot"

#1...........................
body = urllib2.urlopen(url)
print body.read()

#2...........................
request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
print response.read()
response.close()
