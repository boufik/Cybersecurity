## p1.py
!!!! Link(s1, h1) has  150 ms delay !!!!
!!!! Bandwidth(s1, h1) = 10 Mbps !!!!
```
print(h1.cmd('ping -c 4 %s' % h2.IP()))
print(h1.cmd('ping -c 4 %s' % h3.IP()))
print(h2.cmd('ping -c 4 %s' % h3.IP()))
net.iperf((h1,h2))
net.iperf((h1,h3))
net.iperf((h2,h3))
```
Pings:
(h1-h2) : rtt min/avg/max/mdev = 304.293/394.930/640.754/142.039 ms
(h1-h3) : rtt min/avg/max/mdev = 304.194/395.076/661.404/153.781 ms
(h2-h3) : rtt min/avg/max/mdev = 0.074/11.246/44.395/19.139 ms
Iperf:
*** Iperf: testing TCP bandwidth between h1 and h2 
*** Results: ['6.23 Mbits/sec', '7.32 Mbits/sec']
*** Iperf: testing TCP bandwidth between h1 and h3 
*** Results: ['6.27 Mbits/sec', '7.47 Mbits/sec']
*** Iperf: testing TCP bandwidth between h2 and h3 
*** Results: ['46.6 Gbits/sec', '46.7 Gbits/sec']


## p2.py
```
host = self.addHost('h'+str(h+1), cpu=0.5/n)
self.addLink(host, switch, bw=10, delay='5ms', loss=2, max_queue_size=1000, use_htb=True)
```
```
net = Mininet(topo=myTopo, host=CPULimitedHost, link=TCLink)
h1, h4 = net.get('h1', 'h4')
net.iperf((h1, h4))
```
Testing bandwidth between h1 and h4 ....
*** Iperf: testing TCP bandwidth between h1 and h4 
*** Results: ['3.41 Mbits/sec', '3.38 Mbits/sec']
