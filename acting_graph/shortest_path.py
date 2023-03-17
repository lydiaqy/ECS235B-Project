import sys
import os
from collections import defaultdict

class Graph:

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

def parse_input(input_file):
    found = False
    with open(input_file, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] == 'v':
                acting_graph = Graph(int(line_content[1]), int(line_content[2]))
                found = True
                break

    if found:
        with open(input_file, 'r') as f:
            for line in f.readlines():
                line_content = line.split()
                if line_content[0] == 'e':
                    acting_graph.add_edge(int(line_content[1]), int(line_content[2]), 1)

    return acting_graph


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter your input.")
        sys.exit("Input not found.")

    # get path of file
    input_file = os.path.realpath(sys.argv[1])
    
    # parse the input file to get the acting graph
    graph_result = parse_input(input_file)
    src = graph_result.src
    dest = graph_result.dest

	# function call
    path = dijsktra(graph_result, src, dest)
    print("The shortest path from vertex %d to vertex %d is: %s" %(src, dest, path))
    print("The minimum number of actors is: ", len(path))