## branch2-wan

### Interfaces:

* LAN Interfaces:

| interface     | description  | ip address   |
| ------------- | ------------ | ------------ |
| GigabitEthernet4 | branch2-lan_ge0/1 |  N/A |
| GigabitEthernet4.10 | data |  172.22.10.1/24 |
| GigabitEthernet4.11 | voice |  172.22.11.1/24 |
| GigabitEthernet4.12 | guest |  172.22.12.1/24 |
| GigabitEthernet4.13 | wifi |  172.22.13.1/24 |

* WAN Interfaces:

| interface     | description  | ip address   | bandwidth |
| ------------- | ------------ | ------------ | --------- |
| GigabitEthernet2 | mpls_provider | 10.255.22.2/30 | 100.0 |
| GigabitEthernet3 | inet_provider | 192.168.22.2/30 | 250.0 |

* Tunnel Interfaces:

| interface     | profile      | ip address   | tunnel source |
| ------------- | -------------| ------------ | ------------- |
| Tunnel10 | dmvpn_mpls_1 | 172.16.101.22/24 | GigabitEthernet2 |
| Tunnel11 | dmvpn_inet_1 | 172.16.102.22/24 | GigabitEthernet3 |

### Routing:

* VRFs:

| VRF name | route distinguisher |
| -------- | ------------------- |
| IWAN-MPLS-1 |  65511:101 | 
| IWAN-INET-1 |  65511:102 | 

* Static routes:
 
| name | prefix | mask | forwarding router | vrf (if applicable) |
| ---- | ------ | ---- | ----------------- | ------------------- |
| mpls-default | 0.0.0.0 | 0.0.0.0 | 10.255.22.1 | IWAN-MPLS-1 | 
| inet-default | 0.0.0.0 | 0.0.0.0 | 192.168.22.1 | IWAN-INET-1 | 

_________________________________________________________________
