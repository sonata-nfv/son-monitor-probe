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

import json,urllib2
import datetime,time,logging
from configure import configuration
from servers import server
from DtFiltering import valdt 


def init():
    global keystone_url
    global node_name
    global tenants
    global logger
    global controller_ip

    conf = configuration("odc.conf")     
    keystone_url = conf.ConfigSectionMap("Openstack")['keystone_url']
    node_name = conf.ConfigSectionMap("Openstack")['node_name']
    tenants = json.loads(conf.ConfigSectionMap("Openstack")['tenants'])
    controller_ip = conf.ConfigSectionMap("Openstack")['controller_ip']  
    logger = logging.getLogger('dataCollector')
    hdlr = logging.FileHandler('dataCollector.log', mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    logger.info('Openstack Data Collector')
    logger.info('keystone_url: '+keystone_url)
    logger.info('node_name: '+node_name)
    logger.info('tenants: '+json.dumps(tenants))

def getToken(tenant):
    global token
    global service_endpoint
    
    try: 
        req = urllib2.Request(keystone_url)
        req.add_header('Content-Type','application/json')
        postdata={"auth": {"tenantName": tenant['name'], "passwordCredentials": {"username": tenant['user_name'], "password": tenant['password']}}}
        data = json.dumps(postdata)
        response=urllib2.urlopen(req,data,timeout = 5)
        code = response.code
        data = json.loads(response.read())
        token=data["access"]["token"]
        service_endpoints = data["access"]["serviceCatalog"]
        serv_endpoints ={}
        serv_endpoints['nova'] = getServiceEndpoint("nova",service_endpoints)
        serv_endpoints['neutron'] = getServiceEndpoint("neutron",service_endpoints)
        serv_endpoints['glance'] = getServiceEndpoint("glance",service_endpoints)
        serv_endpoints['cinder'] = getServiceEndpoint("cinder",service_endpoints)
        #print 'Status: '+ str(code) +' Data: '+json.dumps(service_endpoints)
        logger.info('Token: '+token["id"])
        return {"id": token["id"], "service_endpoints": serv_endpoints}
        
    except urllib2.HTTPError, e:
        print e.code
        logger.warning('Error: '+e)
    except urllib2.URLError, e:
        print e.args
        logger.warning('Error: '+e)


def getTokenv3(tenant):
    global token
    global service_endpoint
    
    try: 
        req = urllib2.Request(keystone_url)
        req.add_header('Content-Type','application/json')
        postdata={"auth":{"identity":{"methods":["password"],"password":{"user":{"name":tenant['name'],"domain":{"name":"default"},"password":tenant['password']}}}}}
        data = json.dumps(postdata)
        response=urllib2.urlopen(req,data, timeout = 5)
        code = response.code
        data = json.loads(response.read())
        if code == 201:
            token = response.info().getheader('X-Subject-Token')
        else:
            return None
        
        
        service_endpoints = data["token"]["catalog"]
        serv_endpoints ={}
        serv_endpoints['nova'] = getServiceEndpointv3("nova",service_endpoints)
        serv_endpoints['neutron'] = getServiceEndpointv3("neutron",service_endpoints)
        serv_endpoints['glance'] = getServiceEndpointv3("glance",service_endpoints)
        serv_endpoints['cinder'] = getServiceEndpointv3("cinder",service_endpoints)
        logger.info('Token: '+token)
        print 'Token: '+ token
        return {"id": token, "service_endpoints": serv_endpoints}
        
    except urllib2.HTTPError, e:
        print e.code
        logger.warning('Error: '+e)
    except urllib2.URLError, e:
        print e.args
        logger.warning('Error: '+e)


def getServiceEndpoint(srv_name, endpoints):
    for endpoint in endpoints:
        if endpoint["name"] == srv_name: 
            url = endpoint["endpoints"][0]["publicURL"]
            host = url[url.find("//")+2 : url.find("//") + len(url)-url.find("//")]
            host = host[0 : 0 + host.find(":")]
            url = url.replace(host,controller_ip)
            return url

def getServiceEndpointv3(srv_name, endpoints):
    for endpoint in endpoints:
        if endpoint["name"] == srv_name: 
            list = endpoint["endpoints"]
            for ep in list:
                if ep['interface'] == "public":
                    url = ep["url"]
                    host = url[url.find("//")+2 : url.find("//") + len(url)-url.find("//")]
                    host = host[0 : 0 + host.find(":")]
                    url = url.replace(host,controller_ip)
                    return url
            
def getLimits(token):
    try: 
        url = token['service_endpoints']['nova']+"/limits"
        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        req.add_header('X-Auth-Token',token["id"])
        response=urllib2.urlopen(req, timeout = 5)
        code = response.code
        data = json.loads(response.read())
        return data
        
    except urllib2.HTTPError, e:
        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:
        logger.warning('Error: '+str(e))
    except ValueError, e:
        logger.warning('Error: '+str(e))

def pushdata(server,data,label,tenant_name):
    try:
        req = urllib2.Request(server+"/job/"+label+"/instance/"+node_name+"/vim_tenant/"+tenant_name)
        req.add_header('Content-Type','text/html')
        req.get_method = lambda: 'PUT'
        response=urllib2.urlopen(req,data, timeout = 10)
        code = response.code
        logger.info('Response Code: '+str(code))

    except urllib2.HTTPError, e:
        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:
        logger.warning('Error: '+str(e))


def getVms(creds):
    servers = {}
    try: 
        url = creds['service_endpoints']['nova']+"/servers/detail?all_tenants=1"
        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        req.add_header('X-Auth-Token',creds["id"])
        response=urllib2.urlopen(req)
        code = response.code
        data = json.loads(response.read())
        for ops_svr in data["servers"]:
            ops_svr[ 'addrLabels'] = srv.getAddr()
            srv = server(ops_svr) 
            if ops_svr["status"] == "ACTIVE":
                srv.addDgn(getVmStats(ops_svr["id"],creds))
            else:
                srv.addDgn({}) 
        return data
        
    except urllib2.HTTPError, e:
        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:
        logger.warning('Error: '+str(e))
    except ValueError, e:
        logger.warning('Error: '+str(e))
    
    
def getVmStats(uuid, creds):
    try:
        req = urllib2.Request(creds['service_endpoints']['nova']+"/servers/"+uuid+"/diagnostics")
        req.add_header('Content-Type','application/json')
        req.add_header('X-Auth-Token',creds["id"])
        response=urllib2.urlopen(req)
        code = response.code
        data = json.loads(response.read())
        data["status"] = 'available'
        return data
    
    except urllib2.HTTPError, e:
        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:
        logger.warning('Error: '+str(e))
    except ValueError, e:
        print e.args
        logger.warning('Error: '+str(e))
        
def postLimits(limits, tenant_name, urls):
    timestamp = " "+str(int(datetime.datetime.now().strftime("%s")) * 1000)
    #metricKeys = ['maxServerMeta','maxPersonality','maxImageMeta','maxPersonalitySize','maxTotalRAMSize','maxSecurityGroupRules','maxTotalKeypairs','totalRAMUsed','maxSecurityGroups', 'totalFloatingIpsUsed', 'totalInstancesUsed', 'totalSecurityGroupsUsed', 'maxTotalFloatingIps', 'maxTotalInstances', 'totalCoresUsed', 'maxTotalCores']
    data = ''
    for key in limits["limits"]["absolute"].keys():
        data +="# TYPE " + "vim_"+key + " gauge" + '\n' + "vim_"+key +" "+ str(limits["limits"]["absolute"][key]) + timestamp + '\n'
        
    logger.info('Post Limits: \n'+data)
    for url in urls:
        pushdata(url,data,"limits",tenant_name)
    

def postVMmetrics(vms, tenant_name, urls):
    timestamp = " "+str(int(datetime.datetime.now().strftime("%s")) * 1000)
    #vm_p_states = {'ACTIVE':'1', 'BUILDING':'2', 'PAUSED':'3', 'SUSPENDED':'4', 'STOPPED':'5', 'SHUTOFF':'5', 'RESCUED':'6', 'RESIZED':'7', 'SOFT_DELETED':'8', 'DELETED':'9', 'ERROR':'10', 'SHELVED':'11', 'SHELVED_OFFLOADED':'12', 'ALLOW_SOFT_REBOOT':'13', 'ALLOW_HARD_REBOOT':'14', 'ALLOW_TRIGGER_CRASH_DUMP':'15'}
    
    #Number of servers
    data = ""
    data +="# TYPE vms_sum gauge" + '\n' + "vms_sum "+ str(len(vms)) + timestamp + '\n'
    #data +="# TYPE vms_possible_states{ACTIVE:\""+vm_p_states['ACTIVE']+"\", BUILDING:\""+vm_p_states['BUILDING']+"\", PAUSED:\""+vm_p_states['PAUSED']+"\", SUSPENDED:\""+vm_p_states['SUSPENDED']+"\", STOPPED:\""+vm_p_states['STOPPED']+"\", RESCUED:\""+vm_p_states['RESCUED']+"\", RESIZED:\""+vm_p_states['RESIZED']+"\", SOFT_DELETED:\""+vm_p_states['SOFT_DELETED']+"\", DELETED:\""+vm_p_states['DELETED']+"\", ERROR:\""+vm_p_states['ERROR']+"\", SHELVED:\""+vm_p_states['SHELVED']+"\", SHELVED_OFFLOADED:\""+vm_p_states['SHELVED_OFFLOADED']+"\", ALLOW_SOFT_REBOOT:\""+vm_p_states['ALLOW_SOFT_REBOOT']+"\", ALLOW_SOFT_REBOOT:\""+vm_p_states['ALLOW_TRIGGER_CRASH_DUMP']+"\", ALLOW_TRIGGER_CRASH_DUMP:\""+vm_p_states['ALLOW_SOFT_REBOOT']+"\"} gauge" + '\n' + "vms_possible_states 1"+ '\n'
    
    #vm_state
    vm_states = getStates(vms)
    data +="# TYPE vms_state gauge" + '\n'
    for key in vm_states.keys():
        data += "vms_state{state=\""+key+"\"} "+ str(vm_states[key]) + timestamp + '\n'
    
    #vms
    vm_update = "# TYPE vm_last_update gauge" + '\n'
    vm_pow_state = "# TYPE vm_power_state gauge" + '\n'
    vm_status = "# TYPE vm_status gauge" + '\n'
    
    for vm in vms:
        vm_update +="vm_last_update{uuid=\""+vm['id']+"\""+vm['addrLabels'] +", created=\""+vm['created']+"\", tenant_id=\""+vm['tenant_id']+"\", user_id=\""+vm['user_id']+"\", name=\""+vm['name']+"\", image_id=\""+vm['image']['id']+"\""+"} " + str(date2int(vm['updated'])) + timestamp + '\n'
        vm_pow_state +="vm_power_state{uuid=\""+vm['id']+"\""+vm['addrLabels'] +", created=\""+vm['created']+"\", tenant_id=\""+vm['tenant_id']+"\", user_id=\""+vm['user_id']+"\", name=\""+vm['name']+"\", image_id=\""+vm['image']['id']+"\""+"} " + str(vm['OS-EXT-STS:power_state']) + timestamp + '\n'
        vm_status +="vm_status{uuid=\""+vm['id']+"\""+vm['addrLabels'] +", created=\""+vm['created']+"\", tenant_id=\""+vm['tenant_id']+"\", user_id=\""+vm['user_id']+"\", name=\""+vm['name']+"\", image_id=\""+vm['image']['id']+"\""+"} " + string2int(vm['status']) + timestamp + '\n'
        #vm_update +="vm_last_update{uuid=\""+vm['id']+"\", created=\""+vm['created']+"\", tenant_id=\""+vm['tenant_id']+"\", user_id=\""+vm['user_id']+"\", name=\""+vm['name']+"\", image_id=\""+vm['image']['id']+"\"}" + str(date2int(vm['updated'])) + '\n'
        #vm_pow_state +="vm_power_state{uuid=\""+vm['id']+"\", created=\""+vm['created']+"\", tenant_id=\""+vm['tenant_id']+"\", user_id=\""+vm['user_id']+"\", name=\""+vm['name']+"\", image_id=\""+vm['image']['id']+"\"} " + str(vm['OS-EXT-STS:power_state']) + '\n'
        #vm_status +="vm_status{uuid=\""+vm['id']+"\", created=\""+vm['created']+"\", tenant_id=\""+vm['tenant_id']+"\", user_id=\""+vm['user_id']+"\", name=\""+vm['name']+"\", image_id=\""+vm['image']['id']+"\"} " + string2int(vm['status']) + '\n'
    data += vm_update + vm_pow_state + vm_status

    logger.info('Post vm metrics: \n'+data)
    for url in urls:
        pushdata(url,data,"vms",tenant_name)

def string2int(str_status):
    code = ""
    for i in str_status:
        ascii_code = ord(i)
        code += str(ascii_code)
    return code 

def date2int(str_date):
    date = datetime.datetime.strptime(str_date,"%Y-%m-%dT%H:%M:%SZ")
    return  time.mktime(date.timetuple())

def getStates(vms):
    states ={}
    for vm in vms:
        if vm['status'] in states:
            states[vm['status']] += 1
        else:
            states[vm['status']] = 1
    return states
    
if __name__ == "__main__":
    print "Openstack Data Collector"
    init()
    for tenant in tenants:
        token = getTokenv3(tenant)
        limits = getLimits(token)
        postLimits(limits, tenant["name"], tenant["pushgw_url"])
        vms = getVms(token)
        postVMmetrics(vms['servers'], tenant["name"], tenant["pushgw_url"])
        
