import urllib
import urllib2
from utils.wordList import build_wordlist
import threading

wordlist_file = "/Users/evega/Documents/cice/pruebas/SVNDigger/all.txt" # from SVN Digger
threads = 5

target_url = "http://testphp.vulnweb.com"
user_agent = "Mozilla/5.0 (X11; LInux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"


def dir_bruter(word_queue, extensions=None):

    while not word_queue.empty():
        attempt = word_queue.get()

        attempt_list = []

        # check to see if there is a file extension;
        # if not it's a directory path we are bruting
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)

        # if we want to bruteforce extensions
        # shouldnt we ignore this if we identified it was a directory?
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt, extension))

        #iterate over our list of attempts
        for brute in attempt_list:
            url = "%s%s" % (target_url, urllib.quote(brute)) # quote('abc def') -> 'abc%20def'.... encode?

            try:
                headers = {}
                headers["User-Agent"] = user_agent
                r = urllib2.Request(url, headers=headers)

                response = urllib2.urlopen(r)
                data = response.read()
                if len(data):
                    #print "Data.... %s" % data
                    print "[%d] => %s" % (response.code, url)
            except urllib2.URLError, e:
                if hasattr(e, 'code') and e.code != 404:
                    print "!!! %d => %s" % (e.code, url)
                    # anything but 404 could indicate something interesting on the remote web server aside from a 'file not found' error
                pass

word_queue = build_wordlist(wordlist_file)
extensions = [".php", ".bak", ".orig", ".inc"]

for i in range(threads):
    t = threading.Thread(target=dir_bruter, args=(word_queue,extensions))
    t.start()

