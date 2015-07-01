#Http Request class

#method, url, headers, body

import httplib
import urllib
import json

class HttpRequest:

        def __init__(self, method, host, port, url, headers, body=''):

                self.host = host;
                self.port = port;
                self.method = method;
                self.url = url;
                self.headers = headers;
                self.body = body;

        def request(self):

                conn = httplib.HTTPConnection(self.host, self.port, timeout=30);
                conn.request(method=self.method,url=self.url, body=self.body, headers=self.headers);
                response = conn.getresponse();
                status = response.status;
                res = response.read();
                print self.url;
                print status;
                print res;

                if response >= 400:
                        print '{0} Error http request : {1}'.format(status, self.url);
                        print 'response: ' + res;

                conn.close();
                return response;


class GetRequest:
 
    def __init__(self, url, headers):
            self.url = url;
            self.headers = headers;
    def request(self):
            req = urllib2.Request(self.url)
            for key in self.headers:
                    req.add_header(key, self.headers[key])
            resp = urllib2.urlopen(req);
            return resp;
