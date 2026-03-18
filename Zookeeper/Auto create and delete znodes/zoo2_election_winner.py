from kazoo.client import KazooClient
import time


def print_all_children(zk, directory, children):
    for i, child in enumerate(children):
        full_path_child = f"{directory}/{child}"
        data_child, stat_child = zk.get(full_path_child)
        print(f"Child {i+1} : {child}  <---->  {data_child.decode('utf-8')}")

def print_children_winner(directory, children, winner, data):
    print(80 * '~')
    print(f"📁 : The directory {directory} has been updated!\nChildren = {children}\n")
    print(f"Election's winner = {winner}")
    print(f"Controller's data = {data.decode('utf-8')}\n{80 * '~'}\n\n")


# 1. Connect to standalone ZooKeeper server
zk = KazooClient(hosts='127.0.0.1:4000')
zk.start()
zk_state = zk.state
dilosi = f"Standalone zk server status = {zk_state}"
print(f"\n{len(dilosi) * '~'}\n{dilosi}\n{len(dilosi) * '~'}\n\n")


# 2. Under /master/<dpid> directory ---> Find election's winner + print children
try:
    #### PUT AN EXISTING DIRECTORY ####
    directory = "/master/1"		
    previous = set()
    while True:
        children = zk.get_children(directory)
        current = set(children)       
        if current != previous:
            # Example: children = ['znode-3', 'znode-4', 'znode-5']
            # print_all_children(zk, directory, children)
            if children:
                winner = sorted(children)[0]
            full_path = f"{directory}/{winner}"	# Example: full_path = /master/1/znode-3
            data, stat = zk.get(full_path)
            previous = current
            print_children_winner(directory, children, winner, data)
            # print_all_children(zk, directory, children)
        time.sleep(0.2)  					# Spam Delay
        
except KeyboardInterrupt:
    print("\n\nJust pressed Ctrl+C ---> Stopped monitoring...\n\n")
    
finally:
    zk.stop()
