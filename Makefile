clean:
# Deletes all subject directories
	ls -d subject_*/ | xargs rm -rf
# Deletes the object directory
	ls -d objects/ | xargs rm -rf
# remove intermediate files
	rm acting_graph.txt
	rm shortest_path.txt
	rm can_know.txt