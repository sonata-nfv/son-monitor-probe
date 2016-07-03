# son-vm-mon 
Sonata's VM monitoring client is used in order to gather monitoring data from VM's linux kernel (/proc/stat/, /proc/dev/net etc) and push them to monitoring server. 
The url of the pushgateway monitoring server must be set in node.conf file 

Supported monitoring metrics are:
 * cpu usage
 * memory usage
 * disk usage 
 * network traffic (transmitted bytes, received bytes, packets per second, bytes per second)

### Dependencies
 * python 2.7
 
Run monitoring probe:

a. From code
```
export PROM_SRV=http://pushgateway:9091/metrics
export NODE_NAME=VNF_1
sudo python sonmonprobe.py
```

b. Using container
```
sudo docker build -t son-vm-probe .
sudo docker run -d --name son-vm-probe -e NODE_NAME=VNF_1 -e PROM_SRV=http://pushgateway:9091/metrics --net="host" --privileged=true  -v /proc:/myhost/proc -v /:/rootfs:ro son-vm-probe
```

c. Using package
```
sudo pip install VmMonProbe
sudo python -c 'from vm_mon_probe import probe; probe().run("TEST_VNF_1","http://pushgateway.eu:9091/metrics")'
```

###Lead Developers
The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas (trakadasp)
 * Panos Karkazis (pkarkazis)
