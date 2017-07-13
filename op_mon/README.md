# son-vim-openstack-probe 

Sonata's vim monitoring client is used in order to gather monitoring data from VIM infrastructure (openstack) and push them to monitoring server 

Supported monitoring metrics are:
 * Total/used Cores
 * Total/used Instances
 * Total/used RAM size
 * Total/used Floating IPs

## Development
To contribute to the development of the SONATA monitoring probes you have to fork the repository, commit new code and create pull requests.

### Dependencies
 * python 2.7


## Installation
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

## License

This son-vim-probe is published under Apache 2.0 license. Please see the LICENSE file for more details.

---
#### Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas  (trakadasp)
 * Panos Karkazis  (pkarkazis)

#### Feedback-Chanel

* You may use the mailing list sonata-dev@lists.atosresearch.eu
* Please use the GitHub issues to report bugs.
