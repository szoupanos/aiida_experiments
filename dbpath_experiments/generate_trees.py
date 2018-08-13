


from aiida.backends.utils import load_dbenv,is_dbenv_loaded
if not is_dbenv_loaded():
    load_dbenv(profile='test_scaling_dbpath')


from aiida.orm import Node, load_node
from aiida.common.links import LinkType
from aiida.orm.group import Group
from aiida.common.exceptions import NotExistent
from aiida.orm.querybuilder import QueryBuilder



def get_all_children(node_pks, return_values=['id'], follow_calls=False, follow_returns=False):
    """
    Get all the children of given nodes
    :param nodes: one node or an iterable of nodes
    :param args & kwargs: additional query parameters
    :return: a list of aiida objects with all the children of the nodes
    """
    from aiida.backends.djsite.db import models
    from aiida.common.links import LinkType
    try:
        the_node_pks = list(node_pks)
    except TypeError:
        the_node_pks = [node_pks]


    link_types_to_follow = [LinkType.CREATE.value, LinkType.INPUT.value]
    if follow_calls:
        link_types_to_follow.append(LinkType.CALL.value)
    if follow_returns:
        link_types_to_follow.append(LinkType.RETURN.value)
    children = models.DbNode.objects.none()
    q_outputs = models.DbNode.aiidaobjects.filter(
            inputs__pk__in=the_node_pks,
            input_links__type__in=link_types_to_follow
        ).distinct()
    #~ count = 0
    while q_outputs.count() > 0:
        #~ count += 1
        #~ print count
        outputs = list(q_outputs)
        children = q_outputs | children.all()
        q_outputs = models.DbNode.aiidaobjects.filter(
                inputs__in=outputs,
                input_links__type__in=link_types_to_follow
            ).distinct()

    #~ return children.filter(*args,**kwargs).distinct()
    return children.values_list(*return_values)

def delete_nodes_serial(pks, follow_calls=False, follow_returns=False,
        dry_run=False, force=False, time_order=True):
    """
    Delete a set of nodes in a serialway, if deleting a bunch of nodes together 
    as above functions fails due to memory issues.

    :note: The script will also delete
    all children calculations generated from the specified nodes.

    :param pks_to_delete: a list of the PKs of the nodes to delete
    """
    from django.db import transaction
    from django.db.models import Q
    from aiida.backends.djsite.db import models
    
    # Delete also all children of the given calculations
    # Here I get a set of all pks to actually delete, including
    # all children nodes.
    if not pks:
        #~ print "Nothing to delete"
        return

    if time_order:
        pks_to_delete = QueryBuilder().append(Node, project='id', filters={'id':{'in':pks}}, tag='n').order_by({'n':{'ctime':{ 'order':'desc'}}}).all()
    else:
        pks_to_delete = pks
    #~ print "I was given {} valid pks".format(len(pks_to_delete))
    for pk, in pks_to_delete:

        #~ pks_set_to_delete_1 = set([pk])
        pks_set_to_delete = set([pk])
        try:
            #~ pks_set_to_delete.update(zip(*QueryBuilder().append(Node, filters={'id':pk}, tag='parent').append(Node, descendant_of='parent',project='id').all())[0])
            #~ pks_set_to_delete_1.update(zip(*QueryBuilder().append(Node, filters={'id':pk}, tag='parent').append(Node, descendant_of='parent',project='id').all())[0])
            pks_set_to_delete.update(_ for _, in get_all_children(pk, follow_calls=follow_calls, follow_returns=follow_returns))
        except IndexError:
            pass
        #~ print pks_set_to_delete
        #~ return
        #~ pks_set_to_delete.update(models.DbNode.objects.filter(
            #~ parents__in=pks_to_delete).values_list('pk', flat=True)
            #~ parents = pk).values_list('pk', flat=True))

        if dry_run:
            print "I would have deleted", " ".join(map(str, sorted(pks_set_to_delete)))
            continue
        #~ print "I'm deleting", " ".join(map(str, sorted(pks_set_to_delete)))
        if not(force) and raw_input("Continue?").lower() != 'y':
            continue

        #~ print "Deleting",pk,"and parents", pks_set_to_delete_2
        #~ print pks_set_to_delete_1 == pks_set_to_delete_2
        #~ continue
        # Recover the list of folders to delete before actually deleting
        # the nodes.  I will delete the folders only later, so that if
        # there is a problem during the deletion of the nodes in
        # the DB, I don't delete the folders
        folders = [load_node(_).folder for _ in pks_set_to_delete]

        with transaction.atomic():
            # Delete all links pointing to or from a given node
            models.DbLink.objects.filter(
                Q(input__in=pks_set_to_delete) |
                Q(output__in=pks_set_to_delete)).delete()
            # now delete nodes
            models.DbNode.objects.filter(pk__in=pks_set_to_delete).delete()

        # If we are here, we managed to delete the entries from the DB.
        # I can now delete the folders
        for f in folders:
            f.erase()

def create_trees(ntrees, ndepth, nbranch, no_delete=False):
    # Create ntrees trees, each of ndepth depth.
    # at every brannching nbranch branches are created.
    # 
    def create_tree(parent, depth):
        if depth == 0:
            return None
        else:
            depth -= 1
            for ibranch in range(nbranch):
                child = Node().store()
                # Calling do_create_link does not check if transitive closure is violated
                # Therefore, no queries are issued and nothing is in the buffers/cache for the first query!
                child._do_create_link(parent, '', link_type=LinkType.CREATE)
                # child._add_dblink_from(parent, link_type=LinkType.CREATE)
                create_tree(child, depth)
    groupname = 'parents-{}-{}'.format(ndepth, nbranch)
    g, created = Group.get_or_create(name=groupname)
    if not created:
        g.store()
    expect = ntrees*sum([nbranch**idepth for idepth in range(ndepth+1)])

    if no_delete:
        ntrees -= len(g.nodes)
        print '    Considering old nodes, now creating {} trees'.format(ntrees)
    else:
        print '    Deleting nodes in group'
        delete_nodes_in_group(g)

    #~ print QueryBuilder().append(Group, project='name', filters={'name':{'!==':str(groupname)}})
    #~ print QueryBuilder().append(Group, project='name', filters={'name':{'!==':str(groupname)}}).all()
    
    for group, in QueryBuilder().append(Group, filters={'name':{'!==':str(groupname)}}).all():
        delete_nodes_in_group(group)

    #~ print '    Generating {} nodes'.format(expect)
    for itree in range(ntrees):
        n = Node().store()
        g.add_nodes(n)
        create_tree(n, ndepth)
    print '    Final check'
    count = QueryBuilder().append(Node).count()
    print '    I expect {} nodes, and I have {} in db'.format( expect, count )
    assert  count == expect
    


def delete_nodes_in_group(group):
    try:
        #~ print group.name, list(group.nodes)
        delete_nodes_serial([n.pk for n in group.nodes], force=True)
    except Exception as e:
        print e



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('ntrees', help='number of trees', type=int)
    parser.add_argument('ndepth', help='depth of each tree', type=int)
    parser.add_argument('nbranch', help='Number of branches created for every node', type=int)
    parser.add_argument('--no-delete', help='Do not delete old nodes', action='store_true')

    create_trees(**vars(parser.parse_args()))
