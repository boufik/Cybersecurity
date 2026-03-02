from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup


class CustomTopo(Topo):
    def build(self):
        # Create 3 switches and 3 hosts
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        # Connect each host to each switch (9 links)
        for s in [s1, s2, s3]:
            for h in [h1, h2, h3]:
                self.addLink(s, h)


def extra(net, myTopo):
    print("\n~~~~ Network topology ~~~~\n")
    print(f"{len(myTopo.hosts())} hosts : {myTopo.hosts()}")
    print(f"{len(myTopo.switches())} switches : {myTopo.switches()}\n")
    print(f"Each host is connected to all switches, so there are totally {len(myTopo.links())} links:\n{myTopo.links()}")
    print("\n\nTesting network connectivity:")
    net.pingAll()
    CLI(net)
    
    
# MAIN FUNCTION
cleanup()
setLogLevel('info')
myTopo = CustomTopo()
net = Mininet(topo=myTopo)
net.start()
extra(net, myTopo)
net.stop()

