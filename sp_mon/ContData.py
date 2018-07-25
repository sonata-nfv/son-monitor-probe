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

import json,time,datetime
from Statistics import Statistics


class cntdt:

    data = []
    dt2sent = False
    
    def __init__(self):
        self.data = Statistics().getMonInfo()

    def checkNone(self,val_):
        if val_ == None:
            return 0
        return val_

    def prom_parser(self):
        #containers metric types
        timestamp = " "+str(int(datetime.datetime.now().strftime("%s")) * 1000)
        cnt_created = "# TYPE cnt_created counter" + '\n'
        cnt_status = "# TYPE cnt_status gauge" + '\n'
        cnt_cpu_perc = "# TYPE cnt_cpu_perc gauge" + '\n'
        cnt_mem_perc = "# TYPE cnt_mem_perc gauge" + '\n'
        cnt_mem_usage_MB = "# TYPE cnt_mem_usage_MB gauge" + '\n'
        cnt_mem_limit_MB = "# TYPE cnt_mem_limit_MB gauge" + '\n'
        cnt_net_rx_MB = "# TYPE cnt_net_rx_MB gauge" + '\n'
        cnt_net_tx_MB = "# TYPE cnt_net_tx_MB gauge" + '\n'
        cnt_block_in_MB = "# TYPE cnt_block_in_MB gauge" + '\n'
        cnt_block_ou_MB = "# TYPE cnt_block_ou_MB gauge" + '\n'
        cnt_status = "# TYPE cnt_status gauge" + '\n'

        for cnt in self.data:
            if len(cnt['stats']) == 0:
                continue
            self.dt2sent = True
            cnt_created += "cnt_created{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}" +str(cnt['created']) + timestamp + '\n'
            cnt_status += "cnt_status{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}" +str(self.checkNone(cnt['status'])) + timestamp + '\n'
            cnt_cpu_perc += "cnt_cpu_perc{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}"+str(self.checkNone(cnt['stats']['cpu_perc'])) + timestamp + '\n'
            cnt_mem_perc += "cnt_mem_perc{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}"+str(self.checkNone(cnt['stats']['mem_perc'])) + timestamp + '\n'
            cnt_mem_usage_MB += "cnt_mem_usage_MB{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}"+str(self.checkNone(cnt['stats']['mem_usage_MB'])) + timestamp + '\n'
            cnt_mem_limit_MB += "cnt_mem_limit_MB {resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}" +str(self.checkNone(cnt['stats']['mem_limit_MB'])) + timestamp + '\n'
            cnt_net_rx_MB += "cnt_net_rx_MB{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}" +str(self.checkNone(cnt['stats']['net_rx_MB'])) + timestamp + '\n'
            cnt_net_tx_MB += "cnt_net_tx_MB{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}" +str(self.checkNone(cnt['stats']['net_tx_MB'])) + timestamp + '\n'
            cnt_block_in_MB += "cnt_block_in_MB{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}" +str(self.checkNone(cnt['stats']['block_in_MB'])) + timestamp + '\n'
            cnt_block_ou_MB += "cnt_block_ou_MB{resource_id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\",name=\""+cnt['name'][0]+"\"}" +str(self.checkNone(cnt['stats']['block_ou_MB'])) + timestamp + '\n'

        data = cnt_created + cnt_cpu_perc +cnt_mem_perc + cnt_mem_usage_MB + cnt_mem_limit_MB + cnt_net_rx_MB + cnt_net_tx_MB + cnt_block_in_MB + cnt_block_ou_MB + cnt_status
        if self.dt2sent:
            return data
        else:
            None