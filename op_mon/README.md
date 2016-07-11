#son-vim-openstack-probe
Sonata's vim (openstack) monitoring client is used in order to gather monitoring data from VIM and push them to monitoring server. 

Supported monitoring metrics are:
 * Total/used Cores
 * Total/used Instances
 * Total/used RAM size
 * Total/used Floating IPs

### Dependencies
 * python 2.7

###Run monitoring probe:

From code

a. Set configuration file (odc.conf)

```
[Openstack]
controller_ip: 127.0.0.1
keystone_url: http://192.168.1.231:5000/v2.0/tokens
tenants: [{"name":"tent_name", "user_name": "admin", "password":"admin_pass"}]
node_name: vim_mane

[Prometheus]
server_url: http://pushgateway:9091/metrics
``` 

b. Execute the probe
  
```
sudo pyhton opensdatacollector.py
```


###Lead Developers
The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas (trakadasp)
 * Panos Karkazis (pkarkazis)
