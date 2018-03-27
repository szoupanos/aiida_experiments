import time

# qb = QueryBuilder()
# qb.append(Group, tag='group', filters={'name':{'==':'20160903-021949'}})
# qb.append(Node, member_of='group')
# 
# start = time.time()
# q = qb.all()
# end = time.time()
# print("Elapsed time (in secs): " + str(end - start))


# DJango query
from aiida.backends.djsite.db.models import DbNode
from aiida.backends.djsite.db.models import DbGroup

print "Query 1"
print "======="
print DbGroup.objects.all()

print "Query 2"
print "======="
print DbGroup.objects.filter(name='20160903-021949').all()

print "Query 3"
print "======="
print DbGroup.objects.filter(name='20160903-021949').query

print "Query 4"
print "======="
from aiida.backends.djsite.db.models import DbAttribute
print DbAttribute.objects.filter(dbnode__pk=1).query

print "Query 5"
print "======="
nodes = DbNode.objects.filter(pk=6)
group = DbGroup.objects.filter(name='20160903-021949').filter(dbnodes__in=nodes)
print group.query

print "Query 6"
print "======="
# attributes = DbAttribute.objects.first()
attributes = DbAttribute.objects.all()[:10]
print attributes.query
print attributes

print "Query 7"
print "======="
# I have to find a way to do a star join
nodes = DbNode.objects.all()
attributes = DbAttribute.objects.filter(dbnode__in=nodes)
group = DbGroup.objects.filter(name='20160903-021949').filter(dbnodes__in=nodes)
print group.query

print "Query 8"
print "======="
nodes = DbNode.objects.filter(dbattributes__key='state')
print nodes.query

print "Query 9"
print "======="
nodes1 = DbNode.objects.filter(dbattributes__key='state')
print nodes1.query

print "Query 10"
print "========"
nodes2 = DbNode.objects.filter(dbgroups__name='lala')
print nodes2.query

print "Query 11"
print "========"
nodes = DbNode.objects.filter(dbattributes__key='cell')
group = DbGroup.objects.filter(name='20160903-021949').filter(dbnodes__in=nodes)
print group.query

print "Query 12"
print "========"
group = DbGroup.objects.filter(name='20160903-021949')
attributes = DbAttribute.objects.filter(key='cell').filter(dbnode__dbgroups__in=group)

# nodes = DbNode.objects.all()
# attributes = DbAttribute.objects.filter(key='cell').filter(dbnode__in=nodes)


# nodes = DbNode.objects.filter(dbattributes__key='cell')
# group = DbGroup.objects.filter(name='20160903-021949').filter(dbnodes__in=nodes)
print attributes.query

# pw_calc = Group.get(pk=1139193).nodes.next()
# structure=pw_calc.out.output_structure
# StructureData=DataFactory('structure')
# qstruc = StructureData.query(children__pk=structure.pk)
# qic = InlineCalculation.query(inputs__in=qstruc).filter(
#         inputs__dbattributes__in=models.DbAttribute.objects.filter(
#         tval__endswith='alvarez')).distinct()
# print qic.query




# from aiida_quantumespresso.calculations.pw import PwCalculation
# from aiida_quantumespresso.tools.dbexporters.tcod_plugins.pw import PwTcodtranslator
# print DbGroup.objects.filter(dbnodes__type=PwTcodtranslator._plugin_type_string).query
# print DbGroup.objects.filter(dbnodes__type="PWCalculation").first()

# import time
# from aiida.backends.sqlalchemy import get_scoped_session
# from aiida.backends.sqlalchemy.models.node import DbNode
# from aiida.backends.sqlalchemy.models.group import DbGroup
# from sqlalchemy.orm.attributes import flag_modified

# print "Query 2"
# print "======="
# n = session.query(DbGroup).filter(DbGroup.name == '20160903-021949').join(DbGroup.dbnodes).add_entity(DbNode).filter(DbNode.attributes.has_key('cell'))
# print str(n)
# print n.first()
# print n.count()
# 
# (a,b) = n.first()
# print b
# print b.attributes




