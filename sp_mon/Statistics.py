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

from docker import Client
import os, subprocess, json


class Statistics:
    'Collect statistics from docker engine'
    containers = []
    mon_dt = []

    def __init__(self):
        self.collectStats()
        self.collectData()
        #print json.dumps(self.mon_dt)

    def getMonInfo(self):
        return self.mon_dt
     
    def convert2MB(self,val_,unit_):
        if unit_ == 'B':
            return float(val_)/1000000
        elif unit_ == 'KB':
            return float(val_)/1000
        elif unit_ == 'MB':
            return float(val_)
        elif unit_ == 'GB':
            return float(val_)*1000
        elif unit_ == 'TB':
            return float(val_)*1000000


    def collectStats(self):
        p = subprocess.Popen('docker stats --no-stream', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p.stdout.readlines()
        count = 0
        self.containers = []
        for line in lines:
            count += 1
            if count == 1:
                continue
            words = line.split()

            #print line
            con = {}
            con['id'] = words[0]
            con['cpu_perc'] = words[1].replace('%','')
            con['mem_perc'] = words[7].replace('%','')
            con['mem_usage_MB'] = self.convert2MB(words[2],words[3])
            con['mem_limit_MB'] = self.convert2MB(words[5],words[6])
            con['net_rx_MB'] = self.convert2MB(words[8],words[9])
            con['net_tx_MB'] = self.convert2MB(words[11],words[12])
            con['block_in_MB'] = self.convert2MB(words[13],words[14])
            con['block_ou_MB'] = self.convert2MB(words[16],words[17])
            if (con['mem_usage_MB'] == 0) and (con['mem_limit_MB'] == 0):
                continue
            else:
                self.containers.append(con)

    def collectData(self):
        cli = Client(base_url='unix://var/run/docker.sock')
        containers_obj = cli.containers()
        #containers_obj = cli.containers(all='true')
        self.mon_dt = []
        for container in containers_obj:
            cont_info = {}
            cont_info['name'] = container['Names']
            cont_info['image_name'] = container['Image']
            cont_info['created'] = container['Created']
            cont_info['id'] = container['Id']
            cont_info['image'] = container['ImageID']
            #cont_info['stats'] = cli.stats(cont_info['id'], False, False)
            cont_info['status'] = self.statusCode(container['Status'])
            if cont_info['status'] == 1:
                cont_info['stats'] = self.getstats(cont_info['id'])
            else:
                con = {}
                con['id'] = 0
                con['cpu_perc'] = 0
                con['mem_perc'] = 0
                con['mem_usage_MB'] = 0
                con['mem_limit_MB'] = 0
                con['net_rx_MB'] = 0
                con['net_tx_MB'] = 0
                con['block_in_MB'] = 0
                con['block_ou_MB'] = 0
                cont_info['stats'] = con
            self.mon_dt.append(cont_info)

    def getstats(self, id_):
        for cnt in self.containers:
            if id_.startswith(cnt['id']):
                return cnt
        return {}


    def statusCode(self, status_):
        if status_.startswith('Up'): 
            return 1
        elif status_.startswith('Exit'): 
            return 0
        elif status_.startswith('Created'):
            return 2
        elif status_.startswith('Paused'):
            return 3
        else:
            return 4
