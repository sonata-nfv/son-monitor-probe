# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os, subprocess
from time import sleep
import sys,time,datetime,json

__author__="panos"
__date__ ="$Dec 8, 2016 15:30:0 PM$"

class valdt:
    
    def __init__(self):
        self.prev_dt = None
        self.curr_dt = None
        #self.id = id_
        #self.prv_mon_data = lsdt_
        #self.mon_data = {}
        #self.mon_data['ram'] = self.getRAM()
        #self.mon_data['cpu'] = self.getCPU() 
        #self.mon_data['network'] = self.getNetTrBytes()
        #self.mon_data['disk'] = self.getdiskUsage()
        

    def validateDT(self,dt_):

        metric_hdr = ''
        dt2go = ''
        if self.prev_dt is None:
            #First interation
            self.prev_dt = self.str2obj(dt_)
            #print json.dumps(self.prev_dt)
            return dt_
        else:
            flag = False
            for line in dt_.splitlines():
                if line.startswith('#'):
                    metric_hdr = line
                    flag = False
                else:
                    c_name = self.getMetricName(line, 'name')
                    c_val = self.getMetricName(line, 'value')
                    c_updated = self.getMetricName(line, 'time')
                    if c_name not in self.prev_dt:
                        if not flag:
                            dt2go += metric_hdr + '\n'
                            flag = True
                        dt2go += line+ '\n'
                        self.prev_dt[c_name]={}
                        self.prev_dt[c_name]['value'] = c_val
                        self.prev_dt[c_name]['last_update'] = c_updated
                        continue
                    if self.chDetla(c_name, c_val):
                        if not flag:
                            dt2go += metric_hdr + '\n'
                            flag = True
                        dt2go += line+ '\n'
                        self.prev_dt[c_name]['value'] = c_val
                        continue
                    if self.chTime(c_name, c_updated):
                        if not flag:
                            dt2go += metric_hdr + '\n'
                            flag = True
                        dt2go += line+ '\n'
                        self.prev_dt[c_name]['value'] = c_val
                        self.prev_dt[c_name]['last_update'] = c_updated
                        continue
            return dt2go
                    
                
                    
    def chDetla(self, c_name, c_val):
        return True
        
    def chTime(self, c_name, c_val):
        return True
    
    
    def str2obj(self, data_):
        dt = {}
        for line in data_.splitlines():
            if line.startswith('#'):
                continue
            self.metric_obj(line,dt)
        return dt
            

    def metric_obj(self, ln_,dt_):
        #ptr = ln_.find('}',0)
        name = self.getMetricName(ln_, 'name') #ln_[0:ptr+1]
        val = self.getMetricName(ln_, 'value') #ln_[ptr+1:ln_.find(' ',ptr)].strip()
        updated = self.getMetricName(ln_, 'time') #ln_[ln_.find(' ',ptr+1):len(ln_)].strip()
        dt_[name]={}
        dt_[name]['value'] = val
        dt_[name]['last_update'] = updated
        return 
    
    def getMetricName(self,ln_, key_):
        ptr = ln_.find('}',0)
        if key_ == 'name':
            return ln_[0:ptr+1]
        if key_ == 'value':
            return ln_[ptr+1:ln_.find(' ',ptr)].strip()
        if key_ == 'time':
            return ln_[ln_.find(' ',ptr+1):len(ln_)].strip()
        else:
            return None
    

