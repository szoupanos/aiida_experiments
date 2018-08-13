#!/bin/bash


#ntreelist=`seq 10 1 10`
#ndepthlist=`seq 4 1 7 `
#nbranchlist=`seq 2 1 6`

ntreelist=`seq 2000 2000 10000`
ndepthlist=`seq 2 2 2`
nbranchlist=`seq 2 2 2`

withdbpathlist="--with-dbpath --no-dbpath"

#for withdbpath in $withdbpathlist; do
#    filename="timings${withdbpath}.dat"
#    rm $filename
#done


echo $ndepthlist

for ndepth in $ndepthlist; do
    for nbranch in $nbranchlist; do
       psql test_scaling_dbpath -c "delete from db_dbpath;"
       psql test_scaling_dbpath -c "delete from db_dblink;"
       psql test_scaling_dbpath -c "delete from db_dbgroup_dbnodes;"
       psql test_scaling_dbpath -c "delete from db_dbnode;"
       psql test_scaling_dbpath -c "delete from db_dbgroup;"
       for ntree in $ntreelist; do
	    echo "@ $ntree $ndepth $nbranch"
            dumpfile="db-${ntree}-${ndepth}-${nbranch}.psql"
	    if [ -f $dumpfile ]; then
		echo "Dump file exists"
		dropdb test_scaling_dbpath && createdb test_scaling_dbpath
		psql test_scaling_dbpath -f $dumpfile > /dev/null
	    else 		
                python generate_trees.py $ntree $ndepth $nbranch --no-delete  #> /dev/null
                pg_dump test_scaling_dbpath > $dumpfile
	    fi 
            for withdbpath in $withdbpathlist; do
	       echo " $withdbpath"
               filename="timings${withdbpath}.dat"
	       #psql test_scaling_dbpath -c "select count(*) from db_dbpath;"	
               time=`python get_query_timings.py $ndepth $nbranch 1000 $withdbpath`
               echo "$ntree $ndepth $nbranch $time" >> $filename
           done
        done
    done
done
