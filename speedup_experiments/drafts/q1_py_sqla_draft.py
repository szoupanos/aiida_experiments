import time
from aiida.backends.sqlalchemy import get_scoped_session
from aiida.backends.sqlalchemy.models.node import DbNode
from aiida.backends.sqlalchemy.models.group import DbGroup
from sqlalchemy.orm.attributes import flag_modified

session = get_scoped_session()

group = session.query(DbGroup).filter(DbGroup.name == '20160903-021949')
print group

# n = session.query(DbGroup).filter(DbGroup.name == '20160903-021949').join(DbNode)
# print list(n)

print "========================================================"

# n = session.query(DbNode).join(DbGroup).filter(DbGroup.name == '20160903-021949')
# n = session.query(DbGroup).join(DbNode)
# print n.count()

# n = session.query(DbGroup).join(DbNode, DbGroup.dbnodes.dbnode_id==DbNode.id)



# print "Query 0.1"
# print "========="
# n = session.query(DbGroup).join(DbGroup.dbnodes)
# print str(n)
# print n.count()

print "Query 1"
print "======="
n = session.query(DbGroup).join(DbGroup.dbnodes)
print str(n)
print n.first()

print "Query 2"
print "======="
n = session.query(DbGroup)
print str(n)
# print n.count()
print n.first()

print "Query 3"
print "======="
print str(n)
n = session.query(DbGroup)
print n.count()

print "Query 4"
print "======="
n = session.query(DbGroup).join(DbGroup.dbnodes).add_entity(DbNode)
print str(n)
print n.first()

print "Query 5"
print "======="
n = session.query(DbGroup).filter(DbGroup.name == '20160903-021949').join(DbGroup.dbnodes).add_entity(DbNode).filter(DbNode.attributes.has_key('cell'))
print str(n)




# address_subq = session.query(DbGroup).filter(DbGroup.name == '20160903-021949').subquery()
# q = session.query(DbNode).join(address_subq)
# print list(q)


# qb = QueryBuilder()
# qb.append(Group, tag='group', filters={'name':{'==':'20160903-021949'}})
# qb.append(Node, member_of='group')
# 
# start = time.time()
# q = qb.all()
# end = time.time()
# print("Elapsed time (in secs): " + str(end - start))

