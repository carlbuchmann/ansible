# IP address Filter

## issue with first network address not yielding any results when using "ip.address | ipaddr(loop.index0) | ipaddr('address')"

| Address | Available IP | Generated IP |
| ------- | ------------ | ------------ |
|10.0.0.0/24|first ip||
|10.0.0.0/24|second ip|10.0.0.1|
|10.0.0.0/24|third ip|10.0.0.2|
|10.1.0.128/25|first ip||
|10.1.0.128/25|second ip|10.1.0.129|
|10.1.0.128/25|third ip|10.1.0.130|

## fix using ipmath instead based of network "ip.address | ipaddr('network') | ipmath(loop.index0)"

| Address | Available IP | Generated IP |
| ------- | ------------ | ------------ |
|10.0.0.0/24|first ip|10.0.0.0|
|10.0.0.0/24|second ip|10.0.0.1|
|10.0.0.0/24|third ip|10.0.0.2|
|10.1.0.128/25|first ip|10.1.0.128|
|10.1.0.128/25|second ip|10.1.0.129|
|10.1.0.128/25|third ip|10.1.0.130|
