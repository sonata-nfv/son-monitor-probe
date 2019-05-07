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

import logging,os
from logging.handlers import RotatingFileHandler
from statscollector import vnf_monitor


if __name__ == '__main__':
    logger = logging.getLogger('Monitoring Container')
    hdlr = RotatingFileHandler('monitoring.log', maxBytes=1000000, backupCount=1)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    prom_url = os.getenv('PW_URL', 'pushgateway.sonata.svc:9091')
    vnf_url = os.getenv('VNF_STATS_URL', None)
    interval = os.getenv('INTERVAL', 2)
    if (not prom_url) or (not vnf_url) or (not interval):
        print('PW_URL :'+str(prom_url))
        print('VNF_STATS_URL :' + str(vnf_url))
        print('INTERVAL :' + str(interval))
    else:
        vnf_monitor(prom_pw_url_=prom_url,vnf_stats_url_=vnf_url,interval_=int(interval), logger_=logger)
