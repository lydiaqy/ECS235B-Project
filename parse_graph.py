import sys
import os
import util

class Server:
    def __init__(self, server_name, server_port):
        self.server_name = server_name
        self.server_port = server_port
        self.connected_servers = {}

def parse_input(input_file):

    graph_exists = False

    with open(input_file, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if (line_content[0] == 'g'):
                graph_exists = True
            if (graph_exists and line_content[0] == 'e'):
                

if __name__ == "__main__":
    input_file = os.path.realpath(util.INPUT_FILE)
    
    # parse input file to get network graph
    graph_result = parse_input(input_file)