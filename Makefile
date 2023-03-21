clean:
# Deletes all subject directories
	ls -d subject_*/ | xargs rm -rf
# Deletes the object directory
	ls -d objects/ | xargs rm -rf
# remove intermediate files
	rm acting_graph.txt
	rm shortest_path.txt
	rm can_know.txt
	rm downloaded_anon_client.txt

# testing
clean_servers:
	rm subject_1/*
	rm subject_2/*
	rm subject_3/*
	rm downloaded_anon_client.txt