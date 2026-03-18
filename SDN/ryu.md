# Linux Prerequisites

```
sudo apt install python3           (Python3)
sudo apt install python3-pip       (pip3 enabled)
sudo apt install python            (Python2)
sudo apt install python-pip        (if it works, it is about pip, not pip3)
```

# 1. Install Mininet

## Clone the repo

```
git clone https://github.com/mininet/mininet.git
```

## Install Mininet

```
mininet/util/install.sh -a
```

The output must end with: `Enjoy Mininet!`

Verify with:

```
mn --version
sudo mn
```

# 2. Install Mininet and OVSController

Use `apt` to install the necessary packages:

```
sudo apt-get install mininet
sudo apt-get install openvswitch-testcontroller
```

# 3. Ryu

## Git clone from the official GH repo

```
git clone https://github.com/osrg/ryu.git
```

## Setup

```
cd ryu
sudo python3 ./setup.py install
```

After that, we can run the command `which ryu-manager`.

## Update ryu

```
cd ..
sudo pip3 install --upgrade ryu
```

# 4. Experiments

## 1st terminal

```
ryu-manager ryu/ryu/app/simple_switch_13.py
```

It outputs 4 lines in the CLI.

## 2nd terminal

```
$ sudo mn --controller remote
```

More info will be displayed in the 1st terminal, after the connection of `remote` controller.

*Note :If we want to execute a custom script `custom.py` that imports `mininet` (`from mininet.topo import Topo`), an error (`ModuleError`) will appear saying that: `'mininet' module is not recognized`.
So, we need to install the module with `pip install mininet`.*

# 5. Ryu Exposed REST API Endpoints

| REST API Endpoint | Functionality |
|:----:|:----|
| `/stats/switches` | Get list of switches |
| `/stats/desc/<dpid>` | Get switch description |
| `/stats/flow/<dpid>` | Get all flows |
| `/stats/aggregateflow/<dpid>` | Get aggregate flow stats |
| `/stats/port/<dpid>[/<port>]` | Get port statistics |
| `/stats/queue/<dpid>[/<port>[/<queue_id>]]` | Get queue statistics |
| `/stats/meterfeatures/<dpid>` | Get meter features |
| `/stats/meterconfig/<dpid>[/<meter_id>]` | Get meter configuration |
| `/stats/flowentry/add` | Add a flow entry |
| `/stats/flowentry/modify` | Modify a flow entry |
| `/stats/flowentry/delete` | Delete a flow entry |

Command:

```
ryu-manager --observe-links ryu.app.simple_switch_13 ryu.app.gui_topology.gui_topology ryu.app.ofctl_rest
```

The `ryu.app.ofctl_rest` module is for the API endpoints.

# 6. Delete Mininet Leftovers

```
sudo ovs-vsctl show
```

Only **IN CASE OF DEBRIS SWITCHES THAT CAN NOT DELETED with `sudo mn -c`**, like leftovers with bridge names (like `s1`, `s2`), run:

## Delete the `s1` bridge for example

```
sudo ovs-vsctl --if-exists del-br s1
```

## Restart the OVS service

```
sudo systemctl restart openvswitch-switch
```

# 7. Post a new rule

Manually navigate in the URL endpoint `http://localhost:8080/stats/flow/1` to observe the flow table. The flow table contains flow entries.
Each flow entry represents a rule with a `match` and an `actions` field. Generally speaking, the flow entry defines a data flow, the way the packets are forwarded.
We can do the same thing by typing the CLI command:

```
curl http://localhost:8080/stats/flow/1
```

By observing the rules, we can see that initially there are 2 (priorities = 65535 and 0). If we want to add a new rule for `switch 1`, we can do so by typing:

```
curl -X POST -d {json_formatted_data} http://localhost:8080/stats/flowentry/add
```

In the `{}`, to add a rule related to switch 1, we must include this: `"dpid":1`. After that, we can verify the fact that a new (3rd) rule was added in the flow table of switch with `dpid=1`, by typing again:

```
URL = http://localhost:8080/stats/flow/1
```

There, we can show that now we have 3 installed rules (initially we had only 2).

```
curl -X POST -d '{
    "dpid": 1,
	"priority": 8888,
    "match": {
        "dl_vlan": 50
    },
    "actions": [
        {
            "type": "OUTPUT",
            "port": 1
        }
    ]
}' http://localhost:8080/stats/flowentry/add
```

This command sends a `POST` request to the OpenFlow controller at `http://localhost:8080/stats/flowentry/add`, adding a flow entry to the switch with dpid (Datapath ID) 1.
The rule matches packets with VLAN ID 5 and forwards them to port 1.
