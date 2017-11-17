## branch2-wan - Intent Configuration


### LAN Interfaces

| interface     | description  | ip address   |
| ------------- | -------------| ------------ |
| GigabitEthernet4 | branch2-lan_ge0/1 |  N/A |
| GigabitEthernet4.10 | data |  172.22.10.1/24 |
| GigabitEthernet4.11 | voice |  172.22.11.1/24 |
| GigabitEthernet4.12 | guest |  172.22.12.1/24 |
| GigabitEthernet4.13 | wifi |  172.22.13.1/24 |

### WAN Interfaces

| interface     | description  | ip address   | bandwidth |
| ------------- | -------------| ------------ |---------- |
| GigabitEthernet2 | mpls_provider | 10.255.22.2/30 | 100000 |
| GigabitEthernet3 | inet_provider | 192.168.22.2/30 | 250000 |
