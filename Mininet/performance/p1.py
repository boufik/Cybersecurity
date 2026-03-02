from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost, Controller
from mininet.link import TCLink
from mininet.clean import cleanup
import mininet.util


def show_stats(contr):
    print(60*"~")
    print(f"Controller '{contr.name}': IP = {contr.ip} using {contr.port} of {contr.protocol}")
    print(60*"~")
    

def show_performance(net, BW, DELAY):
    print('\n')
    print(60*"~", '\n!!!! Link(s1, h1) has ', DELAY, 'ms delay !!!!\n')
    print(f"!!!! Bandwidth(s1, h1) = {BW} Mbps !!!!")
    print(60*"~", '\n')
    print("----> PINGS <----")
    print(f"h1 --> h2 : At least {2*DELAY}ms delay = 2-way {DELAY}ms delay")
    print(h1.cmd('ping -c 4 %s' % h2.IP()))
    print(f"h1 --> h3 : At least {2*DELAY}ms delay = 2-way {DELAY}ms delay")
    print(h1.cmd('ping -c 4 %s' % h3.IP()))
    print("h2 --> h3 : No extra delays")
    print(h2.cmd('ping -c 4 %s' % h3.IP()))
    print("\n\n!!!! Check also iperf between the 2 hosts !!!!\n")
    print("----> IPERF <----")
    net.iperf((h1,h2))
    net.iperf((h1,h3))
    net.iperf((h2,h3))
    CLI(net)
    
# MAIN FUNCTION
cleanup()
net = Mininet(link=TCLink, host=CPULimitedHost)
c1000 = net.addController('c1000')
show_stats(c1000)

s1 = net.addSwitch('s1')
h1 = net.addHost('h1')
h2 = net.addHost('h2')
h3 = net.addHost('h3')
BW = 10
DELAY = 150
delay = str(DELAY) + 'ms'
net.addLink(s1, h1, bw=BW, delay=delay)
net.addLink(s1, h2)
net.addLink(s1, h3)

net.start()
show_performance(net, BW, DELAY)
net.stop()
