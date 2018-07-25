## ALL RIGHTS RESERVED.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## Neither the name of the SONATA-NFV, 5GTANGO [, ANY ADDITIONAL AFFILIATION]
## nor the names of its contributors may be used to endorse or promote
## products derived from this software without specific prior written
## permission.
##
## This work has been performed in the framework of the SONATA project,
## funded by the European Commission under Grant number 671517 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the SONATA
## partner consortium (www.sonata-nfv.eu).
##
## This work has been performed in the framework of the 5GTANGO project,
## funded by the European Commission under Grant number 761493 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the 5GTANGO
## partner consortium (www.5gtango.eu).
# encoding: utf-8

import json

class server(object):
    def __init__(self, server_):
        self.id = server_["id"]
        self.status = server_["status"]
        self.updated = server_["updated"]
        self.hostId = server_["hostId"]
        self.hostName = server_["OS-EXT-SRV-ATTR:hypervisor_hostname"]
        self.addresses = server_["addresses"]
        if 'id' in server_["image"]:
            self.imageId = server_["image"]["id"]
        else:
            self.imageId = 'null'
        self.launched = server_["OS-SRV-USG:launched_at"]
        self.flavorId = server_["flavor"]["id"]
        #self.security_groups = server_["security_groups"]
        self.name = server_["name"]
        self.useId = server_["user_id"]
        self.tenantId = server_["tenant_id"]
        self.volumes = server_["os-extended-volumes:volumes_attached"]
        
    def addDgn(self,diagnostics_):
        self.diagnostics = diagnostics_

    def getAddr(self):
        nets = self.addresses.keys()
        netlabels=[]
        label=""
        i=0
        if nets:
            label=", "
            for net in nets:
                i=i+1
                if i > 1:
                    label +=", "
                network={}
                network['label'] = "network_"+str(i)
                network['name'] = net
                network['IPs'] = []
                label += "network_"+str(i)+"=\""+network['name']
                for interface in self.addresses[net]:
                    network['IPs'].append(interface['addr'])
                    label += ":"+interface['addr']
                label += "\""
                netlabels.append(network)
        label = ", "+label
        return label


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)