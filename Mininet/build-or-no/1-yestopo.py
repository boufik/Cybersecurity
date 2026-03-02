from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import dumpNodeConnections


class CustomTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)


# MAIN FUNCTION
print(30*"~")
print("Topo Class: Yes\nController: Yes - Default")
print(30*"~", '\n\n')
myTopo = CustomTopo()
net = Mininet(topo=myTopo)
net.start()
h1 = net.get('h1')
h2 = net.get('h2')
h1.setIP('172.16.1.101')
h2.setIP('172.16.1.102')

net.pingAll()
CLI(net)
net.stop()
