# VM probe 
[5GTango](http://5gtango.eu)/[Sonata](http://sonata-nfv.eu) VM monitoring client is used in order to gather monitoring data from VM's linux kernel (/proc/stat/, /proc/dev/net etc) and push them to monitoring server. 
The url of the pushgateway monitoring server must be set in node.conf file 

Among the monitoring metrics supported by the probe are:
 * cpu usage
 * memory usage
 * disk usage 
 * network traffic (transmitted bytes, received bytes, packets per second, bytes per second)


### Installing / Getting started
a. From code
```
export PROM_SRV=http://<pushgateway>:<port>/metrics
export NODE_NAME=VNF_1
sudo python sonmonprobe.py
```

b. Using container
```
sudo docker build -t son-vm-probe .
sudo docker run -d --name son-vm-probe -e NODE_NAME=VNF_1 -e PROM_SRV=http://<pushgateway_ip>:<port>/metrics --net="host" --privileged=true  -v /proc:/myhost/proc -v /:/rootfs:ro son-vm-probe
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
