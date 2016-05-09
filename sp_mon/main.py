# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

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
    prometh_server = os.getenv('PROM_SRV', conf.ConfigSectionMap("vm_node")['node_name'])
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
    while 1:
        vm_dt = vmdt(id_).prom_parser(id_)
        time.sleep(3)
        
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
