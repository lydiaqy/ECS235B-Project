clean:
# Deletes all subject directories
	ls -d subject_*/ | xargs rm -rf
# Deletes the object directory
	ls -d objects/ | xargs rm -rf