import time
import sys

from aiida.backends.djsite.db.models import DbAttribute
from aiida.backends.djsite.db.models import DbNode
from aiida.backends.djsite.db.models import DbGroup
from django.db.models import Count

from aiida.common.exceptions import AiidaException
from aiida.backends.djsite.db.models import deserialize_attributes
from aiida.common.exceptions import DbContentError

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

group_size = DbGroup.objects.values('label').annotate(node_no=Count('dbnodes')).order_by('-node_no').filter(label=group_choice)[0]['node_no']


print("Querying group: {} which size is {}".format(group_choice, group_size))
group = DbGroup.objects.filter(label=group_choice)
# DbAttribute.objects.filter(key__startswith=attr_name).filter(dbnode__dbgroups__in=group).filter(dbnode__id=381696).values_list(
n = DbAttribute.objects.filter(key__startswith=attr_name).filter(dbnode__dbgroups__in=group).values_list(
	"dbnode__dbgroups__id", 
	"dbnode__id", 
	"dbnode__uuid", 
	"dbnode__node_type", 
	"dbnode__process_type", 
	"dbnode__label", 
	"dbnode__description", 
	"dbnode__ctime", 
	"dbnode__mtime", 
	"key",
	"datatype", 
	"tval", 
	"fval", 
	"ival", 
	"bval", 
	"dval"
	)

# DB time
db_time = 0
# Serialization time
ser_time = 0


start_db = time.time()
res = list(n.all())
db_time += time.time() - start_db

start_ser = time.time()
node_to_data = {}
for r in res:
	if not node_to_data.has_key(r[1]):
		node_to_data[r[1]] = {}
	node_to_data[r[1]][r[9]] =  {
	   "datatype": r[10],
	   "tval": r[11],
	   "fval": r[12],
	   "ival": r[13],
	   "bval": r[14],
	   "dval": r[15],
   }

for nkey, nval in node_to_data.iteritems():
   try:
	   #print("=========================")
	   #print("nkey: " + str(nkey))
	   deser = deserialize_attributes(nval, sep=".", original_class=DbAttribute, original_pk=nkey)
	   #import json
	   #parsed = json.loads(deser)
	   #print("deser, ")
	   #print(json.dumps(deser, indent=4, sort_keys=True))
   except AiidaException as exc:
	   exc = DbContentError(exc)
	   exc.original_exception = exc
	   raise exc
ser_time += time.time() - start_ser

print("Query time (in secs) [no serialization of attributes]: " + str(db_time) + ", Result size: " + str(len(res)))
print("Serialization time (in secs): " + str(ser_time) + ", Result size: " + str(len(res)))
print("Size of non-serialized reply (in bytes): {}".format(len(str(res).encode('utf-8'))))
