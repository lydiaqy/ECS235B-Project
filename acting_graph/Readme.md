To run the code, please have your network graph .txt file (G.txt in the sample code) ready with the required format, then run the following command:
```./run.sh your_network_graph.txt```
The shortest path and the number of minimum actors will be displayed in the output on the terminal.

Rules of generating `your_network_graph.txt`:
1. The `your_network_graph.txt` is the only input of the whole simulation code. Based on the constraints we defined for the simulation, only w and r rights are considered in the network graph, also only one original file f exists while several copies of f are allowed. Here we require the user to rename the vertices of the network graph with integer numbers from 1, starting from the subjects, then name the objects after naming all the subjects, i.e., a network graph has 6 subjects and 2 objects, name the 6 subjects first, then the two objects as 7 and 8.

2. The first line of the `your_network_graph.txt` requires a declaration on the number of vertices of the network graph as `g number_of_vertices number_of_subjects number_of_objects`, i.e., if a network graph has 8 vertices with 6 subjects and 2 objects, the first line would be `g 8 6 2`.

3. `your_network_graph.txt` requires declarations on the locations of the source file as well as the copied files in the network graph as `v vertex_of_source vertex_of_copy`, i.e., for a network graph with the vertex of source file f as 1 and the vertex of the copied file f’ as 3, the line would be `v 1 3`. If you have several copied files in your network graph, you need to declare all the locations of the copied files, for example, if you have vertex of source file as 1, and three copied files at 2, 3, 4, then the lines would be `v 1 2`, `v 1 3`, `v 1 4`.

4. At last, the `your_network_graph.txt` requires declarations on all the edges between all the subjects vertices and the vertex of the source file with the corresponding rights as `e from_vertex_of_edge to_vertex_of_edge rights`, r right is 0, w right is 1, rw right is 2. For a network graph with edge from subject vertex 1 to object vertex 7 of right r, the line would be `e 1 7 0`. Be aware that only the object vertex with the original file should be included in the declarations of edges, the vertices with copied files are not included.
