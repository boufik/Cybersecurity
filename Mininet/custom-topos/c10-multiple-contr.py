from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController, OVSSwitch
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup


class CustomTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
               

# MAIN FUNCTION
def run():

    setLogLevel('info')    
    myTopo = CustomTopo()
    c1 = RemoteController('c1')
    c2 = Controller('c2', ip='127.0.0.2')
    net = Mininet(topo=myTopo, controller=None, switch=OVSSwitch)
    for controller in [c0, c1]:
        net.addController(controller)
    net.start()
    
    # Connect specific switches to specific controllers
    net.get('s1').start([c0])
    net.get('s2').start([c1])
    net.get('s3').start([c1])
    
    # Run commands
    h1 = net.get('h1')
    result = h1.cmd('python3 --version')
    print(result)
    result = h1.cmd('ifconfig')
    print(result)
    
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
