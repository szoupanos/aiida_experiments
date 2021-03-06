import time
import sys

from aiida.backends.djsite.db.models import DbGroup
from django.db.models import Count

# Check the input arguments
if len(sys.argv) !=  3:
	print("You should provide the group of nodes that interest you and the attribute that you would like to project (choices: cell, kinds sites)")
	print("Argument number", len(sys.argv))
	print("Provided arguments", sys.argv)
	sys.exit(1)

group_choice = sys.argv[1]
attr_name = sys.argv[2]

if attr_name not in ["cell", "kinds", "sites"]:
	print("The attribute filter choices are between cell, kinds and sites")
	sys.exit(1)

group_size = DbGroup.objects.values('label').annotate(node_no=Count('dbnodes')).order_by('-node_no').filter(label=group_choice)[0]['node_no']


print("Querying group: {} which size is {}".format(group_choice, group_size))
qb = QueryBuilder()
qb.append(Group, filters={"label":{"==": "20160222-225236"}}, project=["id"], tag="my_group")
qb.append(Node, project=["id", "uuid", "node_type", "process_type" , "label", "description", "ctime", "mtime", "nodeversion", "public", "attributes." + group_choice], with_group="my_group")

start = time.time()
res = list(qb.all())
end = time.time()

# print "==============================="
print("Query time (in secs): " + str(end - start) + ", Result size: " + str(qb.count()))
