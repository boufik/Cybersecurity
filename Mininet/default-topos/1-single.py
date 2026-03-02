from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
from mininet.cli import CLI

Single5 = SingleSwitchTopo(k=5)
net = Mininet(topo=Single5)
net.start()
net.pingAll()
# CLI(net)
net.stop()

