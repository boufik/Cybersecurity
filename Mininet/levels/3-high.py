from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.clean import cleanup


class CustomTopo(Topo):
    def build(self, n=2):
        s1 = self.addSwitch('s1')
        for i in range(1, n+1):
            host = self.addHost('h'+str(i))
            self.addLink(s1, host)
            

# MAIN FUNCTION
cleanup()
myTopo = CustomTopo(n=4)
net = Mininet(topo=myTopo)
print("\n3) Create a network using high-level API: Topology templates\n")
net.start()
net.pingAll()
CLI(net)
net.stop()
