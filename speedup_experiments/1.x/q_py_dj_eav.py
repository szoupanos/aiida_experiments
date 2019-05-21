import time
import sys

from aiida.backends.djsite.db.models import DbAttribute
from aiida.backends.djsite.db.models import DbNode
from aiida.backends.djsite.db.models import DbGroup
from django.db.models import Count

# Check the input arguments
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

group_size = DbGroup.objects.values('name').annotate(node_no=Count('dbnodes')).order_by('-node_no').filter(name=group_choice)[0]['node_no']


print("Querying group: {} which size is {}".format(group_choice, group_size))
group = DbGroup.objects.filter(name=group_choice)
n = DbAttribute.objects.filter(key__startswith=attr_name).filter(dbnode__dbgroups__in=group).values_list("dbnode__dbgroups__id", "dbnode__id", "dbnode__uuid", "dbnode__type", "dbnode__label", "dbnode__description", "dbnode__ctime", "dbnode__mtime", "dbnode__nodeversion", "dbnode__public", "key","datatype", "tval", "fval", "ival", "bval", "dval")

start = time.time()
res = list(n.all())
end = time.time()

print("Query time (in secs): " + str(end - start) + ", Result size: " + str(len(res)))
print("Size of serialized reply (in bytes): {}".format(len(str(res).encode('utf-8'))))
