#!/usr/bin/env python
from aiida import load_dbenv, is_dbenv_loaded
if not is_dbenv_loaded():
    load_dbenv()

import sys
import glob
import os

from ase.io import read

extension='.cif'
in_directory = '/home/szoupanos/structure_datasets/big/extracted_cif'
out_directory = '/home/szoupanos/structure_datasets/big/converted_xsf'

paths = glob.glob("{}/*{}".format(in_directory,extension))

i=1
for idx, filepath in enumerate(paths):
  if filepath.endswith(extension):
  	filename = os.path.basename(filepath)
  	struct = read(filepath)
  	print "({})Converting {}".format(i, filename)
  	struct.write(os.path.join(out_directory, filename + ".xsf"))
  	i = i+1
