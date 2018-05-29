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

import threading,sys
from executer import Executer
from prompw import Pusher

class Scheduler(object):

    def __init__(self,metric_,job_,node_name_,id_,srvs_, logger_):
        self.metric = metric_
        self.job = job_
        self.pw_srvs =srvs_
        self.logger = logger_
        self.node_name = node_name_
        self.vm_id = id_
        self.run()

    def is_float(self, num_):
        try:
            float(num_)
            return True
        except ValueError:
            return False

    def run(self):
        try:
            resp = Executer("./metrics/"+self.metric['command']).run_cmd()
            for pusher in self.pw_srvs:
                if self.is_float(resp[0]):
                    pusher.sendGauge(metric=self.metric['name'], description=self.metric['description'], value=resp[0], job=self.job,
                                     labels=None)
                    self.logger.info('Metric ' + self.metric['name'] + ' pushed, value: '+resp[0])
                else:
                    pusher.remove_metric(metric=self.metric['name'],job=self.job)
                    self.logger.info('Metric ' + self.metric['name'] + ' removed, value: ' + resp[0])
        except Exception as e:
            self.logger.exception(e)
            print(str(e))
        except:
            self.logger.error("error on executing task: {0} ".format(sys.exc_info()[0]))
            print("General exception")
        timer = threading.Timer(interval=self.metric['interval'],function=self.run)
        timer.start()


if __name__ == "__main__":
    sc = Scheduler(metric_={'exec': 'ping.sh', 'type': 'gauge', 'name': 'ping', 'interval': 2, 'description': 'Check network connectivity in Layer 3',"command":"ping.sh 192.168.1.250"},
                   node_name_='testNode', id_=45678992,job_='vnf',srvs_=["192.168.1.127:9091"], logger_=None)
