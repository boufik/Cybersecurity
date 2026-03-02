from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Host, Controller, RemoteController
from mininet.log import setLogLevel, info
from mininet.clean import cleanup

class CustomTopo(Topo):
    def build(self):
        # Nodes
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        # Links
        self.addLink(s1, h1)
        self.addLink(s2, h2)
        self.addLink(s3, h3)
        self.addLink(s4, h4)
        # Links again
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s2, s4)


def extra(net):
    print('\n')
    print("~~~~ Hosts ~~~~~")
    for host in net.hosts:
    	 print(host, ' ----> IP:', host.IP(), ' and MAC:', host.MAC())
    print("\n~~~~ Switches ~~~~")
    for switch in net.switches:
        print(switch)
    print("\n~~~~ Controllers ~~~~")
    for controller in net.controllers:
        print(controller, '----> port:', controller.port)
    print('\n')
    CLI(net)


# MAIN FUNCTION
setLogLevel('info')
myTopo = CustomTopo()
myController = RemoteController(name='c0-remote', ip='127.0.0.1', port=6653)
net = Mininet(topo=myTopo, controller=myController)

net.start()
h1 = net.get('h1')
host_ip = "10.0.2.15"
print("Host machine IP =", host_ip)
print(h1.cmd("curl http://" + host_ip + ":8080/stats/switches"))
extra(net)
net.stop()
