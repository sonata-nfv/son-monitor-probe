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


import threading,json,time
import requests
from prompw import Pusher

class vnf_monitor(object):

    def __init__(self, prom_pw_url_, vnf_stats_url_, interval_, logger_):
        self.pushgateway = prom_pw_url_
        self.vnf_endpoid = vnf_stats_url_
        self.interval = interval_
        self.logger = logger_
        self.stop_thread = False
        self.timer = threading.Thread(target=self.collectStats,
                                      args=(int(self.interval), lambda: self.stop_thread))
        self.timer.daemon = True
        self.timer.run()
        self.logger.info('Thread created...')

    def stopThread(self):
        self.stop_thread = True
        self.timer.join()

    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def sendStats(self, dt, resp, ip, port):
        if not 'resource_id' in dt:
            self.logger.error('Response does not contains "resource_id":' + str(resp.text))
        else:
            rsc_id = dt['resource_id']
            del dt['resource_id']
            ps = Pusher(pw_url_=self.pushgateway, node_name_=rsc_id, id_=rsc_id,
                        logger_=self.logger)
            for mt in dt:
                ps.sendGauge(metric=mt.replace('-', '_'),
                            description='', value=dt[mt],
                            job='mon_container', labels={'ip': ip, 'port': port})
                self.logger.info('Metric '+mt+' Pushed')
            print(dt)

    def collectStats(self,interval_, stop_):
        lastclick = None
        while True:
            self.logger.info('============')
            nowclick = int(round(time.time() * 1000))
            if lastclick:
                self.logger.info('actual interval ' + str(nowclick - lastclick))
            lastclick = nowclick
            try:
                resp = requests.get(self.vnf_endpoid)
                sc = self.vnf_endpoid.split('/')[2]
                ip = sc.split(':')[0]
                port = sc.split(':')[1]
                if resp.status_code == 200:
                    try:
                        dt_object = resp.json()
                        if isinstance(dt_object, list):
                            for dt in dt_object:
                                if dt:
                                    self.sendStats(dt, resp, ip, port)
                        elif isinstance(dt_object, dict):
                            self.sendStats(dt_object, resp, ip, port)
                        else:
                            raise self.logger.error("Invalid data format")
                    except ValueError:
                        self.logger.error('Response is not hedjson format:' + str(resp.text))
                else:
                    self.logger.error('Response code error:' + str(resp.status_code))

            except requests.exceptions.RequestException:
                self.logger.error('Exception on request')

            if stop_():
                break
            time.sleep(self.interval)