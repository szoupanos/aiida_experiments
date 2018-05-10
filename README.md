# aiida_experiments
AiiDA experiments on speed increase and space improvements

Speed experiments
=================
Comments on the speed experiments
- The following information are from experiments on aiidadb_mounet_new_sqla and on aiidadb_mounet_new_dj databases
- The size of the aiidadb_mounet_new_dj is 92 GB and the size of aiidadb_mounet_new_sqla is 23GB
- Both contain 7318371 number of nodes
- The experiments are carried on the a set that contains 1124139 number of nodes

For the AiiDA experiment, the SQLA query is the following:
> session.query(DbGroup.id, DbNode.uuid, DbNode.type, DbNode.label, DbNode.description, DbNode.ctime, DbNode.mtime, DbNode.nodeversion, DbNode.public, DbNode.attributes[(attr_name)]).filter(DbGroup.name == group_choice).join(DbGroup.dbnodes).filter(DbNode.attributes.has_key(attr_name))

And the Django query is the following:
> DbAttribute.objects.filter(key__startswith=attr_name).filter(dbnode__dbgroups__in=group).values_list("dbnode__dbgroups__id", "dbnode__id", "dbnode__uuid", "dbnode__type", "dbnode__label", "dbnode__description", "dbnode__ctime", "dbnode__mtime", "dbnode__nodeversion", "dbnode__public", "key","datatype", "tval", "fval", "ival", "bval", "dval")

The group_choice is "20160222-225236" and the attr_name among "cell" "kinds" "sites"

For the SQL level experiment, the queries are as follows (where cell can be replaced with any of the  "cell" "kinds" "sites" - for different attribute size):
SQLA
> SELECT db_dbgroup.id, db_dbnode.uuid, db_dbnode.type, db_dbnode.label, db_dbnode.description, db_dbnode.ctime, db_dbnode.mtime, db_dbnode.nodeversion, db_dbnode.public, db_dbnode.attributes -> 'cell' AS anon_1
aiidadb_mounet_new_sqla-# FROM db_dbgroup JOIN db_dbgroup_dbnodes AS db_dbgroup_dbnodes_1 ON db_dbgroup.id = db_dbgroup_dbnodes_1.dbgroup_id JOIN db_dbnode ON db_dbnode.id = db_dbgroup_dbnodes_1.dbnode_id
aiidadb_mounet_new_sqla-# WHERE db_dbgroup.name = '20160222-225236' AND (db_dbnode.attributes ? 'cell');
Django
> SELECT "db_dbgroup_dbnodes"."dbgroup_id", "db_dbattribute"."dbnode_id", "db_dbnode"."uuid", "db_dbnode"."type", "db_dbnode"."label", "db_dbnode"."description", "db_dbnode"."ctime", "db_dbnode"."mtime", "db_dbnode"."nodeversion", "db_dbnode"."public", "db_dbattribute"."key", "db_dbattribute"."datatype", "db_dbattribute"."tval", "db_dbattribute"."fval", "db_dbattribute"."ival", "db_dbattribute"."bval", "db_dbattribute"."dval" FROM "db_dbattribute" INNER JOIN "db_dbnode" ON ( "db_dbattribute"."dbnode_id" = "db_dbnode"."id" ) INNER JOIN "db_dbgroup_dbnodes" ON ( "db_dbnode"."id" = "db_dbgroup_dbnodes"."dbnode_id" ) WHERE ("db_dbattribute"."key"::text LIKE 'cell%' AND "db_dbgroup_dbnodes"."dbgroup_id" IN (SELECT U0."id" FROM "db_dbgroup" U0 WHERE U0."name" = '20160222-225236'));

For all the experiments the database was reset with the following command (cold database) 
sync; service postgresql stop; echo 3 > /proc/sys/vm/drop_caches; service postgresql start

More detailed information about the following results can be found at the files speed_tests_aiida.txt and speed_tests_sql_queries.txt

The SQL level results are the following ones:
---------------------------------------------
**Database: aiidadb_mounet_new_dj, Attribute choice: "cell"**  
Try 1: Time: 1420238.260 ms  
Try 2: Time: 2052195.636 ms  (too  high - should be repeated)  

Avg: 420238.260 ms  -> 420.238260 sec  

**Database: aiidadb_mounet_new_dj, Attribute choice: "kinds"**  
Try 1: Time: 1422019.282 ms  
Try 2: Time: 1421088.446 ms  
Try 3: Time: 1421582.310 ms  

Avg: 1421563.346 ms  -> 1421,563346 sec  

**Database: aiidadb_mounet_new_dj, Attribute choice: "sites"**  
Try 1: Time: 1552095.847 ms  
Try 2: Time: 1548960.599 ms  
Try 3: Time: 1550219.549 ms  
Try 4: Time: 1550509.603 ms  

