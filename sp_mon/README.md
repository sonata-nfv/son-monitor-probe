#son-service-platform-probe
Sonata's Service platform monitoring client is used in order to gather monitoring data from VM and containers which hosts sonatas servives and push them to monitoring server. 

Supported monitoring metrics are:
 * cpu usage
 * memory usage
 * disk usage 
 * network traffic

### Development
To contribute to the development of the SONATA monitoring probes you have to fork the repository, commit new code and create pull requests.

### Dependencies
 * python 2.7
 * docker-engine 1.10.2

### Installation

Build container
```
sudo docker build -t son-sp-mon .
```

Run monitoring probe as container
```
sudo docker run --net="host" -e "NODE_NAME=INT-SRV-1" -e "PROM_SRV=http://sp.int2.sonata-nfv.eu:9091/metrics" --privileged=true -d -v /var/run/docker.sock:/var/run/docker.sock -v /proc:/myhost/proc -v /:/rootfs:ro son-sp-mon
```

## License
This son-sp-probe is published under Apache 2.0 license. Please see the LICENSE file for more details.

###Lead Developers
The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas  (trakadasp)
 * Panos Karkazis  (pkarkazis)

 #### Feedback-Chanel
* You may use the mailing list sonata-dev@lists.atosresearch.eu
* Please use the GitHub issues to report bugs.
