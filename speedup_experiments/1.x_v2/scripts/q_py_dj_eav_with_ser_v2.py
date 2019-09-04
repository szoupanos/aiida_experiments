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
ns = DbNode.objects.filter(dbgroups__in=group).values_list(
	"dbgroups__id", 
	"id", 
	"uuid", 
	"node_type", 
	"process_type", 
	"label", 
	"description", 
	"ctime", 
	"mtime",
	)


# DB time
db_time = 0
# Serialization time
ser_time = 0
# Size of reply
res_size = 0

start_db = time.time()
res = list(ns.all())
db_time += time.time() - start_db

res_size += len(str(res).encode('utf-8'))

for n in res:
   start_db = time.time()

   dballsubvalues = DbAttribute.objects.filter(dbnode__id=n[1]).filter(key__startswith=attr_name).values_list(
	  'key', 'datatype', 'tval', 'fval',
	  'ival', 'bval', 'dval')
   db_time += time.time() - start_db

   start_ser = time.time()
   data = {_[0]: {
	   "datatype": _[1],
	   "tval": _[2],
	   "fval": _[3],
	   "ival": _[4],
	   "bval": _[5],
	   "dval": _[6],
   } for _ in dballsubvalues
   }
   try:
	   deser = deserialize_attributes(data, sep=".", original_class=DbAttribute, original_pk=n[1])
   except AiidaException as exc:
	   exc = DbContentError(exc)
	   exc.original_exception = exc
	   raise exc

   ser_time += time.time() - start_ser
   res_size += len(str(deser).encode('utf-8'))

print("Query time (in secs): " + str(db_time) + ", Result size: " + str(len(res)))
print("Serialization time (in secs): " + str(ser_time) + ", Result size: " + str(len(res)))
print("Size of serialized reply (in bytes): {}".format(res_size))

