# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import json
from Statistics import Statistics
__author__="panos"
__date__ ="$Apr 8, 2016 1:30:54 PM$"

class cntdt:

    data = []
    
    def __init__(self):
        self.data = Statistics().getMonInfo()

    def checkNone(self,val_):
	if val_ == None:
		return 0
        return val_
        
    def prom_parser(self):
        #containers metric types
        cnt_created = "# TYPE cnt_created count" + '\n'
        cnt_cpu_perc = "# TYPE cnt_cpu_perc gauge" + '\n'
        cnt_mem_perc = "# TYPE cnt_mem_perc gauge" + '\n'
        cnt_mem_usage_MB = "# TYPE cnt_mem_usage_MB gauge" + '\n'
        cnt_mem_limit_MB = "# TYPE cnt_mem_limit_MB gauge" + '\n'
        cnt_net_rx_MB = "# TYPE cnt_net_rx_MB gauge" + '\n'
        cnt_net_tx_MB = "# TYPE cnt_net_tx_MB gauge" + '\n'
        cnt_block_in_MB = "# TYPE cnt_block_in_MB gauge" + '\n'
        cnt_block_ou_MB = "# TYPE cnt_block_ou_MB gauge" + '\n'
	
        for cnt in self.data:
            cnt_created = "cnt_created{id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}" +str(self.checkNone(cnt['created']))+ '\n'
            cnt_cpu_perc += "cnt_cpu_perc{id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}"+str(self.checkNone(cnt['stats']['cpu_perc']))+ '\n'
            cnt_mem_perc += "cnt_mem_perc{id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}"+str(self.checkNone(cnt['stats']['mem_perc']))+ '\n'
            cnt_mem_usage_MB += "cnt_mem_usage_MB{id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}"+str(self.checkNone(cnt['stats']['mem_usage_MB']))+ '\n'
            cnt_mem_limit_MB += "cnt_mem_limit_MB {id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}" +str(self.checkNone(cnt['stats']['mem_limit_MB']))+ '\n'
            cnt_net_rx_MB += "cnt_net_rx_MB{id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}" +str(self.checkNone(cnt['stats']['net_rx_MB']))+ '\n'
            cnt_net_tx_MB += "cnt_net_tx_MB{id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}" +str(self.checkNone(cnt['stats']['net_tx_MB']))+ '\n'
            cnt_block_in_MB += "cnt_block_in_MB{id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}" +str(self.checkNone(cnt['stats']['block_in_MB']))+ '\n'
            cnt_block_ou_MB += "cnt_block_ou_MB{id=\""+cnt['id']+"\",image_name=\""+cnt['image_name']+"\",image=\""+cnt['image']+"\"}" +str(self.checkNone(cnt['stats']['block_ou_MB']))+ '\n'
            
        data = cnt_cpu_perc +cnt_mem_perc + cnt_mem_usage_MB + cnt_mem_limit_MB + cnt_net_rx_MB + cnt_net_tx_MB + cnt_block_in_MB + cnt_block_ou_MB
	return data