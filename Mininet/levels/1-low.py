from mininet.node import Host, OVSSwitch, Controller
from mininet.link import Link


h1 = Host('h1')
h2 = Host('h2')
s1 = OVSSwitch('s1', inNamespace=False)
c0 = Controller('c0', inNamespace=False)
Link(h1, s1)
Link(h2, s1)
h1.setIP('172.16.1.1/24')
h2.setIP('172.16.1.2/24')
print("\n1) Create a network using low-level API: Nodes and Links\n")

c0.start()
s1.start([c0])
print(h1.cmd('ping -c4', h2.IP()))
s1.stop()
c0.stop()
