from mininet.net import Mininet
from mininet.node import Controller, OVSController, OVSSwitch
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup


class CustomTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)


def extra(net):
    print("\n\n")
    print(30*"~")
    print("Controller's Information:")
    print(f"Name: {c1000.name}")
    print(f"Port: {c1000.port}")
    print(f"Protocol: {c1000.protocol}")
    print(f"IP: {c1000.ip}")
    print(30*"~", '\n')
    print("\n\n~~~~ Testing connectivity between hosts (2 AUTOMATED PINGS) ~~~~\n")
    # AUTOMATED PINGS
    h1, h2, s1 = net.get('h1', 'h2', 's1')
    print("h1 --> h2:")
    print(h1.cmd('ping -c 2 %s' % h2.IP()))
    print("h1 --> s1:")
    print(h1.cmd('ping -c 2 %s' % s1.IP()))
    print("h2 --> s1:")
    print(h2.cmd('ping -c 2 %s' % s1.IP()))
    print("\n\n")
    CLI(net)
    

# MAIN FUNCTION
cleanup()
setLogLevel('info')
myTopo = CustomTopo()
c1000 = Controller('c1000')
net = Mininet(topo=myTopo, controller=c1000)
net.start() 
extra(net)
net.stop()
