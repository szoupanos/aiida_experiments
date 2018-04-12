#!/usr/bin/env python

import sys
import glob
import os

from ase.io import read

extension='.cif'
in_directory = '/home/szoupanos/structure_datasets/small_1k/extracted_cif/structures_1000'
out_directory = '/home/szoupanos/structure_datasets/small_1k/converted_xsf'

paths = glob.glob("{}/*{}".format(in_directory,extension))

i=1
for idx, filepath in enumerate(paths):
  if filepath.endswith(extension):
  	filename = os.path.basename(filepath)
  	struct = read(filepath)
  	print "({})Converting {}".format(i, filename)
  	struct.write(os.path.join(out_directory, filename + ".xsf"))
  	i = i+1
