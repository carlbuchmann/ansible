# WAN Detailed design

## Logical Topology

![Alt text](diagrams/logical_network_topology.jpg?raw=true "Logical Network Topology")

## WAN Router Device Intent Configuration

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

### Running Configuration

```

hostname branch1-wan

ntp server 172.20.5.101

ip domain name homelab.lab
!
ip multicast-routing distributed
!
snmp-server community LAB@APICEMro RO
snmp-server community LAB@APICEMrw RW
snmp-server trap-source Loopback0
snmp ifmib ifindex persist

cdp run

key chain MPLS-WAN-KEY
 key 1
  key-string mpls-wan@154
key chain INET-WAN-KEY
 key 1
  key-string inet-wan@154

key chain LAN-KEY
 key 1
  key-string eigrp@LAN

crypto ikev2 keyring DMVPN-KEYRING
 peer ANY
  address 0.0.0.0 0.0.0.0
  pre-shared-key iWAN@lab#154

crypto ikev2 proposal AES/GCM/256
 encryption aes-gcm-256
 prf sha512
 group 19

crypto ikev2 policy AES/GCM/256
 match fvrf any
 proposal AES/GCM/256

crypto ikev2 profile DMVPN-IKEv2-PROFILE
 description PSK-Profile
 match fvrf any
 match identity remote address 0.0.0.0
 identity local address 172.21.255.1
 authentication local pre-share
 authentication remote pre-share
 keyring local DMVPN-KEYRING
 dpd 40 5 on-demand
 

crypto ipsec transform-set AES256/GCM/TRANSFORM esp-gcm 256
 mode transport

crypto ipsec profile DMVPN-IPSEC-PROFILE
 set transform-set AES256/GCM/TRANSFORM
 set ikev2-profile DMVPN-IKEv2-PROFILE

crypto ipsec security-association replay window-size 1024 
interface Loopback0
 no shutdown
 description mgmt
 ip address 172.21.255.1 255.255.255.255
interface Tunnel10
 no shutdown
 description dmvpn_mpls_1
 bandwidth 100000
 ip address 172.16.101.21 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip tcp adjust-mss 1360
 hold-queue 4096 in
 hold-queue 4096 out
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 101
 tunnel vrf IWAN-MPLS-1
 tunnel protection ipsec profile DMVPN-IPSEC-PROFILE
 ip nhrp authentication LABmpls1
 ip nhrp network-id 101
 ip nhrp nhs 172.16.101.1 nbma 10.255.20.2 multicast
 if-state nhrp
 
 no nhrp route-watch
 delay 1000
 cdp enable
interface Tunnel11
 no shutdown
 description dmvpn_inet_1
 bandwidth 250000
 ip address 172.16.102.21 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip tcp adjust-mss 1360
 hold-queue 4096 in
 hold-queue 4096 out
 tunnel source GigabitEthernet3
 tunnel mode gre multipoint
 tunnel key 102
 tunnel vrf IWAN-INET-1
 tunnel protection ipsec profile DMVPN-IPSEC-PROFILE
 ip nhrp authentication LABinet1
 ip nhrp network-id 102
 ip nhrp nhs 172.16.102.1 nbma 192.168.20.2 multicast
 if-state nhrp
 
 no nhrp route-watch
 delay 2000
 cdp enable
interface GigabitEthernet2
 no shutdown
 description mpls_provider
 bandwidth 100000
 ip vrf forwarding IWAN-MPLS-1
 ip address 10.255.21.2 255.255.255.252
 
 
 hold-queue 4096 in
 hold-queue 4096 out
interface GigabitEthernet3
 no shutdown
 description inet_provider
 bandwidth 250000
 ip vrf forwarding IWAN-INET-1
 ip address 192.168.21.2 255.255.255.252
 
 
 hold-queue 4096 in
 hold-queue 4096 out
interface GigabitEthernet4
 no shutdown
 description branch1-core_ge0/1
 ip address 172.21.0.1 255.255.255.252
 
 
 delay 24000
 
 cdp enable
router eigrp ENTERPRISE-EIGRP
 address-family ipv4 unicast autonomous-system 100
  af-interface default
   passive-interface
  exit-af-interface
  topology base
   summary-metric 172.21.0.0/16 1000000 10000 255 1 1500
  exit-af-topology
  network 172.21.0.0 0.0.0.3
  af-interface GigabitEthernet4
   no passive-interface
   authentication mode md5
   authentication key-chain LAN-KEY
  exit-af-interface
  af-interface Tunnel10
   summary-address 172.21.0.0 255.255.0.0
   authentication mode md5
   authentication key-chain MPLS-WAN-KEY
   hello-interval 20
   hold-time 60
   no passive-interface
   stub-site wan-interface
  exit-af-interface
  network 172.16.101.0 0.0.0.255
  af-interface Tunnel11
   summary-address 172.21.0.0 255.255.0.0
   authentication mode md5
   authentication key-chain INET-WAN-KEY
   hello-interval 20
   hold-time 60
   no passive-interface
   stub-site wan-interface
  exit-af-interface
  network 172.16.102.0 0.0.0.255
  eigrp router-id 172.21.255.1
ip vrf IWAN-MPLS-1
 rd 65511:101
 
ip vrf IWAN-INET-1
 rd 65511:102
 
ip route vrf IWAN-MPLS-1 0.0.0.0 0.0.0.0 10.255.21.1 name mpls-default
 
ip route vrf IWAN-INET-1 0.0.0.0 0.0.0.0 192.168.21.1 name inet-default
```

