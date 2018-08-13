

from aiida.backends.utils import load_dbenv,is_dbenv_loaded
if not is_dbenv_loaded():
    load_dbenv(profile='test_scaling_dbpath')


import numpy as np

from resource import getrusage as resource_usage, RUSAGE_SELF
from time import time as timestamp
from aiida.orm.querybuilder import QueryBuilder
from aiida.orm import Node, Group

#~ In [1]: def get_dbpath_size(depth, branch):
   #~ ...:     count = 0
   #~ ...:     for d in range(1, depth+1):
   #~ ...:         count += d*(branch)**d
   #~ ...:     return count

def unix_time(function, *args, **kwargs):
    '''Return `real`, `sys` and `user` elapsed time, like UNIX's command `time`
    You can calculate the amount of used CPU-time used by your
    function/callable by summing `user` and `sys`. `real` is just like the wall
    clock.
    Note that `sys` and `user`'s resolutions are limited by the resolution of
    the operating system's software clock (check `man 7 time` for more
    details).
    '''
    start_time, start_resources = timestamp(), resource_usage(RUSAGE_SELF)
    function(*args, **kwargs)
    end_resources, end_time = resource_usage(RUSAGE_SELF), timestamp()

    return {'real': end_time - start_time,
            'sys': end_resources.ru_stime - start_resources.ru_stime,
            'user': end_resources.ru_utime - start_resources.ru_utime}


def get_children_one_node(pk, with_dbpath):
    qb = QueryBuilder(with_dbpath=with_dbpath).append(Node, tag='p', filters={'id':pk}).append(Node, descendant_of='p', project='uuid')
    res = qb.all()

#~ def get_children_of_nodes(pks_to_search, with_dbpath):

def get_children(ndepth, nbranch, counts, dbpath):
    groupname = 'parents-{}-{}'.format(ndepth, nbranch)

    pks = [n.pk for n in Group.get(groupname).nodes]
    pks_to_search = np.random.choice(pks, size=counts, replace=False)

    times = np.empty(len(pks_to_search))
    for idx, pk in enumerate(pks_to_search):
        timings = unix_time(get_children_one_node, pk=pk, with_dbpath=dbpath)
        times[idx] = (timings['user'] + timings['sys'])
    print '{:.10f} {:.10f}'.format(times.mean(), times.std() / np.sqrt(counts))
    #~ timings = unix_time(get_children_of_nodes, pks_to_search=pks_to_search, with_dbpath=dbpath)
    #~ print '{:.6f}'.format((timings['user'] + timings['sys'])/counts)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('ndepth', help='depth of each tree', type=int)
    parser.add_argument('nbranch', help='Number of branches created for every node', type=int)
    parser.add_argument('counts', help='number of counts', type=int)
    parser.add_argument('--with-dbpath', dest='dbpath',help='use dbpath', action='store_true')
    parser.add_argument('--no-dbpath', dest='dbpath', help='use dbpath', action='store_false')
    parser.set_defaults(dbpath=False)
    #~ parser.add_argument('ndepth', help='depth of each tree', type=int)
    #~ parser.add_argument('nbranch', help='Number of branches created for every node', type=int)
    #~ delete_nodes_in_group()
    get_children(**vars(parser.parse_args()))
