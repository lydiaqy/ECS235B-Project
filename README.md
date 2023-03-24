# ECS235B-Project

## How to run

```
./run.sh acting_graph/G.txt
```

To use other graphs, please copy from the `graphs/` directory and paste it into the `acting_graph/G.txt` file. `G_report_{rule}` corresponds to the graph that demonstrates the de jure {rule}.

## Usage - Server: 

Spawn FTP server at directory ./subject_1 hosted at localhost:50001 with object number 7 connected to it with right 0 (‘r’)
```
python server.py ./subject_1 50001 50007 0
```

Spawn FTP server at directory ./subject_3 hosted at localhost:50003 with subjects servers connected at:
1. localhost:50002 with right 0 ('r')
2. localhost:50006 with right 2 ('rw')
```
python server.py ./subject_3 50003 50002 0 50006 2
```

## Usage - Client Download:

Fetch file from FTP server with the first hop at localhost:50003 following by hops at localhost:50002 and localhost:50001. The file is hosted at localhost:50001.

```
python anon_client_download.py 50003 object_file_7:50002:50001
```

## To clean objects, subject_* directories, and intermediate files:

```
make clean
```

## To verify existence of FTP servers:

In a different terminal tab, run:

```
ps u | grep subject
```
