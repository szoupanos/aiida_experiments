import time
import sys

from aiida.backends.sqlalchemy import get_scoped_session
from aiida.backends.sqlalchemy.models.node import DbNode
from aiida.backends.sqlalchemy.models.group import DbGroup
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm import Load
from sqlalchemy.orm import load_only
from sqlalchemy import func

session = get_scoped_session()

# Check that the 
if len(sys.argv) !=  3:
	print "You should provide the group of nodes that interest you and the attribute that you would like to project (choices: cell, kinds sites)"
	print "Argument number", len(sys.argv)
	print "Provided arguments", sys.argv
	sys.exit(1)

group_choice = sys.argv[1]
attr_name = sys.argv[2]

if attr_name not in ["cell", "kinds", "sites"]:
	print "The attribute filter choices are between cell, kinds and sites"
	sys.exit(1)

_, group_size = session.query(DbGroup.name, func.count(DbNode.id)).join(DbGroup.dbnodes).group_by(DbGroup.name).filter(DbGroup.name==group_choice).all()[0]

print "Querying group:", group_choice, "which size is", group_size
# print "==============================="

n = session.query(DbGroup.id, DbNode.uuid, DbNode.type, DbNode.label, DbNode.description, DbNode.ctime, DbNode.mtime, DbNode.nodeversion, DbNode.public, DbNode.attributes[(attr_name)]).filter(DbGroup.name == group_choice).join(DbGroup.dbnodes).filter(DbNode.attributes.has_key(attr_name))


start = time.time()
res = n.all()
end = time.time()

# print "======="
# print res[0:5]

# print "==============================="
print("Query time (in secs): " + str(end - start) + ", Result size: " + str(n.count()))
