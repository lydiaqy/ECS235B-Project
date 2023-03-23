import sys
import os

class ActingGraph:
    def __init__(self, num, num_subject, num_object):
        self.num = num
        self.num_subject = num_subject
        self.num_object = num_object
        self.vertices = set([i for i in range(1, self.num + 1)])
        self.subjects = set([i for i in range(1, self.num_subject + 1)])
        self.objects = set([i for i in range(1 + self.num_subject, 1 + self.num)])
        self.init_spans = {}
        self.term_spans = {}
        self.information_gate = []
        self.src = 0
        self.dest = 0

    def get_src_dest(self, src, dest):
        self.src = src
        self.dest = dest
    
    def initialize_rw_spans(self):
        for s in self.subjects:
            self.init_spans[s] = set([s])
            self.term_spans[s] = set([s])

    def get_access_sets(self, head, tail, rights):
        # rights: 0-r, 1-w, 2-rw
        if head in self.subjects:
            if rights == 0 or rights == 2: # tw-terminally spans
                self.term_spans[head].add(tail)
            
            if rights == 1 or rights == 2: # rw-initially spans
                self.init_spans[head].add(tail)

    def get_acting_edges(self):
        # find information gates
        for s in self.subjects:
            if self.init_spans[s] == {s}:
                if self.term_spans[s] == {s}:
                    self.information_gate.append({s})
        print("information gate: ", self.information_gate)
        
        # create a dict to save acting graph edges
        edges = {}
        for s in self.subjects:
            if s not in edges:
                edges[s] = set()

        # delta pair (a,b) = I(a) intersection T(b)
        for a in self.subjects:
            for b in self.subjects:
                if b != a:
                    I_a = self.init_spans[a]
                    T_b = self.term_spans[b]
                    delta_set = I_a.intersection(T_b)
                    if delta_set:
                        # if delta_set not in self.information_gate:
                        #     edges[a].add(b)
                        edges[a].add(b)

        return edges


def parse_input(input_file):
    found = False
    with open(input_file, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] == 'g':
                acting_graph = ActingGraph(int(line_content[1]), int(line_content[2]), int(line_content[3]))
                acting_graph.initialize_rw_spans()
                found = True
                break

    if found:
        with open(input_file, 'r') as f:
            for line in f.readlines():
                line_content = line.split()
                if line_content[0] == 'v':
                    acting_graph.get_src_dest(int(line_content[1]), int(line_content[2]))
                if line_content[0] == 'e':
                    acting_graph.get_access_sets(int(line_content[1]), int(line_content[2]), int(line_content[3]))

    return acting_graph


def write_output(output_file, edges, src, dest):
    subjects = sorted(edges.keys())
    output_txt = ' '.join(['v', str(src), str(dest)]) + '\n'

    for s in subjects:
        for v in edges[s]:
            output_txt += ' '.join(['e', str(s), str(v)]) + '\n'

    with open(output_file, 'w') as f:
        f.write(output_txt)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please enter your input.")
        sys.exit("Input not found.")

    # get path of files
    input_file = os.path.realpath(sys.argv[1])
    output_file = os.path.realpath(sys.argv[2])
    
    # parse the input file to get the network graph
    graph_result = parse_input(input_file)
    print("subjects: ", graph_result.subjects)
    print("objects: ", graph_result.objects)
    # rw-initially spans
    print("rw-initially spans: ", graph_result.init_spans)
    # rw-terminally spans
    print("rw-terminally spans: ", graph_result.term_spans)

    # get src and dest vertex
    src = graph_result.src
    dest = graph_result.dest

    # get acting graph edges
    edges_result = graph_result.get_acting_edges()
    print("acting graph edges: ", edges_result)

    # write edges result to output file
    write_output(output_file, edges_result, src, dest)