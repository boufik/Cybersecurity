from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller, RemoteController


# MAIN FUNCTION
print(30*"~")
print("Topo Class: No\nController: Yes (added later)")
print(30*"~", '\n\n')

net = Mininet()
net.addController('cont')			# If I omit it, pings fail??? But the above line of code creates a Mininet() with the default Controller....
h1 = net.addHost('h1', ip='10.0.0.1/24')
h2 = net.addHost('h2', ip='10.0.0.2/24')
s1 = net.addSwitch('s1')
net.addLink(h1, s1)
net.addLink(h2, s1)

net.start()
net.pingAll()
CLI(net)
net.stop()