___

## branch2-wan

### Interfaces

* **LAN Interfaces**

| interface     | description  | ip address   |
| ------------- | ------------ | ------------ |
| GigabitEthernet4 | branch2-lan_ge0/1 |  N/A |
| GigabitEthernet4.10 | data |  172.22.10.1/24 |
| GigabitEthernet4.11 | voice |  172.22.11.1/24 |
| GigabitEthernet4.12 | guest |  172.22.12.1/24 |
| GigabitEthernet4.13 | wifi |  172.22.13.1/24 |
| GigabitEthernet4.99 | Cisco Gold Audit |  172.22.99.1/24 |

* **WAN Interfaces**

| interface     | description  | ip address   | bandwidth |
| ------------- | ------------ | ------------ | --------- |
| GigabitEthernet2 | mpls_provider | 10.255.22.2/30 | 100.0 |
| GigabitEthernet3 | inet_provider | 192.168.22.2/30 | 250.0 |

* **Tunnel Interfaces**

| interface     | profile      | ip address   | tunnel source |
| ------------- | -------------| ------------ | ------------- |
| Tunnel10 | dmvpn_mpls_1 | 172.16.101.22/24 | GigabitEthernet2 |
| Tunnel11 | dmvpn_inet_1 | 172.16.102.22/24 | GigabitEthernet3 |

### Routing

* **VRFs**

| VRF name | route distinguisher |
| -------- | ------------------- |
| IWAN-MPLS-1 |  65511:101 |
| IWAN-INET-1 |  65511:102 |

* **Static Routes**

| name | prefix | mask | forwarding router | vrf (if applicable) |
| ---- | ------ | ---- | ----------------- | ------------------- |
| mpls-default | 0.0.0.0 | 0.0.0.0 | 10.255.22.1 | IWAN-MPLS-1 | 
| inet-default | 0.0.0.0 | 0.0.0.0 | 192.168.22.1 | IWAN-INET-1 | 

### Running Configuration

