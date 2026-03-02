from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.log import setLogLevel
from mininet.cli import CLI

Linear3 = LinearTopo(k=3)
net = Mininet(topo=Linear3)
net.start()
net.pingAll()
# CLI(net)
net.stop()
