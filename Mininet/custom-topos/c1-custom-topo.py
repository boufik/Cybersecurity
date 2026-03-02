from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup

class CustomTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        
# MAIN FUNCTION
cleanup()
setLogLevel('info')
myTopo = CustomTopo()
net = Mininet(topo=myTopo)
net.start()
net.pingAll()
net.stop()
