import config
import FcRequest
import json
import urllib
from FcRequest import vmHttpRequest, searchRequest

def get_sites(token):

#	request_url = config.service_url + config.site_url;
      #  req = BaseRequest.OnlineRequest("POST", base.host, base.HTTP_PORT, url, headers);
        #res = req.request();
        #if res.ststus == 200:
        #        print 'Get sites OK';

        #print res.read();
	return

def clone_vm_by_tmplt(vm_url, vm_config):
	#f = open(vm_json_file);
	#data = json.load(f);
	#data = {
	#	"name":"rest_test",
	#	"description":"for rest test"
	#}
	#print data;
	params = json.dumps(vm_config)
	req = vmHttpRequest("POST", vm_url, "/action/clone", params)
	req.request();
	return

def start_vm(vm_url):
        req = vmHttpRequest("POST", vm_url, "/action/start")
        req.request();
        return;

def stop_vm(vm_url):
	data = {"mode":"safe"}
	print data;
        params = json.dumps(data)
        req = vmHttpRequest("POST", vm_url, "/action/stop", params)
        req.request();
	return

def reboot_vm(vm_url):
	data = {"mode":"safe"}
	print data;
        params = json.dumps(data)
        req = vmHttpRequest("POST", vm_url, "/action/reboot", params)
        req.request();
	return

def del_vm(vm_url):
	data = {"isReserveDisks":0,
                "isFormat":0,
                "holdTime":0
	}
	print data;
        params = json.dumps(data)
        req = vmHttpRequest("DELETE", vm_url, "", params)
        req.request();
	return

def get_vm_info(vm_url):

        req = vmHttpRequest("GET", vm_url, "")
        res = req.request();
	vm_info = json.loads(res.read().decode('utf-8'))
	
	return vm_info
	
def search_vm(site_id, condition_params):
	search_obj_url = '{}/{}/vms'.format(config.site_url, site_id)
	condition = urllib.urlencode(condition_params)
	print condition
	req = searchRequest('GET', search_obj_url, condition)
	res = req.request();
	vms = json.loads(res.read().decode('utf-8'))
	return vms;
	
