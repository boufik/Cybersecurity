from kazoo.client import KazooClient
import time

# Connect to standalone ZooKeeper server
zk = KazooClient(hosts='127.0.0.1:4000')
zk.start()

try:
    previous = set()
    directory = "/master/1"
    while True:
        children = zk.get_children(directory)
        current = set(children)       
        if current != previous:
            print("📁 / directory updated:", sorted(children))
            previous = current
        time.sleep(1)  # spam delay
        
except KeyboardInterrupt:
    print("Stopped monitoring.")
    
finally:
    zk.stop()
