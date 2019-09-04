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

group_choice = "20160222-225236_100k"
attr_name = "cell"

if attr_name not in ["cell", "kinds", "sites"]:
	print "The attribute filter choices are between cell, kinds and sites"
	sys.exit(1)

group_size = DbGroup.objects.values('label').annotate(node_no=Count('dbnodes')).order_by('-node_no').filter(label=group_choice)[0]['node_no']


print("Querying group: {} which size is {}".format(group_choice, group_size))
group = DbGroup.objects.filter(label=group_choice)
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


# from aiida.backends.djsite.db.models.DbAttributeBaseClass#get_all_values_for_nodepk

start_db = time.time()
res = list(n.all())
end_db = time.time()

#dballsubvalues = cls.objects.filter(dbnode__id=dbnodepk).values_list(
#    'key', 'datatype', 'tval', 'fval',
#    'ival', 'bval', 'dval')

start_ser = time.time()
for _ in res:
	data = {_[9]: {
	    "datatype": _[10],
	    "tval": _[11],
	    "fval": _[12],
	    "ival": _[13],
	    "bval": _[14],
	    "dval": _[15],
	}
	}
	dbnodepk = _[1]
	
	print("=============")
	print(data)
	print("=============")	
	
	try:
		deser = deserialize_attributes(data, sep=".",
		                          original_class=DbAttribute,
		                          original_pk=dbnodepk)

# 		print("deser", deser)		

	except AiidaException as exc:
	    exc = DbContentError(exc)
	    exc.original_exception = exc
	    raise exc

end_ser = time.time()

print("Query time (in secs): " + str(end_db - start_db) + ", Result size: " + str(len(res)))
print("Serialization time (in secs): " + str(end_ser - start_ser) + ", Result size: " + str(len(res)))
print("Size of serialized reply (in bytes): {}".format(len(str(res).encode('utf-8'))))

