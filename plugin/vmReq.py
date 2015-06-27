import config

import FcRequest

import json

from FcRequest import vmHttpRequest

def get_sites(token):

request_url = config.service_url + config.site_url;

        req = BaseRequest.OnlineRequest("POST", base.host, base.HTTP_PORT, url, headers);

        res = req.request();

        if res.ststus == 200:

                print 'Get sites OK';

        print res.read();

return

def clone_vm_by_tmplt(site_id, vm_id, vm_json_file):

#f = open(vm_json_file);

#data = json.load(f);

data = {

"name":"rest_test",

"description":"for rest test"

}

print data;

params = json.dumps(data)

req = vmHttpRequest("POST", site_id, vm_id, "/action/clone", params)

req.request();

return

def start_vm(site_id, vm_id):

        req = vmHttpRequest("POST", site_id, vm_id, "/action/start")

        req.request();

        return;

def stop_vm(site_id, vm_id):

data = {"mode":"safe"}

print data;

        params = json.dumps(data)

        req = vmHttpRequest("POST", site_id, vm_id, "/action/clone", params)

        req.request();

return

def reboot_vm(site_id, vm_id):

data = {"mode":"safe"}

print data;

        params = json.dumps(data)

        req = vmHttpRequest("POST", site_id, vm_id, "/action/reboot", params)

        req.request();

return

def del_vm(site_id, vm_id):

data = {"isReserveDisks":0,

                "isFormat":0,

                "holdTime":0}

print data;

        params = json.dumps(data)

        req = vmHttpRequest("DELETE", site_id, vm_id, "", params)

        req.request();

return
