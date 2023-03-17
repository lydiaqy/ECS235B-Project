#!/bin/bash
python3 acting_graph.py network_graph.txt acting_graph.txt
python3 shortest_path.py acting_graph.txt
#`./run.sh $INPUT $OUTPUT`