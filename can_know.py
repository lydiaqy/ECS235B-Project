import sys
from parse_graph import parse_input, is_subject
import util
import ast

if __name__ == "__main__":
    if (len(sys.argv) < 2): 
        print("Provide input file")
        sys.exit("Input file not provided")

    input_file = sys.argv[1]

    # parse input file to get network graph
    graph = parse_input(input_file)

    # obtain shortest_path
    try: 
        with open(util.SHORTEST_PATH_FILE, 'r') as f:
            shortest_path = f.read()
    except FileNotFoundError:
        sys.exit("shortest_path.txt not found, so can_know = False")

    print("can_know = True because shortest_path.txt exists")
    shortest_path = ast.literal_eval(shortest_path)
    
    # Whatever objects the first node has
    # we want to validate if the last node in the 
    # shortest path can obtain using de jure rules

    can_obtain = [None for _ in shortest_path]
    shortest_path_can_obtain_idx = {}
    for idx, node in enumerate(shortest_path):
        shortest_path_can_obtain_idx[node] = idx
    obtainable_objects = []
    
    # Check if the first subject can access any object
    first_node = shortest_path[0]
    for nearby_node_tup in graph.graph_network[first_node].items():
        nearby_node = nearby_node_tup[0]
        right_on_nearby_node = nearby_node_tup[1]
        if (nearby_node == first_node):
            continue
        if (not is_subject(nearby_node, graph.num_subjects) and right_on_nearby_node in [0, 2]):
            can_obtain[0] = True
            obtainable_objects.append(nearby_node)
    
    if (can_obtain[0] == None):
        can_obtain[0] = False
        sys.exit(f"can_obtain[{shortest_path[0]}] = False: First node {shortest_path[0]} cannot obtain any objects")

    print(f"can_obtain[{shortest_path[0]}] = True: First node {shortest_path[0]} can obtain objects: {obtainable_objects}")
    # now, iterate till the last node 
    # and check using post and spy rules
    # or direct access using 'r' or 'rw' on a previously can_obtain[True] node 
    for i in range(1, len(shortest_path)):
        current_node = shortest_path[i]
        de_jure_result = False

        for nearby_node_tup in graph.graph_network[current_node].items():
            nearby_node = nearby_node_tup[0]
            right_on_nearby_node = nearby_node_tup[1]

            if (de_jure_result):
                break

            if (nearby_node == current_node):
                continue
            
            # check if we have 'r' right on any of the previous nodes
            if nearby_node not in shortest_path_can_obtain_idx:
                continue
            nearby_node_idx = shortest_path_can_obtain_idx[nearby_node]
            if (can_obtain[nearby_node_idx] == True and right_on_nearby_node in [0, 2]):
                de_jure_result = True
                print(f"can_obtain[{current_node}] = True: Node {current_node} can directly connect out to {nearby_node}")
                break

            # post
            if (not de_jure_result and right_on_nearby_node in [0, 2]):
                for level_2_node_tup in graph.inverse_graph_network[nearby_node].items():
                    level_2_node = level_2_node_tup[0]
                    right_on_level_2_node = level_2_node_tup[1]

                    if level_2_node not in shortest_path_can_obtain_idx:
                        continue
                    level_2_node_idx = shortest_path_can_obtain_idx[level_2_node]
                    if (is_subject(level_2_node, graph.num_subjects) and right_on_level_2_node in [1, 2] and can_obtain[level_2_node_idx]):
                        print(f"can_obtain[{current_node}] = True using POST: Node {current_node} can connect to {level_2_node} via {nearby_node}")
                        de_jure_result = True

            # spy 
            if (not de_jure_result and is_subject(nearby_node, graph.num_subjects) and right_on_nearby_node in [0, 2]):
                for level_2_node_tup in graph.graph_network[nearby_node].items():
                    level_2_node = level_2_node_tup[0]
                    right_on_level_2_node = level_2_node_tup[1]

                    if level_2_node not in shortest_path_can_obtain_idx:
                        continue
                    level_2_node_idx = shortest_path_can_obtain_idx[level_2_node]
                    if (right_on_level_2_node in [0, 2] and can_obtain[level_2_node_idx]):
                        print(f"can_obtain[{current_node}] = True using SPY: Node {current_node} can connect to {level_2_node} via {nearby_node}")
                        de_jure_result = True

        # check de jure rules: find and pass
        for nearby_node_tup in graph.inverse_graph_network[current_node].items():
            nearby_node = nearby_node_tup[0]
            right_on_nearby_node = nearby_node_tup[1]

            if (de_jure_result):
                break

            if (nearby_node == current_node):
                continue

            # find 
            if (not de_jure_result and is_subject(nearby_node, graph.num_subjects) and right_on_nearby_node in [1, 2]):
                for level_2_node_tup in graph.inverse_graph_network[nearby_node].items():
                    level_2_node = level_2_node_tup[0]
                    right_on_level_2_node = level_2_node_tup[1]

                    if level_2_node not in shortest_path_can_obtain_idx:
                        continue
                    level_2_node_idx = shortest_path_can_obtain_idx[level_2_node]
                    if (is_subject(level_2_node, graph.num_subjects) and right_on_level_2_node in [1, 2] and can_obtain[level_2_node_idx]):
                        print(f"can_obtain[{current_node}] = True using FIND: Node {current_node} can connect to {level_2_node} via {nearby_node}")
                        de_jure_result = True

            # pass
            if (not de_jure_result and is_subject(nearby_node, graph.num_subjects) and right_on_nearby_node in [1, 2]):
                for level_2_node_tup in graph.graph_network[nearby_node].items():
                    level_2_node = level_2_node_tup[0]
                    right_on_level_2_node = level_2_node_tup[1]

                    if level_2_node not in shortest_path_can_obtain_idx:
                        continue
                    level_2_node_idx = shortest_path_can_obtain_idx[level_2_node]
                    if (right_on_level_2_node in [0, 2] and can_obtain[level_2_node_idx]):
                        print(f"can_obtain[{current_node}] = True using PASS: Node {current_node} can connect to {level_2_node} via {nearby_node}")
                        de_jure_result = True

        # finally, if it is still False, then set it as False
        # This means that the shortest path cannot contain this node
        if (de_jure_result == False):
            can_obtain[i] = False
            sys.exit(f"can_obtain[{current_node}] = False: Current node {current_node} cannot obtain any objects")
        else:
            can_obtain[i] = True


    # Final check 
    final_result = can_obtain[-1]
    with open('can_know.txt', 'w') as f:
        if (final_result):
            f.write(str(1))
        else:
            f.write(str(0))

    if (can_obtain[-1] == True):
        print(f"File transfer is possible from {shortest_path[0]} to {shortest_path[-1]}")
    else:
        print(f"File transfer is not possible from {shortest_path[0]} to {shortest_path[-1]}")
