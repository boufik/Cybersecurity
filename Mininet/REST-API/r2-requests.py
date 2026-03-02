import requests
import json

# 1. Get switches information
response = requests.get('http://localhost:8080/stats/switches')
switches = response.json()
print(40*"~", '\n1) For all the switches\nEndpoint = ..../stats/switches')
print("Switches: " + str(switches))
print(40*"~", '\n')


# 2. Get flow entries for switch with dpid=1
response = requests.get('http://localhost:8080/stats/flow/1')
flows = response.json()
print(40*"~", '\n2) For switch 1\nEndpoint = ..../stats/flow/1')
print("Flows: " + str(json.dumps(flows, indent=2)))
print(40*"~", '\n')


# 3. Add a new flow entry
flow = {
    "dpid": 1,
    "match": {
        "in_port": 1
    },
    "actions": [
        {
            "type": "OUTPUT",
            "port": 2
        }
    ]
}
response = requests.post('http://localhost:8080/stats/flowentry/add', data=json.dumps(flow))
print(40*"~", '\n3) Add a new flow entry\nEndpoint = ..../stats/flowentry/add')
print("Adding a new flow - status code = " + str(response.status_code))
print(40*"~", '\n')
