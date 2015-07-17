import config
from BaseRequest import HttpRequest,GetRequest

def get_versions():
    
    headers = {
           "Host": config.host+":"+config.HTTP_PORT,
           "Content-type": "application/json; charset=UTF-8"
        }
        
	#request_url = config.service_url + config.version_url;
	#req = HttpRequest("POST", config.host, config.HTTP_PORT, request_url, headers);
	#res = req.request();

	#if res.status == 200:
	#	print "Get versions OK";

	#return res.read();

def login():

	    headers = {
		"Host": config.host+":"+config.HTTP_PORT,
		"Content-type": "application/json; charset=UTF-8",
		"Accept":"application/json; version={}".format(config.VERSION), 
		"X-Auth-User": config.user, 
		"X-Auth-Key": config.passwd, 
		"X-ENCRIPT-ALGORITHM":"0"
		}

	    url = config.service_url + config.session_url;
	    req = HttpRequest("POST", config.host, config.HTTP_PORT, url, headers);
	    res = req.request();
	    print res.status

 	   #if res.status == 200:
        	#print 'Login OK';

	    token = res.getheader('X-Auth-Token');
	    print token
            return token;

class OnlineRequest():
 
    def __init__(self, token, method, url, body=''):
            host = config.host;
            port = config.HTTP_PORT;
            headers = {
                   "Host": config.host+":"+config.HTTP_PORT,
                   "Content-type": "application/json; charset=UTF-8",
                   "Accept":"application/json; version={}".format(config.VERSION),
                   "X-Auth-Token": token,
                }
            if method == 'GET':
                    self.requester = GetRequest('http://'+host+':'+port+url, headers)
            else:
                    self.requester = HttpRequest(method, host, port, url, headers, body);

    def request(self):
            res = self.requester.request();
            return res;

class OnlineRequestOld(HttpRequest):

        def __init__(self, token, method, url, body=''):
                host = config.host;
                port = config.HTTP_PORT;   
                headers = {
                       "Host": config.host+":"+config.HTTP_PORT,
                       "Content-type": "application/json; charset=UTF-8",
                       "Accept":"application/json; version={}".format(config.VERSION), 
                       "X-Auth-Token": token, 
                    }

                HttpRequest.__init__(self, method, host, port, url, headers, body)

        def request(self):
                res = HttpRequest.request(self);
                return res;

class objectHttpRequest(OnlineRequest):
    
    def __init__(self, method, object_url, body=''):
        token = login();
        self.token = token;
        url = object_url;
        OnlineRequest.__init__(self, token, method, url, body)
        
    def request(self):
        res = OnlineRequest.request(self);
        logout(self.token);
        return res;
        
        
class vmHttpRequest(objectHttpRequest):

        def __init__(self, method, vm_url, action_url, body=''):
                self.action_url = action_url;
                url = vm_url + action_url;
                objectHttpRequest.__init__(self, method, url, body)

        def request(self):
                res = objectHttpRequest.request(self);
                return res;

class  searchRequest(objectHttpRequest):
    
    def __init__(self, method, search_obj_url, condition_params, body=''):
        self.condition_params = condition_params;
        self.body = body;
        url = config.service_url + search_obj_url +'?'+ condition_params;
        objectHttpRequest.__init__(self, method, url, body)
        
    def request(self):
            res = objectHttpRequest.request(self);
            return res;

def logout(token):

	url = config.service_url + config.session_url;
	req = OnlineRequest(token, "DELETE", url);
	res = req.request();

	if res.status == 200:
        	print 'Logout OK';
