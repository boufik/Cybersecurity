## 1-low.py
1) Create a network using low-level API: Nodes and Links
```
h1 = Host('h1')
h2 = Host('h2')
s1 = OVSSwitch('s1', inNamespace=False)
c0 = Controller('c0', inNamespace=False)
Link(h1, s1)
Link(h2, s1)
```
--- 172.16.1.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3055ms


## 2-mid.py
2) Create a network using mid-level API: Network Object
```
net = Mininet()
c0 = net.addController('c0')
h1 = net.addHost('h1')
h2 = net.addHost('h2')
s1 = net.addSwitch('s1')
```
--- 10.0.0.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3012ms


## 3-high.py
3) Create a network using high-level API: Topology templates
```
myTopo = CustomTopo(n=4)
net = Mininet(topo=myTopo)
```
Results: 0% dropped (12/12 received)
