import time
from aiida.backends.djsite.db.models import DbAttribute
from aiida.backends.djsite.db.models import DbGroup

# DJango query
from aiida.backends.djsite.db.models import DbNode
from aiida.backends.djsite.db.models import DbGroup

print "Query 1 - group 20160903-021949"
print "==============================="
# group = DbGroup.objects.filter(name='20160903-021949')
# n = DbAttribute.objects.filter(key__startswith='cell').filter(dbnode__dbgroups__in=group).values_list("id", "dbnode__id")
# print n.query
group = DbGroup.objects.filter(name='20160903-021949')
n = DbAttribute.objects.filter(key__startswith='cell').filter(dbnode__dbgroups__in=group).values_list("key","datatype", "tval", "fval", "ival", "bval", "dval", "dbnode__id", "dbnode__dbgroups__id")
print n.query


# "db_dbattribute"."dbnode_id", "db_dbattribute"."key", "db_dbattribute"."datatype", "db_dbattribute"."tval", "db_dbattribute"."fval", "db_dbattribute"."ival", "db_dbattribute"."bval", "db_dbattribute"."dval"


start = time.time()
# print n.count()
res = list(n.all())
end = time.time()

print "======="
print res[0:5]


print "======="
print("Query time (in secs): " + str(end - start))
