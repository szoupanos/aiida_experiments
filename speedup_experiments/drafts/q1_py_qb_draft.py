import time


print "===== Query 1 ====="
qb = QueryBuilder()
qb.append(Group, tag='group', filters={'name':{'==':'20160903-021949'}})
qb.append(Node, member_of='group')

start = time.time()
q = qb.all()
end = time.time()
print("Elapsed time (in secs): " + str(end - start))

print "===== Query 2 ====="
qb = QueryBuilder()
qb.append(PwCalculation, project=['*'], tag='calc')
qb.append(
    ParameterData,
    input_of='calc',
    filters={'attributes.SYSTEM.ecutwfc':{'>':30.0}},
    project=[
        'attributes.SYSTEM.ecutwfc',
        'attributes.SYSTEM.ecutrho',
    ]
)
