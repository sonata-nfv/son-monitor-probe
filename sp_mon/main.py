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

__author__="panos"
__date__ ="$Apr 16, 2016 7:37:03 PM$"
import urllib2, time, logging                                                                                                                              
import json, urllib2, os
from threading import  Thread    
from VmData import vmdt
from ContData import cntdt
from configure import configuration
from logging.handlers import RotatingFileHandler

def init():
    global prometh_server
    global node_name
    global logger
    global vm_id
       
    #read configuration
    
    conf = configuration("/opt/Monitoring/node.conf")
    if hasattr(conf.ConfigSectionMap("vm_node"),'cadvisor'):
    	cadvisor = conf.ConfigSectionMap("vm_node")['cadvisor']
    node_name = os.getenv('NODE_NAME', conf.ConfigSectionMap("vm_node")['node_name'])
    prometh_server = os.getenv('PROM_SRV', conf.ConfigSectionMap("Prometheus")['server_url'])
    #node_name = conf.ConfigSectionMap("vm_node")['node_name']
    #prometh_server = conf.ConfigSectionMap("Prometheus")['server_url']
    if hasattr(conf.ConfigSectionMap("vm_node"),'node_exporter'):
        node_exporter = conf.ConfigSectionMap("vm_node")['node_exporter']
    logger = logging.getLogger('dataCollector')
    #hdlr = logging.FileHandler('dataCollector.log', mode='w')
    hdlr = RotatingFileHandler('dataCollector.log', maxBytes=10000, backupCount=1)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    vm_id = getMetaData()
    if vm_id == None:
        vm_id = node_name
    print vm_id
    logger.info('SP Data Collector')
    logger.info('Promth Server '+prometh_server)
    logger.info('Monitoring Node '+node_name)

def postNode(node_,type_, data_):
    url = prometh_server+"/job/"+type_+"/instance/"+node_
    logger.info('Post on: \n'+url)
    try: 
        req = urllib2.Request(url)
        req.add_header('Content-Type','text/html')
        req.get_method = lambda: 'PUT'
        response=urllib2.urlopen(req,data_)
        code = response.code
        logger.info('Response Code: '+str(code))      
    except urllib2.HTTPError, e:
        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:
        logger.warning('Error: '+str(e))
        
def getMetaData():
    try:
        url = 'http://169.254.169.254/openstack/latest/meta_data.json'
        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        
        response=urllib2.urlopen(req, timeout = 3)
        code = response.code
        data = json.loads(response.read())
        #print json.dumps(data)
        return data["uuid"]
    
    except urllib2.HTTPError, e:
        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:
        logger.warning('Error: '+str(e))
    except ValueError, e:
        logger.warning('Error: '+str(e))


def function1(id_):
    global vm_dt
    vm_dt = None
    lsval={}
    while 1:
        dt_collector = vmdt(id_,lsval)
        lsval = dt_collector.getCurrentDT()
        vm_dt = dt_collector.prom_parser()
        time.sleep(1)
        
def function2():
    global container_dt
    container_dt = None
    while 1:     
        container_dt = cntdt().prom_parser()
        time.sleep(4)


if __name__ == "__main__":
    init()
    t1 = Thread(target = function1, args=(vm_id,))
    t2 = Thread(target = function2)
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    
    
    while 1:
        time.sleep(5)
        if container_dt: 
            postNode(node_name,"containers",container_dt)
        if vm_dt:
            postNode(node_name,"vm",vm_dt)
