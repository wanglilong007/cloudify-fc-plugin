########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

import vmReq

# ctx is imported and used in operations
from cloudify import ctx

# put the operation decorator on any function that is a task
from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError, RecoverableError
import urllib, urllib2, httplib
import config
import time

IP_PROPERTY = 'ip'  # the server's private ip

VM_CREATING = 'creating'
VM_RUNNING = 'running'
VM_STARTING = 'starting'
VM_STOPPED = 'stopped'
VM_STOPPING = 'stopping'
VM_DELETING = 'shutting-down'

@operation
def create(**kwargs):
    # retrieve the port from the node's properties
    site_id = ctx.node.properties['site_id']
    vm_id = ctx.node.properties['image_id']
    vm_name = ctx.node.properties['vm_name']
    vm_desc = ctx.node.properties['vm_desc']
    vm_mac = ctx.node.properties['vm_config']['ex_nic']['nic_mac']
    vm_config = {
            "name": vm_name,
            "description" : vm_desc,
            "vmConfig":
                {
                    "nics":
                        [
                            {
                                "name":"Network Adapter 0",          
                                "portGroupUrn":"urn:sites:435008B8:dvswitchs:2:portgroups:114"
                            },
                            {
                                "name":"Network Adapter 1",            
                                "portGroupUrn":"urn:sites:435008B8:dvswitchs:2:portgroups:42",
                                "mac":vm_mac                                
                            }
                        ]
                }
        }
    vm_url = '{}/{}/{}{}/{}'.format(config.service_url, config.site_url, site_id, config.vm_url, vm_id)
    vmReq.clone_vm_by_tmplt(vm_url, vm_config);
    ctx.logger.info('creating vm')
    get_vm_creating(site_id)
    
@operation
def start(**kwargs):
    site_id = ctx.node.properties['site_id']
    vm_url = ctx.instance.runtime_properties['vm_url']
    ctx.instance.runtime_properties['ip_changed'] = False
    #vmReq.start_vm(vm_url);
    #verify
    #verify_vm_is_up(site_id, vm_id)
    ctx.logger.info('wait for vm running')
    wait_vm_status(VM_RUNNING)

@operation
def stop(**kwargs):
    vm_url = ctx.instance.runtime_properties['vm_url'] 
    vmReq.stop_vm(vm_url);
    ctx.logger.info('stopping vm')
    wait_vm_status(VM_STOPPED)
    
@operation
def delete(**kwargs):
    vm_url = ctx.instance.runtime_properties['vm_url'] 
    vmReq.del_vm(vm_url);
    ctx.logger.info('deleting vm')
    wait_vm_status(VM_DELETING)


@operation
def creation_validation(**kwargs):
    # setting node instance runtime property
    #ctx.instance.runtime_properties['value_of_some_property'] = some_property
    pass

@operation
def get_state(**kwargs):
    vm_url = ctx.instance.runtime_properties['vm_url'] 

    for attempt in range(30):
        ctx.logger.info('verify server is up')
        vm_info = vmReq.get_vm_info(vm_url);
        vm_status = vm_info['status']
        ipv4 = vm_info['vmConfig']['nics'][0]['ip']
        ipv6 = vm_info['vmConfig']['nics'][0]['ips6']
        if len(ipv6) != 0 and ipv4 != '':
            ctx.instance.runtime_properties['ip'] = ipv4;
            ctx.logger.info('get vm ipv4: {}, ipv6: {}'.format(ipv4, ipv6))
            return True;
        else:
            ctx.logger.info('wait for vm ip......vm status is {}, ipv4 is {}, ipv6 is {}'.format(vm_status, ipv4, ipv6))
            
        time.sleep(30)
    else:
        raise NonRecoverableError("Failed to start vm")

def get_vm_creating(site_id):
    vm_name = ctx.node.properties['vm_name']
    vm_desc = ctx.node.properties['vm_desc']
    condition_params = {
            'status': VM_CREATING,
            'name': vm_name,
            'description': vm_desc
        }
    
    for attempt in range(15):
        res = vmReq.search_vm(site_id, condition_params);
        number = res['total']
        
        if number == 1:
            real_vm = res['vms'][0];
            uri = real_vm['uri']
            #uuid = real_vm['uuid']
            name = real_vm['name']
            #ctx.instance.runtime_properties['uuid'] = uuid;
            ctx.instance.runtime_properties['vm_url'] = uri;
            ctx.logger.info('get vm uri :{}, vm name :{}'.format(uri, name))
            break;
        else:
            ctx.logger.info('Wait for vm create......Now searched vm number is {}'. format(number))
            
        time.sleep(20)
    else:
        raise NonRecoverableError("Failed to search vm")
        
def wait_vm_status(status):
    vm_url = ctx.instance.runtime_properties['vm_url'] 

    for attempt in range(30):
        ctx.logger.info('getting server status......')
        vm_info = vmReq.get_vm_info(vm_url);
        vm_status = vm_info['status']
        if vm_status == status:
            ctx.logger.info('get vm status: {}'.format(vm_status))
            break;
        else:
            ctx.logger.info('wait for vm {}......But Now vm status is {}'.format(status, vm_status))
            
        time.sleep(30)
    else:
        raise NonRecoverableError("Failed to wait vm {}".format(status))
