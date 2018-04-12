#!/usr/bin/env python

import sys
import glob
import os
import random

extension='.xsf'
directory = '/home/szoupanos/structure_datasets/medium_10k/converted_xsf'
expected_file_no = 10000

paths = glob.glob("{}/*{}".format(directory,extension))
actual_file_no = len(paths)
to_be_deleted_file_no = actual_file_no - expected_file_no

if to_be_deleted_file_no == 0:
	print "Nothing to be deleted. The number of files is the expected number of files"
	sys.exit(1)

if to_be_deleted_file_no < 0:
	print "There are less files than the expected number to be deleted"
	sys.exit(2)

to_be_deleted_file_paths = set()
while len(to_be_deleted_file_paths) < to_be_deleted_file_no:
	to_be_deleted_file_paths.add(paths[random.randrange(0, actual_file_no)])

print len(to_be_deleted_file_paths)

for tbd_path in to_be_deleted_file_paths:
	os.remove(tbd_path)
