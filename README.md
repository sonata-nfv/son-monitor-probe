# son-monitor-probe  [![Build Status](http://jenkins.sonata-nfv.eu/buildStatus/icon?job=son-monitor-probe)](http://jenkins.sonata-nfv.eu/job/son-monitor-probe) 

Sonata's monitoring system provides three probes for collecting data from: 
 * Service Platform infrastucture (sp_mon)
 * VNFs (vm_mon)
 * VIMs (op_mon)

More detailed information about installation, dependencies etc are available in README files of each probe. 

## Development
To contribute to the development of the SONATA monitoring probes you have to fork the repository, commit new code and create pull requests.

## License
SONATA mmonitoring probes are published under Apache 2.0 license. Please see the LICENSE file for more details.


#### Lead Developers
The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas  (trakadasp)
 * Panos Karkazis  (pkarkazis)

####  Feedback-Chanel
* You may use the mailing list sonata-dev@lists.atosresearch.eu
* Please use the GitHub issues to report bugs.
##
## Some general information regarding this
## VNF descriptor.
##
descriptor_version: "vnfd-schema-01"
vendor: "nginx"
name: "nginx"
version: "0.11"
author: "Thomas Soenen @imec"
description: "nginx VNF"
##
## The virtual deployment unit.
##
virtual_deployment_units:
  - id: "vdu01"
    vm_image: "http://www.google.com"
    vm_image_format: "qcow2"
    vm_image_md5: '56e826bdbf2a3f9af2a38dc750b70f8b'
    resource_requirements:
      cpu:
        vcpus: 1
      memory:
        size: 1
        size_unit: "GB"
      storage:
        size: 20
        size_unit: "GB"
    monitoring_parameters:
	- name: "active_connections"
    	unit: "bps"
    connection_points:
      - id: "mgmt"
        interface: "ipv4"
        type: "management"
      - id: "cpinout"
        interface: "ipv4"
        type: "internal"
    

## The virtual links that interconnect
## the different connections points.
##
virtual_links:
  - id: "mgmt"
    connectivity_type: "E-LAN"
    connection_points_reference:
      - "vdu01:mgmt"
      - "cpmgmt"
  - id: "inout"
    connectivity_type: "E-Line"
    connection_points_reference:
      - "vdu01:cpinout"
      - "cpinout"

##
## The VNF connection points to the
## outside world.
##
connection_points:
  - id: "cpmgmt"
    interface: "ipv4"
    type: "management"
  - id: "cpinout"
    interface: "ipv4"
    type: "internal"

monitoring_rules:
  - name: "mon:rule:active_connections"
    description: "Trigger events if active connections are greater than threshold."
    duration: 1
    duration_unit: "s"
    condition: "vdu01:active_connections > 10"
    notification:
      - name: "notification01"
        type: "rabbitmq_message"

# function_specific_managers:
#  - id: "sonfsmplugtestnginxcss1"
#    description: "FSM to do a first FSM test"
#    image: "tsoenen/nginx"
#    options:
#      - key: "type"
#        value: "start"