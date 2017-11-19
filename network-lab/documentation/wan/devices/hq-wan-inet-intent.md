
## hq-wan-inet

### Interfaces

* **LAN Interfaces**

| interface     | description  | ip address   |
| ------------- | ------------ | ------------ |
| GigabitEthernet3 | hq-core_ge0/3 |  172.20.0.5/30 |

* **WAN Interfaces**

| interface     | description  | ip address   | bandwidth |
| ------------- | ------------ | ------------ | --------- |
| GigabitEthernet2 | inet_provider_ge0/5 | 192.168.20.2/30 | 500.0 |

* **Tunnel Interfaces**

| interface     | profile      | ip address   | tunnel source |
| ------------- | -------------| ------------ | ------------- |
| Tunnel11 | dmvpn_inet_1 | 172.16.102.1/24 | GigabitEthernet2 |

### Routing

* **VRFs**

| VRF name | route distinguisher |
| -------- | ------------------- |
| IWAN-INET-1 |  65511:102 |

* **Static Routes**

| name | prefix | mask | forwarding router | vrf (if applicable) |
| ---- | ------ | ---- | ----------------- | ------------------- |
| inet-default | 0.0.0.0 | 0.0.0.0 | 192.168.20.1 | IWAN-INET-1 | 

### Running Configuration

```./configurations/wan/hq-wan-inet.cfg```

___
