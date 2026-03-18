We need 4 terminals to showcase how Zookeeper election works, First, navigate to the folder, where you have installed Zookeeper:

```
cd ~/Desktop/monitoring-zoo/
```

## Terminal 1 - Upper Left

The Shell terminal of the actual Zookeeper service:

```
bin/zkCli.sh -server localhost:4000
```

## Terminal 2 - Upper Right

```
python3 zoo1_directory_updates.py
```

## Terminal 3 - Bottom Left

```
python3 autocreate.py
```

## Terminal 4 - Bottom Right

```
python3 zoo3_election_winner_better.py
```
