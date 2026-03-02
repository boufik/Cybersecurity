from mininet.net import Mininet
from mininet.cli import CLI

net = Mininet()
c0 = net.addController('c0')
h1 = net.addHost('h1')
h2 = net.addHost('h2')
s1 = net.addSwitch('s1')
net.addLink(h1, s1)
net.addLink(h2, s1)
print("\n2) Create a network using mid-level API: Network Object\n")

net.start()
print(h1.cmd( 'ping -c4', h2.IP()))
CLI(net)
net.stop()
