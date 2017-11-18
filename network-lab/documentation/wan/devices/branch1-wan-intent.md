
## branch1-wan

### Interfaces

* **LAN Interfaces**

| interface     | description  | ip address   |
| ------------- | ------------ | ------------ |
| GigabitEthernet4 | branch1-core_ge0/1 |  172.21.0.1/30 |

* **WAN Interfaces**

| interface     | description  | ip address   | bandwidth |
| ------------- | ------------ | ------------ | --------- |
| GigabitEthernet2 | mpls_provider | 10.255.21.2/30 | 100.0 |
| GigabitEthernet3 | inet_provider | 192.168.21.2/30 | 250.0 |

* **Tunnel Interfaces**

| interface     | profile      | ip address   | tunnel source |
| ------------- | -------------| ------------ | ------------- |
| Tunnel10 | dmvpn_mpls_1 | 172.16.101.21/24 | GigabitEthernet2 |
| Tunnel11 | dmvpn_inet_1 | 172.16.102.21/24 | GigabitEthernet3 |

### Routing

* **VRFs**

| VRF name | route distinguisher |
| -------- | ------------------- |
| IWAN-MPLS-1 |  65511:101 |
| IWAN-INET-1 |  65511:102 |

* **Static Routes**
 
| name | prefix | mask | forwarding router | vrf (if applicable) |
| ---- | ------ | ---- | ----------------- | ------------------- |
| mpls-default | 0.0.0.0 | 0.0.0.0 | 10.255.21.1 | IWAN-MPLS-1 | 
| inet-default | 0.0.0.0 | 0.0.0.0 | 192.168.21.1 | IWAN-INET-1 | 

_________________________________________________________________
