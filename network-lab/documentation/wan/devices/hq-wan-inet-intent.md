
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

ip domain name iwan.lab
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
