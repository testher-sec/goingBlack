'''
Functionality to create a Queue out of a wordlist file
https://www.netsparker.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/
'''

import Queue

resume = None

def build_wordlist(wordlist_file):
    # read the word list
    fd = open(wordlist_file, "rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = Queue.Queue()

    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resuming wordlist from: %s" % resume
        else:
            words.put(word)
    return words