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
if len(sys.argv) !=  2:
	print "You should provide the attribute that you would like to project (choices: cell, kinds sites)"
	print "Argument number", len(sys.argv)
	print "Provided arguments", sys.argv
	sys.exit(1)

attr_name = sys.argv[1]

if attr_name not in ["cell", "kinds", "sites"]:
	print "The attribute filter choices are between cell, kinds and sites"
	sys.exit(1)

n = DbAttribute.objects.filter(key__startswith=attr_name).values_list( 
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
	if not node_to_data.has_key(r[0]):
		node_to_data[r[0]] = {}
	node_to_data[r[0]][r[8]] =  {
	   "datatype": r[9],
	   "tval": r[10],
	   "fval": r[11],
	   "ival": r[12],
	   "bval": r[13],
	   "dval": r[14],
   }

for nkey, nval in node_to_data.iteritems():
   try:
	   deser = deserialize_attributes(nval, sep=".", original_class=DbAttribute, original_pk=nkey)
   except AiidaException as exc:
	   exc = DbContentError(exc)
	   exc.original_exception = exc
	   raise exc
ser_time += time.time() - start_ser

print("Query time (in secs) [no serialization of attributes]: " + str(db_time) + ", Result size: " + str(len(res)))
print("Serialization time (in secs): " + str(ser_time) + ", Result size: " + str(len(res)))
print("Size of non-serialized reply (in bytes): {}".format(len(str(res).encode('utf-8'))))
