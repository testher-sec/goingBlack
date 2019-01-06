import os
import Queue
import urllib2
import threading

threads = 10

target = "http://www.blackhatpython.com"

# we'll download and extract here the web app
directory = "/Users/evega/Documents/cice/pruebas"

# not interesting extensions for us
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)

web_paths = Queue.Queue()

for r,d,f in os.walk("."): # "." is the top dir
    for files in f:
        remote_path = "%s/%s" % (r,files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        # Split a path in root and extension.
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()

            print "[%d] => %s" % (response.code, path)
            response.close()

        except urllib2.HTTPError as error:
            print "Failed %s" % error.code
            pass


for i in range(threads):
    print "Spawning thread: %d" % i
    t = threading.Thread(target=test_remote)
    t.start()