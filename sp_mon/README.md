#son-service-platform-probe
Sonata's Service platform monitoring client is used in order to gather monitoring data from VM and containers which hosts sonatas servives and push them to monitoring server. 


Supported monitoring metrics are:
 * cpu usage
 * memory usage
 * disk usage 
 * network traffic

### Dependencies
 * python 2.7
 * docker-engine 1.10.2

Build container container
```
sudo docker build -t son-sp-mon .
```

Run monitoring probe as container
```
sudo docker run -e "NODE_NAME=INT-SRV-1" -e "PROM_SRV=http://sp.int2.sonata-nfv.eu:9091/metrics" --privileged=true -d -v /var/run/docker.sock:/var/run/docker.sock -v /proc:/myhost/proc son-sp-mon
```

###Lead Developers
The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas (trakadasp)
 * Panos Karkazis (pkarkazis)