```

hostname branch2-wan

ntp server 172.20.5.101

ip domain name homelab.lab
!
ip multicast-routing distributed
!
snmp-server community LAB@APICEMro RO
snmp-server community LAB@APICEMrw RW
snmp-server trap-source Loopback0
snmp ifmib ifindex persist

cdp run

key chain MPLS-WAN-KEY
 key 1
  key-string mpls-wan@154
key chain INET-WAN-KEY
 key 1
  key-string inet-wan@154


crypto ikev2 keyring DMVPN-KEYRING
 peer ANY
  address 0.0.0.0 0.0.0.0
  pre-shared-key iWAN@lab#154

crypto ikev2 proposal AES/GCM/256
 encryption aes-gcm-256
 prf sha512
 group 19

crypto ikev2 policy AES/GCM/256
 match fvrf any
 proposal AES/GCM/256

crypto ikev2 profile DMVPN-IKEv2-PROFILE
 description PSK-Profile
 match fvrf any
 match identity remote address 0.0.0.0
 identity local address 172.22.255.1
 authentication local pre-share
 authentication remote pre-share
 keyring local DMVPN-KEYRING
 dpd 40 5 on-demand
 

crypto ipsec transform-set AES256/GCM/TRANSFORM esp-gcm 256
 mode transport

crypto ipsec profile DMVPN-IPSEC-PROFILE
 set transform-set AES256/GCM/TRANSFORM
 set ikev2-profile DMVPN-IKEv2-PROFILE

crypto ipsec security-association replay window-size 1024 
interface Loopback0
 no shutdown
 description mgmt
 ip address 172.22.255.1 255.255.255.255
interface Tunnel10
 no shutdown
 description dmvpn_mpls_1
 bandwidth 100000
 ip address 172.16.101.22 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip tcp adjust-mss 1360
 hold-queue 4096 in
 hold-queue 4096 out
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 101
 tunnel vrf IWAN-MPLS-1
 tunnel protection ipsec profile DMVPN-IPSEC-PROFILE
 ip nhrp authentication LABmpls1
 ip nhrp network-id 101
 ip nhrp nhs 172.16.101.1 nbma 10.255.20.2 multicast
 if-state nhrp
 
 no nhrp route-watch
 delay 1000
 cdp enable
interface Tunnel11
 no shutdown
 description dmvpn_inet_1
 bandwidth 250000
 ip address 172.16.102.22 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip tcp adjust-mss 1360
 hold-queue 4096 in
 hold-queue 4096 out
 tunnel source GigabitEthernet3
 tunnel mode gre multipoint
 tunnel key 102
 tunnel vrf IWAN-INET-1
 tunnel protection ipsec profile DMVPN-IPSEC-PROFILE
 ip nhrp authentication LABinet1
 ip nhrp network-id 102
 ip nhrp nhs 172.16.102.1 nbma 192.168.20.2 multicast
 if-state nhrp
 
 no nhrp route-watch
 delay 2000
 cdp enable
interface GigabitEthernet2
 no shutdown
 description mpls_provider
 bandwidth 100000
 ip vrf forwarding IWAN-MPLS-1
 ip address 10.255.22.2 255.255.255.252
 
 
 hold-queue 4096 in
 hold-queue 4096 out
interface GigabitEthernet3
 no shutdown
 description inet_provider
 bandwidth 250000
 ip vrf forwarding IWAN-INET-1
 ip address 192.168.22.2 255.255.255.252
 
 
 hold-queue 4096 in
 hold-queue 4096 out
interface GigabitEthernet4
 no shutdown
 description branch2-lan_ge0/1
 no ip address
 
 
 
 cdp enable
interface GigabitEthernet4.10
 no shutdown
 description data
 encapsulation dot1Q 10
 ip address 172.22.10.1 255.255.255.0
 ip helper-address 172.22.10.11
 ip helper-address 172.22.10.12
 ip helper-address 172.22.10.13
 
 
 
 cdp enable
interface GigabitEthernet4.11
 no shutdown
 description voice
 encapsulation dot1Q 11
 ip address 172.22.11.1 255.255.255.0
 ip helper-address 172.22.10.11
 ip helper-address 172.22.10.12
 ip helper-address 172.22.10.13
 
 
 
 cdp enable
interface GigabitEthernet4.12
 no shutdown
 description guest
 encapsulation dot1Q 12
 ip address 172.22.12.1 255.255.255.0
 ip helper-address 172.22.10.11
 ip helper-address 172.22.10.12
 ip access-group acl-guest in
 
 
 
 cdp enable
interface GigabitEthernet4.13
 no shutdown
 description wifi
 encapsulation dot1Q 13
 ip address 172.22.13.1 255.255.255.0
 ip helper-address 172.20.5.11
 ip helper-address 172.20.5.12
 ip access-group acl-wifi in
 
 
 
 cdp enable
interface GigabitEthernet4.99
 no shutdown
 description Cisco Gold Audit
 encapsulation dot1Q 10
 ip address 172.22.99.1 255.255.255.0
 ip helper-address 172.22.10.11
 ip helper-address 172.22.10.12
 ip helper-address 172.22.10.13
 
 
 
 cdp enable
router eigrp ENTERPRISE-EIGRP
 address-family ipv4 unicast autonomous-system 100
  af-interface default
   passive-interface
  exit-af-interface
  topology base
   summary-metric 172.22.0.0/16 1000000 10000 255 1 1500
  exit-af-topology
  network 172.22.10.0 0.0.0.255
  network 172.22.11.0 0.0.0.255
  network 172.22.12.0 0.0.0.255
  network 172.22.13.0 0.0.0.255
  network 172.22.99.0 0.0.0.255
  af-interface Tunnel10
   summary-address 172.22.0.0 255.255.0.0
   authentication mode md5
   authentication key-chain MPLS-WAN-KEY
   hello-interval 20
   hold-time 60
   no passive-interface
   stub-site wan-interface
  exit-af-interface
  network 172.16.101.0 0.0.0.255
  af-interface Tunnel11
   summary-address 172.22.0.0 255.255.0.0
   authentication mode md5
   authentication key-chain INET-WAN-KEY
   hello-interval 20
   hold-time 60
   no passive-interface
   stub-site wan-interface
  exit-af-interface
  network 172.16.102.0 0.0.0.255
  eigrp router-id 172.22.255.1
ip vrf IWAN-MPLS-1
 rd 65511:101
 
ip vrf IWAN-INET-1
 rd 65511:102
 
ip route vrf IWAN-MPLS-1 0.0.0.0 0.0.0.0 10.255.22.1 name mpls-default
 
ip route vrf IWAN-INET-1 0.0.0.0 0.0.0.0 192.168.22.1 name inet-default
```

