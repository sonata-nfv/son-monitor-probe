# CNF monitoring container 

[5GTango](http://5gtango.eu)/[Sonata](http://sonata-nfv.eu) 


## Development
To contribute to the development of the monitoring probes you have to fork the repository, commit new code and create pull requests.

### Dependencies
 * python 3
 * prometheus-client
 * requests


## Installation

Build container
```
sudo docker build -f cnf_mon/Dockerfile -t tng-stats-collector .
```

Run monitoring probe as container
```
sudo docker run -d  -e "VNF_STATS_URL=http://<ip>:<port>" -e "PW_URL=<ip>:<port>" -e "INTERVAL=2" --name tng-stats-coll tng-stats-collector
```

## License

This implemantation is published under Apache 2.0 license. Please see the LICENSE file for more details.


#### Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas  (trakadasp)
 * Panos Karkazis  (pkarkazis)

#### Feedback-Chanel

* Please use the GitHub issues to report bugs.
