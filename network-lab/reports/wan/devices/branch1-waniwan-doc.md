## branch1-wan - Intent Configuration


### LAN Interfaces

| interface     | description  | ip address   |
| ------------- | -------------| ------------ |
| GigabitEthernet4 | branch1-core_ge0/1 |  172.21.0.1/30 |

### WAN Interfaces

| interface     | description  | ip address   | bandwidth |
| ------------- | -------------| ------------ |---------- |
| GigabitEthernet2 | mpls_provider | 10.255.21.2/30 | 100000 |
| GigabitEthernet3 | inet_provider | 192.168.21.2/30 | 250000 |
