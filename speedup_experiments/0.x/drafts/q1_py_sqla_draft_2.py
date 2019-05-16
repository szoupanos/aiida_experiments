import time
from aiida.backends.sqlalchemy import get_scoped_session
from aiida.backends.sqlalchemy.models.node import DbNode
from aiida.backends.sqlalchemy.models.group import DbGroup
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm import Load
from sqlalchemy.orm import load_only

session = get_scoped_session()

# We should see if the following query can be modified in order to get only the cell
# attributes
print "Query 1"
print "======="
# Old query with many projections
# n = session.query(DbGroup).filter(DbGroup.name == '20160903-021949').join(DbGroup.dbnodes).add_entity(DbNode).filter(DbNode.attributes.has_key('cell')).options(Load(DbGroup).load_only("id"))

# Good version
# n = session.query(DbGroup, DbNode).filter(DbGroup.name == '20160903-021949').join(DbGroup.dbnodes).filter(DbNode.attributes.has_key('cell')).options(Load(DbGroup).load_only("id"), Load(DbNode).load_only("id", "attributes"))

# Good version - v2
n = session.query(DbGroup.id, DbNode.id, DbNode.attributes[('cell')]).filter(DbGroup.name == '20160903-021949').join(DbGroup.dbnodes).filter(DbNode.attributes.has_key('cell'))




print str(n)

start = time.time()
# print n.count()
res = n.all()
# res = n.values()
end = time.time()

print "======="
print res[0:5]
# print res.next()

print "======="
print("Query time (in secs): " + str(end - start))
 
 
 
 
# print n.first()
# (a,b) = n.first()
# print b
# print b.attributes
