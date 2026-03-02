from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI

# Create a custom tree topology
class CustomTreeTopo(Topo):
    def build(self, depth=1, fanout=2):
        # Numbering:  h1..N, s1..M
        self.hostNum = 1
        self.switchNum = 1
        self.addTree(depth, fanout)
        
    def addTree(self, depth, fanout):
        isSwitch = depth > 0
        if isSwitch:
            node = self.addSwitch(f's{self.switchNum}')
            self.switchNum += 1
            for _ in range(fanout):
                child = self.addTree(depth - 1, fanout)
                self.addLink(node, child)
            return node
        else:
            # Add a host
            node = self.addHost(f'h{self.hostNum}')
            self.hostNum += 1
            return node
            

# MAIN FUNCTION
setLogLevel('info')
Tree32 = CustomTreeTopo()
Tree32.build(depth=3, fanout=2)
net = Mininet(topo=Tree32)
net.start()
net.pingAll()
# CLI(net)
net.stop()


