from kazoo.client import KazooClient
import kazoo.exceptions
import time

"""
REQUIREMENTS:
1) Existing /master/1 directory
2) Under /master/1 directory, NO CHILDREN named "znode-0" and "znode-3"
p.e. This directory can contain childern like: "znode-1" and "znode-2"
"""

# AUXILIARY FUNCTIONS
def create(zk, directory, new, data):
    print(f"----> Creating {new} with value = {data}")
    zk.create(path=f"{directory}/{new}", value=data, makepath=True)
    print("\n")


def delete(zk, full_directory):
    print(f"----> Deleting {full_directory}...")
    zk.delete(full_directory)
    print("\n")


# 1. Connect to standalone ZooKeeper server
zk = KazooClient(hosts='127.0.0.1:4000')
zk.start()
zk_state = zk.state
dilosi = f"Standalone zk server status = {zk_state}"
print(f"\n{len(dilosi) * '~'}\n{dilosi}\n{len(dilosi) * '~'}\n\n")
print("!!!! Script for auto-creating and auto-deleting znodes !!!!", '\n\n')
SLEEP = 5
time.sleep(SLEEP)



# 2. Create and delete znodes under the "/master/<dpid>" directory
try:
    directory = "/master/1"
    new1 = "znode-0"
    new2 = "znode-3"
    data1 = b"FIRST Controller"
    data2 = b"Controller 9"
    create(zk, directory, new1, data1)
    time.sleep(SLEEP)
    create(zk, directory, new2, data2)
    time.sleep(SLEEP)
    delete(zk, f"{directory}/{new2}")
    time.sleep(SLEEP)
    delete(zk, f"{directory}/{new1}")
   
   
    
# These are the possible 6 errors from calling create() and delete()    
except (NodeExistsError, NoNodeError, NoChildrenForEphemeralsError, ZookeeperError, BadVersionError, NotEmptyError) as e:
    print("\n", 80 * '~', '\n')
    print(f"Exception occurred: {type(e).__name__}")
    print(f"\n{80 * '~'}\n")
    
finally:
    print("\nStopping the client...")
    zk.stop()
