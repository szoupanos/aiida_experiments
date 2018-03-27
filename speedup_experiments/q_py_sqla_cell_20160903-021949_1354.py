import time
from aiida.backends.sqlalchemy import get_scoped_session
from aiida.backends.sqlalchemy.models.node import DbNode
from aiida.backends.sqlalchemy.models.group import DbGroup
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm import Load
from sqlalchemy.orm import load_only

session = get_scoped_session()

# Group size -> 1354 | 20160903-021949
print "Query 1 - group 20160903-021949"
print "==============================="
# Good version - v2
n = session.query(DbGroup.id, DbNode.uuid, DbNode.type, DbNode.label, DbNode.description, DbNode.ctime, DbNode.mtime, DbNode.nodeversion, DbNode.public, DbNode.attributes[('cell')]).filter(DbGroup.name == '20160903-021949').join(DbGroup.dbnodes).filter(DbNode.attributes.has_key('cell'))

print str(n)

start = time.time()
res = n.all()
end = time.time()

# print "======="
# print res[0:5]

print "======="
print("Query time (in secs): " + str(end - start))

