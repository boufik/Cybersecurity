from mininet.net import Mininet
from mininet.cli import CLI


# MAIN FUNCTION
print(30*"~")
print("Topo Class: No\nController: None")
print(30*"~", '\n\n')
net = Mininet(controller=None)
h1 = net.addHost('h1')
h2 = net.addHost('h2')
s1 = net.addSwitch('s1')
net.addLink(h1, s1)
net.addLink(h2, s1)
h1.setIP('172.16.1.101')
h2.setIP('172.16.1.102')


net.start()
net.pingAll()
CLI(net)
net.stop()
