# Network-Lab
# ! Work Under Development !

This repository contains Ansible scripts I'm developing in a lab environment using Cisco VIRL to fully automate an enterprise network infrastructure.

* Current focus of the project is to automate the WAN topology based on Cisco's iWAN CVDs (published April 2017)
  * For current project update: https://github.com/carlbuchmann/ansible/projects/1

## Topology 

  * HQ:
    * hq-wan-mpls: csr-1000v (mpls DMVPN hub)
    * hq-wan-inet: csr-1000v (inet DMVPN hub)
    * hq-mc: csr-1000v (pfr master controller - IOS CA root)
    * hq-core: IOSv (planning to update to redundant pair of NX-OS)
  * Branch1 (L3 site):
    * branch1-wanc: csr-1000v (wan edge - dual-transport inet+mpls)
    * branch1-core: IOSvL2 (LAN Core L3 enable)
  * Branch2 (L2 Site):
    * branch2-wan: csr-1000v (wan edge - dual-transport inet+mpls)
    * branch2-lan: IOSvL2 (LAN acces L2 only)
  * MPLS/INET Backbone
    * Provider: IOSv (planning to update to multiple IOS-XR with MPLS/BGP)
  

## Network Logical Topology

![Alt text](diagrams/logical_network_topology.jpg?raw=true "Logical Network Topology")


## Network Physical Topology (VIRL)
![Alt text](diagrams/physical_network_topology.jpg?raw=true "Logical Network Topology")
