\timing
SELECT db_dbnode.id AS db_dbnode_id, db_dbnode.uuid AS db_dbnode_uuid, db_dbnode.type AS db_dbnode_type, db_dbnode.label AS db_dbnode_label, db_dbnode.description AS db_dbnode_description, db_dbnode.ctime AS db_dbnode_ctime, db_dbnode.mtime AS db_dbnode_mtime, db_dbnode.dbcomputer_id AS db_dbnode_dbcomputer_id, db_dbnode.user_id AS db_dbnode_user_id, db_dbnode.public AS db_dbnode_public, db_dbnode.nodeversion AS db_dbnode_nodeversion, db_dbnode.attributes AS db_dbnode_attributes, db_dbnode.extras AS db_dbnode_extras
        FROM db_dbnode JOIN db_dbgroup_dbnodes AS db_dbgroup_dbnodes_1 ON db_dbnode.id = db_dbgroup_dbnodes_1.dbnode_id JOIN db_dbgroup ON db_dbgroup.id = db_dbgroup_dbnodes_1.dbgroup_id
        WHERE (db_dbnode.attributes ? 'cell') AND db_dbgroup.name LIKE '20160216%213117'
