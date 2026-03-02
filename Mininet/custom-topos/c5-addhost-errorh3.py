from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.clean import cleanup
from mininet.util import dumpNodeConnections

class CustomTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(h1, s1)
        self.addLink(h2, s1)


# MAIN FUNCTION
# 1. Start the network
cleanup()
setLogLevel('info')
myTopo = CustomTopo()
net = Mininet(topo=myTopo)
net.start()


# 2. Initial State
print(50*"~")
print("----> Initial network state - Hosts <----")
dumpNodeConnections(net.hosts)
print("\n\nInitial ping test:")
net.pingAll()
print(50*"~")


# 3. Add another host to the already running network
print('\n\n', 50*"~")
print("Adding a new host named 'h3'...")
print(50*"~", '\n\n')
h3 = net.addHost('h3')
s1 = net.get('s1')
net.addLink(h3, s1)


# 4. Final State
print(50*"~")
print("----> Final network state - Hosts <----")
dumpNodeConnections(net.hosts)
print("\n\nFinal ping test:")
net.pingAll()
print(50*"~", '\n\n')


# 5. Notes
print(80*"~")
print("The host h3 is added in the network, but it is not configured properly.")
print("So, the host is physically located in the network, but can not be pinged!")
print("Also, the new host can not be recognized in CLI too....")
print("Some extra steps are required to make it functional!")
print(80*"~")


# 6. CLI and stop the network
CLI(net)
net.stop()
