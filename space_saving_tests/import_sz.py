#!/usr/bin/env python
from aiida import load_dbenv, is_dbenv_loaded
if not is_dbenv_loaded():
    load_dbenv()
from aiida.orm.group import Group

# Import aiida structure class
from aiida.orm.data.structure import StructureData
from aiida.common.exceptions import UniquenessError
# Os
import os
import glob
import sys

importer = 'ase'

if importer == 'ase':
    from ase.io import read as read_xyz
    aiida_convert = lambda x: StructureData(ase=x)
elif importer == 'pymatgen':
    from pymatgen import Structure
    read_xyz = Structure.from_file
    aiida_convert = lambda x: StructureData(pymatgen_structure=x)

extension='.xyz'
group_name='zeolite_import'
directory = '../structures_10_xyz'
#directory = 'structures_0004'

# Create a group where to put the structure (for later export)
# N.B. You only have to create a group once, not every time you create a new structure
#try:
#    g1 = Group(name=group_name, description='import for testing djnago/sqlalchemy performance')
#    g1.store()
#except Exception as e:
##except UniquenessError as e:
#    print "Group {} already exists".format(group_name)
#    g1 = Group.get_from_string(group_name)
#g1 = Group.get_from_string(group_name)

paths = glob.glob("{}/*{}".format(directory,extension))

# print "{}/*{}".format(directory,extension)
# print paths
# 
# sys.exit(0)


# Import structure first in ase, then in aiida
#for idx, filename in enumerate(os.listdir(directory)):
#  if filename.endswith(extension):
#    struct = read_cif(filename)
#    s1 = aiida_convert(struct)

for idx, filename in enumerate(paths):
  if filename.endswith(extension):
    struct = read_xyz(filename)
    s1 = aiida_convert(struct)
    #import pdb; pdb.set_trace()
    #Store the structure
    s1.store()

    # Check that the structure has been loaded correctly
    #print "Content of the node with pk {}".format(s1.pk)
    label = filename[:-4]
    s1.label = label
    print "Node infos -- pk:{}, uuid:{}, label:{}".format(s1.pk,s1.uuid,s1.label)
    ## Add the structure to the group
    #g1.add_nodes(s1)

print "Total number of structures: {}".format(idx+1)


## Check that the structure has boen put in the group
print "##########Checking node inclusion in group {}".format(group_name)
#for node in g1.nodes:
#    print node.pk, s1.pk

# From a bash shell run
# verdi export -g acenes -- acenes.aiida
# to export the group in a compressed archive.
# In[ ]:
