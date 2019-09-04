# Service platform probe
[5GTango](http://5gtango.eu)/[Sonata](http://sonata-nfv.eu) service platform monitoring client is used in order to gather monitoring data from VM and containers which hosts 5GTango/Sonata services and push them to the monitoring server. 

Among the monitoring metrics supported by the probe are:
 * cpu usage
 * memory usage
 * disk usage 
 * network traffic

## Installing / Getting started

Build container
```
sudo docker build -t son-sp-mon .
```

Run monitoring probe as container
```
sudo docker run --net="host" -e "NODE_NAME=INT-SRV-1" -e "PROM_SRV=http://sp.int2.sonata-nfv.eu:9091/metrics" --privileged=true -d -v /var/run/docker.sock:/var/run/docker.sock -v /proc:/myhost/proc -v /:/rootfs:ro son-sp-mon
```

## Developing

To contribute to the development of the monitoring probes you have to fork the repository, commit new code and create pull requests.

### Built With

 * python 2.7
 * docker-engine 1.10.2


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
