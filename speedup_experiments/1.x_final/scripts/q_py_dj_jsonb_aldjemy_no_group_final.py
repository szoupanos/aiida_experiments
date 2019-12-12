# Comment: We don't project extras. Is this what we want

import time
import sys

import aiida.backends.djsite.db.models as djmodels
from aiida.orm.implementation.django.querybuilder import DjangoQueryBuilder

from sqlalchemy import func

# Check the input arguments
if len(sys.argv) !=  2:
	print("You should provide the attribute that you would like to project (choices: cell, kinds sites)")
	print("Argument number", len(sys.argv))
	print("Provided arguments", sys.argv)
	sys.exit(1)

session = DjangoQueryBuilder.get_session()

attr_name = sys.argv[1]

if attr_name not in ["cell", "kinds", "sites"]:
	print("The attribute filter choices are between cell, kinds and sites")
	sys.exit(1)

n = session.query(
	djmodels.DbGroup.sa.id, 
	djmodels.DbNode.sa.uuid, 
	djmodels.DbNode.sa.node_type, 
	djmodels.DbNode.sa.process_type, 
	djmodels.DbNode.sa.label,
	djmodels.DbNode.sa.description, 
	djmodels.DbNode.sa.ctime, 
	djmodels.DbNode.sa.mtime,
	djmodels.DbNode.sa.attributes[(attr_name)]
	).join(
	djmodels.DbGroup.sa.dbnodes).filter(djmodels.DbNode.sa.attributes.has_key(attr_name))

start = time.time()
res = list(n.all())
end = time.time()

n = None

print("Query time (in secs): " + str(end - start) + ", Result size: " + str(len(res)))

ser_size = 0
for r in res:
	ser_size += len(str(r).encode('utf-8'))
print("Size of serialized reply (in bytes): {}".format(ser_size))