Avg: 1550446.3995 ms  -> 1550,4463995 sec  

**Database: aiidadb_mounet_new_sqla, Attribute choice: "cell"**  
Try 1: Time: 19443.762 ms / 19.443762 sec  
Try 2: Time: 19796.725 ms / 19.796725 sec  
Try 3: Time: 19333.014 ms / 19.333014 sec  

Avg: 19524,500333333333333 ms  -> 19,524500333333333333 sec  

**Database: aiidadb_mounet_new_sqla, Attribute choice: "kinds"**  
Try 1: Time: 19660.286 ms  
Try 2: Time: 19918.963 ms  
Try 3: Time: 19671.706 ms  

Avg: 19750,318333333333333333 ms  -> 19,750318333333333333333 sec  

**Database: aiidadb_mounet_new_sqla, Attribute choice: "sites"**  
Try 1: Time: 12888.922 ms  (too low - maybe the database was not reset properly)
Try 2: Time: 22450.556 ms  
Try 3: Time: 22689.995 ms  
Try 4: Time: 22169.775 ms  

Avg: 22436,775333333333333333 ms  -> 22,436775333333333333333 sec  

The AiiDA level results are the following ones:
-----------------------------------------------
(we need to compare the timings of the time command and what was measured by the python time
**Database: aiidadb_mounet_new_dj, Attribute choice: "cell"**  
Try 1: Time:  1417.21063685 secs
Try 2: Time:  1419.3495729 secs
Result size: 974246

**Database: aiidadb_mounet_new_dj, Attribute choice: "kinds"**  
Try 1: Time:  1424.208534 secs
Try 2: Time:  1425.2271049 secs
Result size: 2143568

**Database: aiidadb_mounet_new_dj, Attribute choice: "sites"**  
Try 1: Time:  4856.43849516 secs
Try 2: Time:  4842.77732611 secs
Try 3: Time:  4843.52382708 secs
Result size: 67033568

**Database: aiidadb_mounet_new_sqla, Attribute choice: "cell"** 
Try 1: Time:  14.0829310417 secs
Try 2: Time:  13.9867520332 secs
Result size: 74942

**Database: aiidadb_mounet_new_sqla, Attribute choice: "kinds"**  
Try 1: Time:  16.3615100384 secs
Try 2: Time:  15.898925066 secs
Result size: 74942

**Database: aiidadb_mounet_new_sqla, Attribute choice: "sites"**  
Try 1: Time:  83.6835131645 secs
Try 2: Time:  83.6638581753 secs
Result size: 74942


Space savings
=============
Comments on structure data usage:
- we use structure data because they are a good example. I.e. they are used in calculations (inputs & outputs) and they have various information that are stored as attributes (interesting for our backend comparison)
- the CIF files contain more information than what we store in AiiDA (database) for a structure data object
- an XSF file contains information much closer to what AiIDA stores (in its database) for a structure data object
- the initial idea was to use an XYZ file but the information stored in it was incomplete (maybe the cell coordinates were missing?)

Space comparison among:
- space on disk of the XSF files (convert the provided CIFs to XSFs)
- SQLA database size when loading the XSF files
- Django database size when loading the XSF files

The XSFs will not be stored in the repository when I load them in AiiDA.

Comment from Leopold regarding space calculation
------------------------------------------------
> Spyros:
> I am not sure if the xyz will be stored in the repository when I load them
> in AiiDA. If yes, maybe I should take this space into account.
> With StructureData it shouldn't, so no need to correct for that.

Leopold:
If you were using CifData (which you aren't), you should add the size
of the repository to the size of the DB for the full amount of data
stored by AiiDA.

Spyros: I understand that the same stands for the XSF files loaded as StructureData.


Space saving experiments
------------------------

**Database size calculated by the following command:**
`SELECT pg_size_pretty(pg_database_size('aiidadb_space2_sqla')) As fulldbsize;`
**File size calculated by the following command:**
`du -h .`


> **Small datase experiment (~1000 structure data files) **  
> Dataset: /home/szoupanos/structure_datasets/small_1k/converted_xsf (provided by Leopold)  
> SQLA DB: aiidadb_space1_sqla  
> Django DB: aiidadb_space1_dj  
>   
> Django database size: 2045 MB  
> SQLA database size: 45 MB  
> File size: 65  

> **Medium dataset experiment**  
> Dataset: /home/szoupanos/structure_datasets/medium_10k/converted_xsf  
> (The dataset resulted from the 47k structure dataset that Leopold provided that was converted by converting the CIFs to XSFs by using convert_to_xsf.py and then randomly deleting files to 10k using the randomly_delete.py)
> SQLA DB: aiidadb_space2_sqla  
> Django DB: aiidadb_space2_dj  
>   
> Django database size: 22 GB (22528 MB)  
> SQLA database size: 424 MB  
> File size: 721 MB