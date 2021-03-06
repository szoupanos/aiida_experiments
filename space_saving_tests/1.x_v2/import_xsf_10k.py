#!/usr/bin/env python
from aiida import load_dbenv, is_dbenv_loaded
if not is_dbenv_loaded():
    load_dbenv()

import sys
import glob
import os

from ase.io import read
#from aiida.orm.data.structure import StructureData
from aiida.orm import StructureData

extension='.xsf'
#in_directory = '/home/szoupanos/structure_datasets/medium_10k/converted_xsf'
in_directory = '/scratch/spyros_backup/theospc38/home/szoupanos/structure_datasets/medium_10k/converted_xsf'

paths = glob.glob("{}/*{}".format(in_directory,extension))

i=1
for idx, filepath in enumerate(paths):
  if filepath.endswith(extension):
  	filename = os.path.basename(filepath)
  	print "({}) Creating & storing AiiDA StructureData for {}".format(i, filename)
  	StructureData(ase=read(filepath)).store()
  	i = i+1