___

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

```

hostname hq-wan-inet

ntp server 172.20.5.101

ip domain name homelab.lab
!
ip multicast-routing distributed
!
snmp-server community LAB@APICEMro RO
snmp-server community LAB@APICEMrw RW
snmp-server trap-source Loopback0
snmp ifmib ifindex persist

cdp run

key chain MPLS-WAN-KEY
 key 1
  key-string mpls-wan@154
key chain INET-WAN-KEY
 key 1
  key-string inet-wan@154

key chain LAN-KEY
 key 1
  key-string eigrp@LAN

crypto ikev2 keyring DMVPN-KEYRING
 peer ANY
  address 0.0.0.0 0.0.0.0
  pre-shared-key iWAN@lab#154

crypto ikev2 proposal AES/GCM/256
 encryption aes-gcm-256
 prf sha512
 group 19

crypto ikev2 policy AES/GCM/256
 match fvrf any
 proposal AES/GCM/256

crypto ikev2 profile DMVPN-IKEv2-PROFILE
 description PSK-Profile
 match fvrf any
 match identity remote address 0.0.0.0
 identity local address 172.20.255.2
 authentication local pre-share
 authentication remote pre-share
 keyring local DMVPN-KEYRING
 

crypto ipsec transform-set AES256/GCM/TRANSFORM esp-gcm 256
 mode transport

crypto ipsec profile DMVPN-IPSEC-PROFILE
 set transform-set AES256/GCM/TRANSFORM
 set ikev2-profile DMVPN-IKEv2-PROFILE

crypto ipsec security-association replay window-size 1024 
interface Loopback0
 no shutdown
 description mgmt
 ip address 172.20.255.2 255.255.255.252
interface Tunnel11
 no shutdown
 description dmvpn_inet_1
 bandwidth 100000
 ip address 172.16.102.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip tcp adjust-mss 1360
 hold-queue 4096 in
 hold-queue 4096 out
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 102
 tunnel vrf IWAN-INET-1
 tunnel protection ipsec profile DMVPN-IPSEC-PROFILE
 ip nhrp authentication LABinet1
 ip nhrp network-id 102
 ip nhrp redirect
 ip pim nbma-mode
 
 delay 2000
 cdp enable
interface GigabitEthernet2
 no shutdown
 description inet_provider_ge0/5
 bandwidth 500000
 ip vrf forwarding IWAN-INET-1
 ip address 192.168.20.2 255.255.255.252
 
 
 hold-queue 4096 in
 hold-queue 4096 out
interface GigabitEthernet3
 no shutdown
 description hq-core_ge0/3
 ip address 172.20.0.5 255.255.255.252
 
 
 delay 24000
 
 cdp enable
router eigrp ENTERPRISE-EIGRP
 address-family ipv4 unicast autonomous-system 100
  af-interface default
   passive-interface
  exit-af-interface
  topology base
   summary-metric 172.20.0.0/16 1000000 10000 255 1 1500
  exit-af-topology
  network 172.20.0.4 0.0.0.3
  af-interface GigabitEthernet3
   no passive-interface
   authentication mode md5
   authentication key-chain LAN-KEY
  exit-af-interface
  af-interface Tunnel11
   summary-address 172.20.0.0 255.255.0.0
   authentication mode md5
   authentication key-chain INET-WAN-KEY
   hello-interval 20
   hold-time 60
   no passive-interface
   no split-horizon
  exit-af-interface
  network 172.16.102.0 0.0.0.255
  eigrp router-id 172.20.255.2
ip vrf IWAN-INET-1
 rd 65511:102
 
ip route vrf IWAN-INET-1 0.0.0.0 0.0.0.0 192.168.20.1 name inet-default
```

___

## hq-wan-mpls

### Interfaces

* **LAN Interfaces**

| interface     | description  | ip address   |
| ------------- | ------------ | ------------ |
| GigabitEthernet3 | hq-core_ge0/2 |  172.20.0.1/30 |

* **WAN Interfaces**

