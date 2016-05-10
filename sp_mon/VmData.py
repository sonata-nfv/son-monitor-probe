# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os, subprocess
from time import sleep
import sys
__author__="panos"
__date__ ="$Apr 8, 2016 1:30:54 PM$"

class vmdt:
    
    def __init__(self,id_):
        self.mon_data = {}
        self.mon_data['ram'] = self.getRAM()
        self.mon_data['cpu'] = self.getCPU() 
        self.mon_data['network'] = self.getNetTrBytes()
        self.mon_data['disk'] = self.getdiskUsage()
        


    def prom_parser(self, id_):
        #containers metric types
        vm_cpu_perc = "# TYPE vm_cpu_perc gauge" + '\n'
        vm_mem_perc = "# TYPE vm_mem_perc gauge" + '\n'
        vm_mem_free_MB = "# TYPE vm_mem_free_MB gauge" + '\n'
        vm_mem_total_MB = "# TYPE vm_mem_total_MB gauge" + '\n'
        vm_net_rx_MB = "# TYPE vm_net_rx_MB gauge" + '\n'
        vm_net_tx_MB = "# TYPE vm_net_tx_MB gauge" + '\n'
        vm_disk_usage_perc = "# TYPE vm_disk_usage_perc gauge" + '\n'
        vm_disk_used_1k_blocks = "# TYPE vm_disk_used_1k_blocks gauge" + '\n'
        vm_disk_total_1k_blocks = "# TYPE vm_disk_total_1k_blocks gauge" + '\n'
    
        data_ = self.mon_data
        for cp in data_['cpu']:
            vm_cpu_perc += "vm_cpu_perc{id=\""+id_+"\", core=\""+str(cp['core'])+"\"}" +str(cp['usage']) + '\n'
        
        vm_mem_perc += "vm_mem_perc{id=\""+id_+"\"}" +str(round(float((data_['ram']['freeRam'])/float(data_['ram']['totalRAM'])*100),2))+ '\n'
        vm_mem_free_MB += "vm_mem_free_MB{id=\""+id_+"\"}" +str(data_['ram']['freeRam'])+ '\n'
        vm_mem_total_MB += "vm_mem_total_MB{id=\""+id_+"\"}" +str(data_['ram']['totalRAM'])+ '\n'
        
        for cp in data_['network']:   
            vm_net_rx_MB += "vm_net_rx_MB {id=\""+id_+"\", inf=\""+str(cp['interface'])+"\"}" +str(cp['rx_MB'])+ '\n'
            vm_net_tx_MB += "vm_net_tx_MB{id=\""+id_+"\", inf=\""+str(cp['interface'])+"\"}" +str(cp['tx_MB'])+ '\n'
        for cp in data_['disk']: 
            vm_disk_usage_perc += "vm_disk_usage_perc{id=\""+id_+"\", file_system=\""+str(cp['file_system'])+"\"}" +str(cp['usage_perc'])+ '\n'
            vm_disk_used_1k_blocks += "vm_disk_used_1k_blocks{id=\""+id_+"\", file_system=\""+str(cp['file_system'])+"\"}" +str(cp['used'])+ '\n'
            vm_disk_total_1k_blocks += "vm_disk_total_1k_blocks{id=\""+id_+"\", file_system=\""+str(cp['file_system'])+"\"}" +str(cp['size_1k_block'])+ '\n'
            
        data = vm_cpu_perc +vm_mem_perc + vm_mem_free_MB + vm_mem_total_MB +vm_net_rx_MB + vm_net_tx_MB + vm_disk_usage_perc + vm_disk_used_1k_blocks + vm_disk_total_1k_blocks
        return data
        
    
         
    def getRAM(self):
        meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
        return {"freeRam":meminfo["MemFree"], "totalRAM":meminfo["MemTotal"]} 

    
    def getCPU(self):
        '''
        The meanings of the columns are as follows, from left to right:

        - user: normal processes executing in user mode
        - nice: niced processes executing in user mode
        - system: processes executing in kernel mode
        - idle: twiddling thumbs
        - iowait: waiting for I/O to complete
        - irq: servicing interrupts
        - softirq: servicing softirqs
        - steal: involuntary wait
        - guest: running a normal guest
        - guest_nice: running a niced guest
        
        p = subprocess.Popen('cat /proc/stat | grep cpu', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p.stdout.readlines()
        cpus = []
        for line in lines:
            if line.startswith("cpu"):
                cpu = line.split()
                usage = (float(cpu[1])+float(cpu[3]))/(float(cpu[1])+float(cpu[3])+float(cpu[4]))*100
                cpus.append({"core": cpu[0],"usage":round(usage,2)})
        return cpus
        '''
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
            netif["interface"] = nif[0]
            netif["rx_MB"] = int(nif[1])/1000000 
            netif["tx_MB"] = int(nif[9])/1000000
            netifs.append(netif)
            
        return netifs
    
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
            if dk[0].startswith('/dev/'):
                disk ={}
                disk["file_system"] = dk[0]
                disk["size_1k_block"] = dk[1]
                disk["used"] = dk[2]
                disk["usage_perc"] = dk[4].replace('%','')
                disks.append(disk)
        return disks
    
class GetCpuLoad(object):

    def __init__(self, percentage=True, sleeptime = 1):
        '''
        @parent class: GetCpuLoad
        @date: 04.12.2014
        @author: plagtag
        @info: 
        @param:
        @return: CPU load in percentage
        '''
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getcputime(self):
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