# VIM probe 

[5GTango](http://5gtango.eu)/[Sonata](http://sonata-nfv.eu) VIM monitoring client is used in order to gather monitoring data from VIM infrastructure (openstack) and push them to monitoring server. 

Among the monitoring metrics supported by the probe are:
 * Total/used Cores
 * Total/used Instances
 * Total/used RAM size
 * Total/used Floating IPs

## Installing / Getting started

From code

a. Set configuration file (odc.conf)

```
[Openstack]
controller_ip: <controller_ip>
keystone_url: http://<keystone_ip>:5000/v2.0/tokens
tenants:  [{"name": "admin","user_name": "name","password": "password","pushgw_url": ["http://<pushgateway>:<port>/metrics"]}]
node_name: pop_vim
``` 

b. Execute the probe
  
```
sudo pyhton opensdatacollector.py
```

## Developing
To contribute to the development of the monitoring probes you have to fork the repository, commit new code and create pull requests.

### Built With
 * python 2.7


### Submiting changes
To contribute to the development of the 5GTango/SONATA monitoring framwork you have to fork the repository, commit new code and create pull requests.

## Versioning
The most up-to-date version is v5.0.

## Licensing
Monitoring framework is published under Apache 2.0 license. Please see the LICENSE file for more details.

#### Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.
 
 * Panos Karkazis (pkarkazis)
 * Panos Trakadas (trakadasp)

#### Feedback-Chanel

* You may use the mailing list [sonata-dev-list](mailto:sonata-dev@lists.atosresearch.eu)
* You may use the GitHub issues to report bugs
