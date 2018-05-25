## Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO [, ANY ADDITIONAL AFFILIATION]
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

import time, logging, os, json, subprocess
from configure import Configuration
from executer import Executer
from prompw import Pusher
from scheduler import Scheduler
from logging.handlers import RotatingFileHandler

def init():
    global prometh_server
    global node_name
    global interval
    global logger
    global vm_id
    global metric_list
    global pusher
    global job

    # read configuration
    interval = 3
    conf = Configuration("node.conf")
    node_name = os.getenv('NODE_NAME', conf.ConfigSectionMap("vm_node")['node_name'])
    job = 'vnf'#os.getenv('MON_JOB', conf.ConfigSectionMap("vm_node")['job'])
    prometh_server = os.getenv('PROM_SRV', conf.ConfigSectionMap("Prometheus")['server_url'])
    interval = conf.ConfigSectionMap("vm_node")['post_freq']

    metric_file=conf.ConfigSectionMap("metrics")['list']
    with open(metric_file) as f:
        metric_list = f.read()
        ml = is_json(metric_list)
        if ml[0]:
            metric_list = ml[1]
            print(metric_list)
        else:
            logger.warning('Metric list is not json object')
            logger.warning('Program exits')
            os._exit(1)

    if is_json(prometh_server):
        prometh_server = json.loads(prometh_server)
    else:
        prometh_server = [prometh_server]
    logger = logging.getLogger('dataCollector')
    hdlr = RotatingFileHandler('dataCollector.log', maxBytes=10000, backupCount=1)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    vm_id = getUUID()
    if vm_id == None:
        vm_id = node_name
    node_name += ":" + vm_id
    print(node_name)
    logger.info('SP Data Collector')
    logger.info('Promth P/W Server ' + json.dumps(prometh_server))
    logger.info('Monitoring Node ' + node_name)
    logger.info('Monitoring time interval ' + interval)

def getUUID():
    path = '/usr/sbin/dmidecode | grep UUID'
    if (os.path.isdir("/rootfs")):
        path = '/rootfs'+path
    lines = Executer(path).run_cmd()
    try:
        for line in lines:
            if 'UUID' in line:
                ar = line.split(" ")
                return ar[1].strip().lower()
    except:
        logger.warning('Error on retrieving UUID')
        return None
        pass

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError:
    return False, None
  return True, json_object

def is_float(num_):
    try:
        float(num_)
        return True
    except ValueError:
        return False

if __name__ == "__main__":

    init()

    servers = []
    for srv in prometh_server:
        pusher = Pusher(pw_url_=srv, node_name_=node_name, id_=vm_id)
        servers.append(pusher)
    print(len(servers))

    for mt in metric_list:
        if os.path.isfile('./metrics/'+mt['exec']):
            sc = Scheduler(metric_=mt,node_name_=node_name, id_=vm_id, job_=job, srvs_=servers, logger_=logger)
        else:
            logger.warning('Executable file not found')
            print ('file not found')
