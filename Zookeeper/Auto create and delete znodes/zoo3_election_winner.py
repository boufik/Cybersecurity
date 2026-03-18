from kazoo.client import KazooClient
import time


# AUXILIARY FUNCTIONS
def print_all_children(zk, directory, children):
    for i, child in enumerate(children):
        full_path_child = f"{directory}/{child}"
        data_child, stat_child = zk.get(full_path_child)
        print(f"Child {i+1} : {child}  <---->  {data_child.decode('utf-8')}")


def print_children_winner(directory, children, winner, data):
    print(f"📁 : The directory {directory} has been updated!\nChildren = {sorted(children)}\n")
    print(f"Election's winner = {winner}")
    print(f"Controller's data = {data.decode('utf-8')}\n{80 * '~'}\n\n")


def compare_sets(zk, directory, previous, current):
    diff1 = previous.difference(current)
    diff2 = current.difference(previous)
    if len(diff1) == 1:
        # If len=0 (set=empty={} - in the beginning) ---> Do not enter here
        # If len>1 (many controllers failed at the same time) ---> Do not enter here
        print("📵 : A controller was disconnected...")
    if len(diff2) == 1:
        full_path = f"{directory}/{list(diff2)[0]}"
        data, stat = zk.get(full_path)
        print(f"🔌 : {data.decode('utf-8')} was connected!")
            

# 0. Global Variables
GLOBAL_DICT = {}


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
        if current != previous:			# Something has changed, compare them
            # Example: children = ['znode-3', 'znode-4', 'znode-5']
            print(80 * '~')
            if children:
                winner = sorted(children)[0]
                compare_sets(zk, directory, previous, current)
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
