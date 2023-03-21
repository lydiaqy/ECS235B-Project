#!/bin/bash
make clean
python3 acting_graph/acting_graph.py $1 acting_graph.txt # creates acting graph and acting_graph.txt
python3 acting_graph/shortest_path.py acting_graph.txt # creates shortest path and shortest_path.txt
python3 can_know.py $1
if [ $(cat can_know.txt) -eq 1 ]; then
    python3 parse_graph.py
fi
#`./run.sh $INPUT