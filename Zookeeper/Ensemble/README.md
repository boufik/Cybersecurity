## 1) Create 3 SEPARATE .conf files:

*  Include 3 different values for `dataDir` + `clientPort`
*  The 3 last lines with `server.X=localhost:......` remain the same for the 3 files

### `zoo1.conf`

```
tickTime=2000
dataDir=temp-snapshots/zookeeper1
clientPort=2181
initLimit=5
syncLimit=2
server.1=localhost:2888:3888
server.2=localhost:2889:3889
server.3=localhost:2890:3890
```

### `zoo2.conf`

```
tickTime=2000
dataDir=temp-snapshots/zookeeper2
clientPort=2182
initLimit=5
syncLimit=2
server.1=localhost:2888:3888
server.2=localhost:2889:3889
server.3=localhost:2890:3890
```


### `zoo3.conf`

```
tickTime=2000
dataDir=temp-snapshots/zookeeper3
clientPort=2183
initLimit=5
syncLimit=2
server.1=localhost:2888:3888
server.2=localhost:2889:3889
server.3=localhost:2890:3890
```

## 2) Folder Structure

According to the `.conf` files above, it is clear that inside the `zookeeper` directory, we need to create a file named `temp-snapshots` and inside it to create 3 more directories named `zookeeper1`, `zookeeper2` and `zookeeper3`.
First, create it (manually or with Bash commands) and then run:

```
echo 1 > /tmp/zookeeper1/myid
echo 2 > /tmp/zookeeper2/myid
echo 3 > /tmp/zookeeper3/myid
```

The 3 `myid` files will be created automatically with contents `1`, `2` and `3`.


## 3) Start each server instance separately:

```
zkServer.sh start zoo1.cfg
zkServer.sh start zoo2.cfg
zkServer.sh start zoo3.cfg
```

# 4) Ensemble Experiments

First, connect to the fist instance of the Zookeeper server and inspect the filesystem with:

```
bin/zkCli.sh -server 127.0.0.1:2181
```

Then, connect to the second one and create folders:

```
bin/zkCli.sh -server 127.0.0.1:2182
```

Verify that all changes are made successfully with the third instance:

```
bin/zkCli.sh -server 127.0.0.1:2183
```
