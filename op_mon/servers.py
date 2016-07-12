'''
Copyright (c) 2015 SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote 
products derived from this software without specific prior written 
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through 
the Horizon 2020 and 5G-PPP programmes. The authors would like to 
acknowledge the contributions of their colleagues of the SONATA 
partner consortium (www.sonata-nfv.eu).
'''

import json

class server(object):
    def __init__(self, server_):
        self.id = server_["id"]
        self.status = server_["status"]
        self.updated = server_["updated"]
        self.hostId = server_["hostId"]
        self.hostName = server_["OS-EXT-SRV-ATTR:hypervisor_hostname"]
        self.addresses = server_["addresses"]
        self.imageId = server_["image"]["id"]
        self.launched = server_["OS-SRV-USG:launched_at"]
        self.flavorId = server_["flavor"]["id"]
        self.security_groups = server_["security_groups"]
        self.name = server_["name"]
        self.useId = server_["user_id"]
        self.tenantId = server_["tenant_id"]
        self.volumes = server_["os-extended-volumes:volumes_attached"]
        
    def addDgn(self,diagnostics_):
        self.diagnostics = diagnostics_