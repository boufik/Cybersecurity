## r1-execute-rest-from-host.py
Requires a second terminal running Ryu:
```
ryu-manager --observe-links ryu.app.simple_switch_13 ryu.app.gui_topology.gui_topology
```
```
myController = RemoteController(name='c0-remote', ip='127.0.0.1', port=6653)
net = Mininet(topo=myTopo, controller=myController)
```
```
h1 = net.get('h1')
host_ip = "10.0.2.15"
print("Host machine IP =", host_ip)
print(h1.cmd("curl http://" + host_ip + ":8080/stats/switches"))
```
curl: (7) Failed to connect to 10.0.2.15 port 8080: No route to host
This happens, because for every host machine, "localhost" refers to the host, p.e. h1 and not the machine-VM that runs Mininet


## r2-requests.py
Requires 3 open terminals:
Terminal 1: Run a Mininet-based script with `sudo python3 ELECTRON.py`
Terminal 2: Run Ryu: `ryu-manager --observe-links ryu.app.simple_switch_13 ryu.app.gui_topology.gui_topology`
Terminal 3: Run the script for REST API: `sudo python3 r2-requests.py`
```
response = requests.get('http://localhost:8080/stats/switches')
response = requests.get('http://localhost:8080/stats/flow/1')
response = requests.post('http://localhost:8080/stats/flowentry/add', data=json.dumps(flow))
```
