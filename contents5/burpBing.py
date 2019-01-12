from burp import IBurpExtender
from burp import IContextMenuFactory # allows us to provide a context menu when user right-clicks a request in Burp

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import socket
import urllib
import json
import re # REGULAR EXPRESSIONS!!! :))
import base64
import threading



bing_api_key = "mykey"

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None

        # we set up our extension
        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Send to Bing", actionPerformed=self.bing_menu))
        return menu_list

    def bing_menu(self, event):
        # grab the details of what the user clicked
        http_traffic = self.context.getSelectedMessages()

        print "%d requests highlighted" % len(http_traffic)

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()

            print "User selected host: %s" % host

            self.bing_search(host)

    def bing_search(self, host):
        # check if we have an IP or hostname
        is_ip = re.match("[0-9]+(?:\.[0-9]+){3}", host)

        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True

        bing_query_string = "'ip:%s'" % ip_address
        self.bing_query(bing_query_string)

        if domain:
            bing_query_string = "'domain:%s'" % host
            self.bing_query(bing_query_string)

    def bing_query(self, bing_query_string):

        print "Performing Bing search: %s" % bing_query_string

        t = threading.Thread(target=self.__trigger_bing_query)
        t.start()

    def __trigger_bing_query(self, bing_query_string):

        # encode our query
        quoted_query = urllib.quote(bing_query_string)

        # OMG, :facepalm: burp http api requires that we build up the entire HTTP request as a string before sending it off,
        # and in particular you can see that we need to base64-encode
        http_request = "GET https://api.datamarket.azure.com/Bing/SEarch/WEb?$format=json&$top=20&Query=%s HTTP/1.1\r\n" % quoted_query
        http_request += "Host: api.datamarket.azure.com\r\n"
        http_request += "Connection: close \r\n"
        http_request += "Authorization: Basic %s\n\n" % base64.b64encode(":%s" % bing_api_key)
        http_request += "User-Agent: Blackhat Python\r\n\r\n"

        json_body = self._callbacks.makeHttpRequest("api.datamarket.azure.com", 443, True, http_request).tostring()

        # split the headers off
        json_body = json_body.split("\r\n\r\n", 1)[1]

        try:
            r = json.loads(json_body)
            if len(r["d"]["results"]):
                for site in r["d"]["results"]:
                    print "*" * 100
                    print site['Title']
                    print site['Url']
                    print site['Description']
                    print "*" * 100

                    j_url = URL(site['Url'])

                    # not sure about this part. How is Burp Target Scope?
                    if not self._callbacks.isInScope(j_url):
                        print "Adding to Burp scope"
                        self._callbacks.includeInScope(j_url)


        except:
            print "No results from Bing"
