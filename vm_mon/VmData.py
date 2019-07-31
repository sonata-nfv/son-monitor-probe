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

import os, subprocess
from time import sleep
import sys,time,datetime


class vmdt:
    
    def __init__(self,id_, lsdt_):
        self.id = id_
        self.prv_mon_data = lsdt_
        self.mon_data = {}
        self.mon_data['ram'] = self.getRAM()
        self.mon_data['cpu'] = self.getCPU() 
        self.mon_data['network'] = self.getNetTrBytes()
        self.mon_data['disk'] = self.getdiskUsage()
        
    def getCurrentDT(self):
        return self.mon_data

    def prom_parser(self):
        timestamp = " "+str(int(datetime.datetime.now().strftime("%s")) * 1000)
        #vm metric types
        vm_up = "# TYPE vm_up gauge" + '\n'
        vm_cpu_perc = "# TYPE vm_cpu_perc gauge" + '\n'
        vm_mem_perc = "# TYPE vm_mem_perc gauge" + '\n'
        vm_mem_free_MB = "# TYPE vm_mem_free_MB gauge" + '\n'
        vm_mem_total_MB = "# TYPE vm_mem_total_MB gauge" + '\n'
        vm_net_rx_MB = "# TYPE vm_net_rx_MB gauge" + '\n'
        vm_net_tx_MB = "# TYPE vm_net_tx_MB gauge" + '\n'
        vm_net_rx_bps = "# TYPE vm_net_rx_bps gauge" + '\n'
        vm_net_tx_bps = "# TYPE vm_net_tx_bps gauge" + '\n'
        vm_net_rx_pps = "# TYPE vm_net_rx_pps gauge" + '\n'
        vm_net_tx_pps = "# TYPE vm_net_tx_pps gauge" + '\n'
        vm_disk_usage_perc = "# TYPE vm_disk_usage_perc gauge" + '\n'
        vm_disk_used_1k_blocks = "# TYPE vm_disk_used_1k_blocks gauge" + '\n'
        vm_disk_total_1k_blocks = "# TYPE vm_disk_total_1k_blocks gauge" + '\n'
        
        vm_up += "vm_up{resource_id=\""+self.id+"\"}" + str(int(datetime.datetime.now().strftime("%s"))) + timestamp+ '\n'
        data_ = self.mon_data
        for cp in data_['cpu']:
            vm_cpu_perc += "vm_cpu_perc{resource_id=\""+self.id+"\", core=\""+str(cp['core'])+"\"}" +str(cp['usage']) + timestamp + '\n'
        
        vm_mem_perc += "vm_mem_perc{id=\""+self.id+"\"}" +str(round(100.0 - (float((data_['ram']['freeRam'])/float(data_['ram']['totalRAM'])*100)),2))+ timestamp + '\n'
        vm_mem_free_MB += "vm_mem_free_MB{resource_id=\""+self.id+"\"}" +str(data_['ram']['freeRam']) + timestamp+ '\n'
        vm_mem_total_MB += "vm_mem_total_MB{resource_id=\""+self.id+"\"}" +str(data_['ram']['totalRAM']) + timestamp+ '\n'
        
        for cp in data_['network']:   
            vm_net_rx_MB += "vm_net_rx_MB {resource_id=\""+self.id+"\", inf=\""+str(cp['interface'])+"\"}" +str(cp['rx_MB']) + timestamp+ '\n'
            vm_net_tx_MB += "vm_net_tx_MB{resource_id=\""+self.id+"\", inf=\""+str(cp['interface'])+"\"}" +str(cp['tx_MB']) + timestamp+ '\n'
            if cp['rx_bps'] != -1:
                vm_net_rx_bps += "vm_net_rx_bps{resource_id=\""+self.id+"\", inf=\""+str(cp['interface'])+"\"}" +str(cp['rx_bps']) + timestamp+ '\n'
            else:
                vm_net_rx_bps =''
            if cp['tx_bps'] != -1:
                vm_net_tx_bps += "vm_net_tx_bps{resource_id=\""+self.id+"\", inf=\""+str(cp['interface'])+"\"}" +str(cp['tx_bps']) + timestamp+ '\n'
            else:
                vm_net_tx_bps=''
            if cp['rx_pps'] != -1:
                vm_net_rx_pps += "vm_net_rx_pps{resource_id=\""+self.id+"\", inf=\""+str(cp['interface'])+"\"}" +str(cp['rx_pps']) + timestamp+ '\n'
            else:
                vm_net_rx_pps=''
            if cp['tx_pps'] != -1:
                vm_net_tx_pps += "vm_net_tx_pps{resource_id=\""+self.id+"\", inf=\""+str(cp['interface'])+"\"}" +str(cp['tx_pps']) + timestamp+ '\n'
            else:
                vm_net_tx_pps=''


        for cp in data_['disk']: 
            vm_disk_usage_perc += "vm_disk_usage_perc{resource_id=\""+self.id+"\", file_system=\""+str(cp['file_system'])+"\"}" +str(cp['usage_perc']) + timestamp+ '\n'
            vm_disk_used_1k_blocks += "vm_disk_used_1k_blocks{resource_id=\""+self.id+"\", file_system=\""+str(cp['file_system'])+"\"}" +str(cp['used']) + timestamp+ '\n'
            vm_disk_total_1k_blocks += "vm_disk_total_1k_blocks{resource_id=\""+self.id+"\", file_system=\""+str(cp['file_system'])+"\"}" +str(cp['size_1k_block']) + timestamp+ '\n'
            
        data = vm_up + vm_cpu_perc +vm_mem_perc + vm_mem_free_MB + vm_mem_total_MB +vm_net_rx_MB + vm_net_tx_MB + vm_disk_usage_perc + vm_disk_used_1k_blocks  + vm_disk_total_1k_blocks + vm_net_rx_bps + vm_net_tx_bps + vm_net_rx_pps + vm_net_tx_pps   
        return data
        
    
         
    def getRAM(self):
        meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
        return {"freeRam":meminfo["MemAvailable"], "totalRAM":meminfo["MemTotal"]} 

    
    def getCPU(self):
        return GetCpuLoad().getcpuload()
            
    def getNetTrBytes(self):
        p = subprocess.Popen('cat /proc/net/dev', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p.stdout.readlines()
        netifs = []
        count = 0
        for line in lines:
            count +=1
            if count < 3:
                continue
            nif = line.split()
            netif ={}
            nif[0] = nif[0].replace(':','')
            netif["interface"] = nif[0]
            netif["rx_b"] = int(nif[1]) 
            netif["tx_b"] = int(nif[9])
            netif["rx_pks"] = int(nif[2]) 
            netif["tx_pks"] = int(nif[10])
            netif["rx_error"] = int(nif[3]) 
            netif["rx_drops"] = int(nif[4])
            netif["tx_error"] = int(nif[11]) 
            netif["tx_drops"] = int(nif[12])
            #RX pkts per sec
            lv = int(self.getlastVal(nif[0],"rx_pks"))
            if lv != -1:
                netif["rx_pps"] = int(nif[2]) - lv
            else:
                netif["rx_pps"] = -1
            #TX pkts per sec
            lv = int(self.getlastVal(nif[0],"tx_pks"))
            if lv != -1:    
                netif["tx_pps"] = int(nif[10]) - lv
            else:
                netif["tx_pps"] = -1
            #RX Bytes per sec
            lv = int(self.getlastVal(nif[0],"rx_b"))
            if lv != -1:     
                netif["rx_bps"] = int(nif[1]) - lv
                netif["rx_bps"] = 8*int(netif["rx_bps"])
            else:
                netif["rx_bps"] = -1
            #TX Bytes per sec
            lv = int(self.getlastVal(nif[0],"tx_b"))
            if lv != -1:    
                netif["tx_bps"] = int(nif[9]) - lv
                netif["tx_bps"] = 8*int(netif["tx_bps"])
            else: 
                netif["tx_bps"] = -1
            netif["rx_MB"] = round(int(nif[1])/1000000.0,2) 
            netif["tx_MB"] = round(int(nif[9])/1000000.0,2)
            netifs.append(netif)
            
        return netifs
    
    def getlastVal(self,intf_,mtr_):
        if not 'network' in self.prv_mon_data:
            return -1
        for inf in self.prv_mon_data['network']:
            if inf['interface'] == intf_:
                if mtr_ in inf:
                    return inf[mtr_]
        return -1

    def getdiskUsage(self):
        p = subprocess.Popen('df', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p.stdout.readlines()
        disks = []
        count = 0
        for line in lines:
            count +=1
            if count < 2:
                continue
            dk = line.split()
            if dk[0] == 'none':
                continue
            disk ={}
            disk["file_system"] = dk[0]
            disk["size_1k_block"] = dk[1] 
            disk["used"] = dk[2]
            disk["usage_perc"] = dk[4].replace('%','')
            disks.append(disk)
        return disks
    
class GetCpuLoad(object):

    def __init__(self, percentage=True, sleeptime = 1):
        
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getcputime(self):
        '''
        #the formulas fromnif[0].replace(':','') htop 
             user    nice   system  idle      iowait irq   softirq  steal  guest  guest_nice
        cpu  74608   2520   24433   1117073   6176   4054  0        0      0      0


        Idle=idle+iowait
        NonIdle=user+nice+system+irq+softirq+steal
        Total=Idle+NonIdle # first line of file for all cpus

        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
        '''
        cpu_infos = {} #collect here the information
        with open(self.cpustat,'r') as f_stat:
            lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

            #compute for every cpu
            for cpu_line in lines:
                if '' in cpu_line: cpu_line.remove('')#remove empty elements
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                #update dictionionary
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
            return cpu_infos

    def getcpuload(self):
        '''
        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)

        '''
        start = self.getcputime()
        #wait a second
        sleep(self.sleeptime)
        stop = self.getcputime()

        usage = []
        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']

            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']
            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            usage.append({"core": cpu,"usage":str(round(CPU_Percentage,2))})
        return usage

