# IP address Filter

## issue with first IP address of subnet not yielding any results when using:
## "ip.address | ipaddr(loop.index0) | ipaddr('address')"

| Address | Available IP | Generated IP |
| ------- | ------------ | ------------ |
|10.0.0.0/24|first ip||
|10.0.0.0/24|second ip|10.0.0.1|
|10.0.0.0/24|third ip|10.0.0.2|
|10.1.0.128/25|first ip||
|10.1.0.128/25|second ip|10.1.0.129|
|10.1.0.128/25|third ip|10.1.0.130|
|192.168.0.128/30|first ip||
|192.168.0.128/30|second ip|192.168.0.129|
|192.168.0.128/30|third ip|192.168.0.130|
|192.168.0.128/30|fourth ip|192.168.0.131|
|192.168.0.128/30|fifth ip|False|

## the issue is actually with the second part of the filter "ipaddr('address')" it simply doesnt return the address if it's the network
## "ip.address | ipaddr(loop.index0) "

| Address | Available IP | Generated IP |
| ------- | ------------ | ------------ |
|10.0.0.0/24|first ip|10.0.0.0/24|
|10.0.0.0/24|second ip|10.0.0.1/24|
|10.0.0.0/24|third ip|10.0.0.2/24|
|10.1.0.128/25|first ip|10.1.0.128/25|
|10.1.0.128/25|second ip|10.1.0.129/25|
|10.1.0.128/25|third ip|10.1.0.130/25|
|192.168.0.128/30|first ip|192.168.0.128/30|
|192.168.0.128/30|second ip|192.168.0.129/30|
|192.168.0.128/30|third ip|192.168.0.130/30|
|192.168.0.128/30|fourth ip|192.168.0.131/30|
|192.168.0.128/30|fifth ip|False|


## try fix with using ipaddr('host') instead... same result not yielding any results for first IP of subnet:
## "ip.address | ipaddr(loop.index0) | ipaddr('host')"

| Address | Available IP | Generated IP |
| ------- | ------------ | ------------ |
|10.0.0.0/24|first ip||
|10.0.0.0/24|second ip|10.0.0.1/24|
|10.0.0.0/24|third ip|10.0.0.2/24|
|10.1.0.128/25|first ip||
|10.1.0.128/25|second ip|10.1.0.129/25|
|10.1.0.128/25|third ip|10.1.0.130/25|
|192.168.0.128/30|first ip||
|192.168.0.128/30|second ip|192.168.0.129/30|
|192.168.0.128/30|third ip|192.168.0.130/30|
|192.168.0.128/30|fourth ip|192.168.0.131/30|
|192.168.0.128/30|fifth ip|False|


## try fix with using ipaddr('ip') instead... same result not yielding any results for first IP of subnet:
## "ip.address | ipaddr(loop.index0) | ipaddr('ip')"

| Address | Available IP | Generated IP |
| ------- | ------------ | ------------ |
|10.0.0.0/24|first ip||
|10.0.0.0/24|second ip|10.0.0.1|
|10.0.0.0/24|third ip|10.0.0.2|
|10.1.0.128/25|first ip||
|10.1.0.128/25|second ip|10.1.0.129|
|10.1.0.128/25|third ip|10.1.0.130|
|192.168.0.128/30|first ip||
|192.168.0.128/30|second ip|192.168.0.129|
|192.168.0.128/30|third ip|192.168.0.130|
|192.168.0.128/30|fourth ip|192.168.0.131|
|192.168.0.128/30|fifth ip|False|

## fix using ipmath instead based of network:
## "ip.address | ipaddr('network') | ipmath(loop.index0)"
## But this doesn't provide error condition and might assign ip beyond subnet
## example fifth IP on /30 subnet should return false

| Address | Available IP | Generated IP |
| ------- | ------------ | ------------ |
|10.0.0.0/24|first ip|10.0.0.0|
|10.0.0.0/24|second ip|10.0.0.1|
|10.0.0.0/24|third ip|10.0.0.2|
|10.1.0.128/25|first ip|10.1.0.128|
|10.1.0.128/25|second ip|10.1.0.129|
|10.1.0.128/25|third ip|10.1.0.130|
|192.168.0.128/30|first ip|192.168.0.128|
|192.168.0.128/30|second ip|192.168.0.129|
|192.168.0.128/30|third ip|192.168.0.130|
|192.168.0.128/30|fourth ip|192.168.0.131|
|192.168.0.128/30|fifth ip|192.168.0.132|


## fix using conditonal, to provide error condition when IP gets assigned beyond subnet range
## if loop index = 0 -> "ip.address | ipaddr('network')"
## Else: -> "ip.address | ipaddr(loop.index0) | ipaddr('address')"

| Address | Available IP | Generated IP |
| ------- | ------------ | ------------ |
|10.0.0.0/24|first ip|10.0.0.0|
|10.0.0.0/24|second ip|10.0.0.1|
|10.0.0.0/24|third ip|10.0.0.2|
|10.1.0.128/25|first ip|10.1.0.128|
|10.1.0.128/25|second ip|10.1.0.129|
|10.1.0.128/25|third ip|10.1.0.130|
|192.168.0.128/30|first ip|192.168.0.128|
|192.168.0.128/30|second ip|192.168.0.129|
|192.168.0.128/30|third ip|192.168.0.130|
|192.168.0.128/30|fourth ip|192.168.0.131|
|192.168.0.128/30|fifth ip|False|
