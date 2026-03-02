## c1-custom-topo.py
1 switch and 2 hosts (2 links)
```
net.pingAll()
```
Results: 0% dropped (2/2 received)


## c2-topo-attributes.py
3 switches and 3 hosts (9 links)
```
net.pingAll()
```
Results: 0% dropped (6/6 received)


## c3-controller-attributes.py
2 switches and 2 hosts (5 links)
```
net = Mininet(topo=myTopo, controller=c1000)
```
Controller's Information:
Name: c1000
Port: 6653
Protocol: tcp
IP: 127.100.100.100
```
net.pingAll()
```
Results: 0% dropped (2/2 received)


## c4-controller-auto-pings.py
1 switch and 2 hosts (2 links)
```
net = Mininet(topo=myTopo, controller=c1000)
```
Controller's Information:
Name: c1000
Port: 6653
Protocol: tcp
IP: 127.0.0.1
```
print(h1.cmd('ping -c 2 %s' % h2.IP()))
print(h1.cmd('ping -c 2 %s' % s1.IP()))
print(h2.cmd('ping -c 2 %s' % s1.IP()))
```
3 successful pings


## c5-addhost-errorh3.py
1 switch and 2 hosts (2 links)
```
net = Mininet(topo=myTopo)
h3 = net.addHost('h3')
s1 = net.get('s1')
net.addLink(h3, s1)
net.pingAll()
```
Results: 66% dropped (2/6 received)
The host h3 is added in the network, but it is not configured properly.
So, the host is physically located in the network, but can not be pinged!
Also, the new host can not be recognized in CLI too....
Some extra steps are required to make it functional!


## c6-custom-ips.py
1 switch and 2 hosts (2 links)
```
net = Mininet(topo=myTopo)
h1 = net.get('h1')
h2 = net.get('h2')
h1.setIP('172.16.1.101')
h2.setIP('172.16.1.102')
net.pingAll()
```
Results: 0% dropped (2/2 received)


## c7-remotecont.py
1 switch and 3 hosts (3 links)
Requires a second terminal running ryu:
```
ryu-manager --observe-links ryu.app.simple_switch_13 ryu.app.gui_topology.gui_topology
```
Controller's Information:
Name: remote-c1000
Port: 6653
Protocol: tcp
IP: 127.0.0.1
```
c1000 = RemoteController(name='remote-c1000', ip='127.0.0.1', port=6653)
net = Mininet(topo=myTopo, controller=c1000)
net.pingAll()
```
Results: 0% dropped (6/6 received)


## c8-custom-remote-topo.py
4 switches and 4 hosts (7 links)
Requires a second terminal running ryu:
```
ryu-manager --observe-links ryu.app.simple_switch_13 ryu.app.gui_topology.gui_topology
```

c1000 = RemoteController(name='remote-c1000', ip='127.0.0.1', port=6633)
net = Mininet(topo=myTopo, controller=c1000)
```
c1000 = RemoteController(name='remote-c1000', ip='127.0.0.1', port=6633)
net = Mininet(topo=myTopo, controller=c1000)
net.pingAll()
```
Results: 0% dropped (12/12 received)


## c9-net-get.py
1 switch and 3 hosts (3 links)
```
h1 = net.get('h1')
result = h1.cmd('python3 --version')
print(result)
result = h1.cmd('ifconfig')
print(result)
net.pingAll()
```

```
Python 3.8.10

h1-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.0.1  netmask 255.0.0.0  broadcast 10.255.255.255
        inet6 fe80::1815:bfff:fef7:f2cc  prefixlen 64  scopeid 0x20<link>
```
Results: 0% dropped (6/6 received)


## c10-multiple-contr.py
Unable to contact the remote controller at 127.0.0.1:6653
Unable to contact the remote controller at 127.0.0.1:6633
