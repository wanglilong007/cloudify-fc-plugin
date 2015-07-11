import vmReq

import FcRequest
import config

site_id = '435008B8'
vm_id = 'i-00000146'

vm_url = '{}/{}{}/{}'.format(config.site_url, site_id, config.vm_url, vm_id)
#get_sites(token);

#vmReq.clone_vm_by_tmplt(vm_url, {'name':'test'});

#vmReq.stop_vm(vm_url);

#vmReq.reboot_vm(vm_url);

#vmReq.del_vm(vm_url);

#vmReq.start_vm(vm_url);

print vmReq.get_vm_info(vm_url)
print vmReq.search_vm(site_id, {'name':'test'})