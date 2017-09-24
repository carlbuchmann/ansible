# Network-Lab
# ! Work Under Development !

This repository contains Ansible scripts I'm developing in a lab environment using Cisco VIRL to fully automate an enterprise network WAN and LAN infrastructure.

* Current focus of the project is to automate the WAN topology based on Cisco's iWAN CVDs (published April 2017)

## Topology 

  * HQ:
    * hq-wan-mpls: csr-1000v
    * hq-wan-inet: csr-1000v
    * hq-mc: csr-1000v
    * hq-core: IOSv (planning to update to HA pair of NX-OS)
  * Branch1 (L3 site):
    * branch1-wanc: csr-1000v
    * branch1-core: IOSvL2
  * Branch2 (L2 Site):
    * branch2-wanc: csr-1000v
    * branch2-lan: IOSvL2
  * MPLS/INET Backbone
    * Provider: IOSv (planning to update to multiple IOS-XR with MPLS/BGP)
  

## Network Logical Topology

![Alt text](diagrams/logical_network_topology.jpg?raw=true "Logical Network Topology")
