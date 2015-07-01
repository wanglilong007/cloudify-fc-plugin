import config
from BaseRequest import HttpRequest,GetRequest

def get_versions():

	request_url = service_url + version_url;
	req = BaseRequest.HttpRequest("POST", config.host, config.HTTP_PORT, url, headers);
	res = req.request();

	if response.status == 200:
		print "Get versions OK";

	print response.read();
	return

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

class vmHttpRequest(OnlineRequest):

        def __init__(self, method, site_id, vm_id, action_url, body=''):
                token = login();
                self.token = token;
                self.vm_id = vm_id;
                self.action_url = action_url;
                url = config.service_url + config.site_url + "/" +site_id + config.vm_url + "/" + vm_id + action_url;
                OnlineRequest.__init__(self, token, method, url, body)

        def request(self):
                res = OnlineRequest.request(self);
                logout(self.token);
                return res;

            

def logout(token):

	url = config.service_url + config.session_url;
	req = OnlineRequest(token, "DELETE", url);
	res = req.request();

	if res.status == 200:
        	print 'Logout OK';
