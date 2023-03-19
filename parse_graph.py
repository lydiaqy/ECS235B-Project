import os
import util

def is_subject(node_number, num_subjects):
    return node_number <= num_subjects

class Graph:
    graph_network = {}
    nodes = {}
    num_vertices = 0
    num_subjects = 0

    def __init__(self, num_vertices, num_subjects):
        self.num_vertices = num_vertices
        self.num_subjects = num_subjects

        for i in range(1, num_vertices + 1):
            self.graph_network[i] = {}
            
            ftp_server_port = None
            vertex_type_subject = is_subject(i, num_subjects)
            if vertex_type_subject:
                self.graph_network[i][i] = 2
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

    return graph

def create_files_and_dirs(graph: Graph):
    
    # the directory shows that the subject has the copy of the file
    for i in range(1, graph.num_subjects + 1):
        directory_path = util.NODE_SUBJECT_DIRECTORY_PREFIX + str(i)
        graph.nodes[i].ftp_server_directory = directory_path
        os.mkdir(directory_path)

    # all objects placed in a central area
    objects_directory = util.NODE_OBJECT_DIRECTORY
    os.mkdir(objects_directory)
    for i in range(graph.num_subjects + 1, graph.num_vertices + 1):
        object_name = util.NODE_OBJECT_FILE_PREFIX + str(i)
        with open(os.path.join(objects_directory, object_name), "w") as f:
            f.write(object_name) # object content is `object_name`

if __name__ == "__main__":
    input_file = os.path.realpath(util.INPUT_FILE)
    
    # parse input file to get network graph
    graph = parse_input(input_file)

    # for the given graph, create subjects and objects directories and object files
    # and add that to nodes of the graph
    create_files_and_dirs(graph)        

    # spawn subjects' servers using server.py