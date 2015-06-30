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

@operation
def create(**kwargs):
    # retrieve the port from the node's properties
    site_id = ctx.node.properties['site_id']
    vm_id = ctx.node.properties['image_id']
    # setting node instance runtime property
    vmReq.clone_vm_by_tmplt(site_id, vm_id, "./vm_1.json");
    ctx.logger.info('created vm')

@operation
def start(**kwargs):
    site_id = ctx.node.properties['site_id']
    vm_id = ctx.node.properties['image_id']
    # setting node instance runtime property
    #ctx.instance.runtime_properties['ip'] = ip;
    #vmReq.start_vm(site_id, vm_id);
    ctx.logger.info('verify server is up')
    # verify
    #verify_server_is_up(webserver_port)
    ctx.logger.info('created vm')

@operation
def stop(**kwargs):
    site_id = ctx.node.properties['site_id']
    vm_id = ctx.node.properties['image_id']
    # setting node instance runtime property
    #ctx.instance.runtime_properties['value_of_some_property'] = some_property
    vmReq.stop_vm(site_id, vm_id);
    ctx.logger.info('stop vm')

@operation
def delete(**kwargs):
    site_id = ctx.node.properties['site_id']
    vm_id = ctx.node.properties['image_id']
    # setting node instance runtime property
    #ctx.instance.runtime_properties['value_of_some_property'] = some_property
    vmReq.del_vm(site_id, vm_id);
    ctx.logger.info('delete vm')


@operation
def creation_validation(**kwargs):
    # setting node instance runtime property
    ctx.instance.runtime_properties['value_of_some_property'] = some_property

def verify_server_is_up(port):
    for attempt in range(15):
        try:
            response = urllib2.urlopen("http://localhost:{0}".format(port))
            response.read()
            break
        except BaseException:
            time.sleep(1)
    else:
        raise NonRecoverableError("Failed to start HTTP webserver")