| interface     | description  | ip address   | bandwidth |
| ------------- | ------------ | ------------ | --------- |
| GigabitEthernet2 | mpls_provider_ge0/2 | 10.255.20.2/30 | 500.0 |

* **Tunnel Interfaces**

| interface     | profile      | ip address   | tunnel source |
| ------------- | -------------| ------------ | ------------- |
| Tunnel10 | dmvpn_mpls_1 | 172.16.101.1/24 | GigabitEthernet2 |

### Routing

* **VRFs**

| VRF name | route distinguisher |
| -------- | ------------------- |
| IWAN-MPLS-1 |  65511:101 |

* **Static Routes**

| name | prefix | mask | forwarding router | vrf (if applicable) |
| ---- | ------ | ---- | ----------------- | ------------------- |
| mpls-default | 0.0.0.0 | 0.0.0.0 | 10.255.20.1 | IWAN-MPLS-1 | 

### Running Configuration

```

hostname hq-wan-mpls

ntp server 172.20.5.101

ip domain name homelab.lab
!
ip multicast-routing distributed
!
snmp-server community LAB@APICEMro RO
snmp-server community LAB@APICEMrw RW
snmp-server trap-source Loopback0
snmp ifmib ifindex persist

cdp run

key chain MPLS-WAN-KEY
 key 1
  key-string mpls-wan@154
key chain INET-WAN-KEY
 key 1
  key-string inet-wan@154

key chain LAN-KEY
 key 1
  key-string eigrp@LAN

crypto ikev2 keyring DMVPN-KEYRING
 peer ANY
  address 0.0.0.0 0.0.0.0
  pre-shared-key iWAN@lab#154

crypto ikev2 proposal AES/GCM/256
 encryption aes-gcm-256
 prf sha512
 group 19

crypto ikev2 policy AES/GCM/256
 match fvrf any
 proposal AES/GCM/256

crypto ikev2 profile DMVPN-IKEv2-PROFILE
 description PSK-Profile
 match fvrf any
 match identity remote address 0.0.0.0
 identity local address 172.20.255.1
 authentication local pre-share
 authentication remote pre-share
 keyring local DMVPN-KEYRING
 

crypto ipsec transform-set AES256/GCM/TRANSFORM esp-gcm 256
 mode transport

crypto ipsec profile DMVPN-IPSEC-PROFILE
 set transform-set AES256/GCM/TRANSFORM
 set ikev2-profile DMVPN-IKEv2-PROFILE

crypto ipsec security-association replay window-size 1024 
interface Loopback0
 no shutdown
 description mgmt
 ip address 172.20.255.1 255.255.255.252
interface Tunnel10
 no shutdown
 description dmvpn_mpls_1
 bandwidth 100000
 ip address 172.16.101.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip tcp adjust-mss 1360
 hold-queue 4096 in
 hold-queue 4096 out
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 101
 tunnel vrf IWAN-MPLS-1
 tunnel protection ipsec profile DMVPN-IPSEC-PROFILE
 ip nhrp authentication LABmpls1
 ip nhrp network-id 101
 ip nhrp redirect
 ip pim nbma-mode
 
 delay 1000
 cdp enable
interface GigabitEthernet2
 no shutdown
 description mpls_provider_ge0/2
 bandwidth 500000
 ip vrf forwarding IWAN-MPLS-1
 ip address 10.255.20.2 255.255.255.252
 
 
 hold-queue 4096 in
 hold-queue 4096 out
interface GigabitEthernet3
 no shutdown
 description hq-core_ge0/2
 ip address 172.20.0.1 255.255.255.252
 
 
 delay 24000
 
 cdp enable
router eigrp ENTERPRISE-EIGRP
 address-family ipv4 unicast autonomous-system 100
  af-interface default
   passive-interface
  exit-af-interface
  topology base
   summary-metric 172.20.0.0/16 1000000 10000 255 1 1500
  exit-af-topology
  network 172.20.0.0 0.0.0.3
  af-interface GigabitEthernet3
   no passive-interface
   authentication mode md5
   authentication key-chain LAN-KEY
  exit-af-interface
  af-interface Tunnel10
   summary-address 172.20.0.0 255.255.0.0
   authentication mode md5
   authentication key-chain MPLS-WAN-KEY
   hello-interval 20
   hold-time 60
   no passive-interface
   no split-horizon
  exit-af-interface
  network 172.16.101.0 0.0.0.255
  eigrp router-id 172.20.255.1
ip vrf IWAN-MPLS-1
 rd 65511:101
 
ip route vrf IWAN-MPLS-1 0.0.0.0 0.0.0.0 10.255.20.1 name mpls-default
```

___
