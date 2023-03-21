import os
import util
import subprocess
import multiprocessing
import ast

import time

def is_subject(node_number, num_subjects):
    return node_number <= num_subjects

class Graph:
    graph_network = {}
    inverse_graph_network = {}
    nodes = {}
    num_vertices = 0
    num_subjects = 0

    def __init__(self, num_vertices, num_subjects):
        self.num_vertices = num_vertices
        self.num_subjects = num_subjects

        for i in range(1, num_vertices + 1):
            self.graph_network[i] = {}
            self.inverse_graph_network[i] = {}
            
            ftp_server_port = None
            vertex_type_subject = is_subject(i, num_subjects)
            if vertex_type_subject:
                self.graph_network[i][i] = 2
                self.inverse_graph_network[i][i] = 2
                ftp_server_port = int(util.SERVER_PORT_PREFIX + str(i))
            self.nodes[i] = Node(vertex_type_subject, i, ftp_server_port)

class Node:

    node_number = None
    ftp_server_port = None
    ftp_server_directory = None

    def __init__(self, is_subject, node_number, ftp_server_port=None):
        if is_subject:
            assert(ftp_server_port != None)
            self.ftp_server_port = ftp_server_port

        self.node_number = node_number

def parse_input(input_file):

    graph = None
    graph_exists = False
    num_vertices = None
    num_subjects = None
    num_objects = None

    with open(input_file, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if (line_content[0] == 'g'):
                graph_exists = True
                num_vertices = int(line_content[1])
                num_subjects = int(line_content[2])
                num_objects = int(line_content[3])

                graph = Graph(num_vertices, num_subjects)
                assert(num_vertices == num_subjects + num_objects)
                break

    if graph_exists: 
        with open(input_file, 'r') as f:
            for line in f.readlines():
                line_content = line.split()
                if (line_content[0] == 'e'):
                    vertex_1 = int(line_content[1])
                    assert(vertex_1 >= 1 and vertex_1 <= num_vertices)
                    vertex_2 = int(line_content[2])
                    assert(vertex_2 >= 1 and vertex_2 <= num_vertices)
                    right = int(line_content[3])
                    assert(right >= 0 and right <= 2)

                    graph.graph_network[vertex_1][vertex_2] = right
                    graph.inverse_graph_network[vertex_2][vertex_1] = right

    return graph

def create_files_and_dirs(graph: Graph):
    
    # the directory shows that the subject has the copy of the file
    for i in range(1, graph.num_subjects + 1):
        directory_path = util.NODE_SUBJECT_DIRECTORY_PREFIX + str(i)
        graph.nodes[i].ftp_server_directory = directory_path
        try: 
            os.mkdir(directory_path)
        except FileExistsError:
            pass

    # all objects placed in a central area
    objects_directory = util.NODE_OBJECT_DIRECTORY
    try:
        os.mkdir(objects_directory)
    except FileExistsError:
        pass
    for i in range(graph.num_subjects + 1, graph.num_vertices + 1):
        object_name = util.NODE_OBJECT_FILE_PREFIX + str(i)
        with open(os.path.join(objects_directory, object_name), "w") as f:
            f.write(object_name) # object content is `object_name`

def run_script(server_script):
    """Function to run a script in a new shell"""
    subprocess.call(server_script)

if __name__ == "__main__":
    input_file = os.path.realpath(util.INPUT_FILE)
    
    # parse input file to get network graph
    graph = parse_input(input_file)

    # for the given graph, create subjects and objects directories and object files
    # and add that to nodes of the graph
    create_files_and_dirs(graph)        

    # spawn subjects' servers using server.py
    scripts = []
    for node_number in graph.nodes.keys():
        if is_subject(node_number, graph.num_subjects):
            script = ['python', 'server.py', graph.nodes[node_number].ftp_server_directory, str(graph.nodes[node_number].ftp_server_port)]
            for remote_ftp_server, remote_ftp_server_right in graph.graph_network[node_number].items():
                script.append(util.SERVER_PORT_PREFIX + str(remote_ftp_server))
                script.append(str(remote_ftp_server_right))
            print(' '.join(script))
            scripts.append(script)

    # spawn anon_download_client script using anon_client_download.py
    # python anon_client_download.py 50000 server_50003_file.txt:50002:50003
    all_first_subject_objects = []
    with open('shortest_path.txt', 'r') as f:
        shortest_path = f.read()
    shortest_path = ast.literal_eval(shortest_path)
    first_subject = shortest_path[0]
    for nearby_node_tup in graph.graph_network[first_subject].items():
        nearby_node = nearby_node_tup[0]
        right_on_nearby_node = nearby_node_tup[1]
        if (not is_subject(nearby_node, graph.num_subjects) and right_on_nearby_node in [0, 2]):
            all_first_subject_objects.append(nearby_node)
    
    client_scripts = []
    for object in all_first_subject_objects:
        object_file_name = util.NODE_OBJECT_FILE_PREFIX + str(object)
        for subject in shortest_path[::-1][1:]:
            object_file_name += f":{util.SERVER_PORT_PREFIX + str(subject)}"
        client_script = ['python', 'anon_client_download.py', util.SERVER_PORT_PREFIX + str(shortest_path[-1]), object_file_name]
        print(' '.join(client_script))
        client_scripts.append(client_script)

    # Spawn a new process for each script
    processes = [multiprocessing.Process(target=run_script, args=(script,)) for script in scripts]

    # Start all processes
    for process in processes:
        process.start()
    
    print("Wait for 5 seconds till all servers start")
    time.sleep(5)
    client_processes = [multiprocessing.Process(target=run_script, args=(client_script, )) for client_script in client_scripts]
    for client_process in client_processes:
        client_process.start()

    for client_process in client_processes:
        client_process.join()

    # Wait for all processes to finish
    for process in processes:
        process.join()
