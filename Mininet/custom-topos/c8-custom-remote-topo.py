from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.clean import cleanup


class CustomTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')
        s4 = self.addSwitch('s4', protocols='OpenFlow13')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)
        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s1, s4)


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
setLogLevel('info')
myTopo = CustomTopo()
c1000 = RemoteController(name='remote-c1000', ip='127.0.0.1', port=6633)
net = Mininet(topo=myTopo, controller=c1000)    
net.start()
extra(net)
net.stop()
