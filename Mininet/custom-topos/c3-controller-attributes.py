from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup


class CustomTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h1, s2)
        self.addLink(h2, s2)
        self.addLink(s1, s2)

def extra(net):
    print("\n\n")
    print(30*"~")
    print("Controller's Information:")
    print(f"Name: {c1000.name}\nPort: {c1000.port}")
    print(f"Protocol: {c1000.protocol}\nIP: {c1000.ip}")
    print(30*"~")
    print("\n\nTesting network connectivity between hosts:")
    net.pingAll()
    CLI(net)


# MAIN FUNCTION
cleanup()
setLogLevel('info')
myTopo = CustomTopo()
c1000 = Controller(name='c1000', ip="127.100.100.100", port=6653, protocol='tcp')
net = Mininet(topo=myTopo, controller=c1000)
net.start()
extra(net)
net.stop()

