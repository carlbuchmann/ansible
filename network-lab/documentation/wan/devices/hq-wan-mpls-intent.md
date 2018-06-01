
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
