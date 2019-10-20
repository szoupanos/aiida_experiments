# aiida_benchmarks using AiiDA v1

There are three different kinds of benchmarks that have been peformed.
Benchmarks to measure speed gains, benchmark to measure the data transfered and benchmarks to measure storage space gains.
All the benchmarks found below are based on the Django EAV version which is just before and after the conversion to AiiDA Django JSONB.
This corresponds to commit 1956cfad8 for AiiDA Django EAV and a7c3ac4e4 of aiida/django_jsonb branch.


Speed benchmarks
================
These benchmarks were performed using the AiiDA Django JSONB and AiiDA Django EAV using an extension of Mounet's database provided by Davide. The benchmarks were peformed on the full database (around 7 milion nodes) as well as on subsets of the database (on 200K nodes and 300K nodes). The results using a cold database (database after restart with clean cache) and a warm database (launching the same query for a second time - the database cache contains the previous results) are presented.

All the benchmarks were run once (so there might be a few descrepancies in the numbers - especially for timings that could be less than a second or a few seconds).


Django JSONB -  comparison on the benefits of a GIN index and datetime deactivation (full database)
----------------------------------------------------------------------------------------------------------------------------------------------------
In this set of benchmarks, we check the benefints of using a GIN index in JSONB related queries as well as well the benefits from not performing the datetime conversion.

**GIN and datetime benefits on a cold database - Full database benchmark**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_cold_gin_comparison.svg "")

**GIN and datetime benefits on a warm database - Full database benchmark**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_warm_gin_comparison.svg "")

**Comments:**
- Overall the graphs seem normal. 
- The performance gains of the GIN index can be seen mainly in the benchmarks of 'Cells' and 'Kinds' (total execution time). 
- The performance gains are also obvious at the SQL time of the graphs for all kinds of attributes 'Cells', 'Kinds' and 'Sites'.
- The usage of GIN index doesn't seem to have an effect on the total execution time for 'Sites'.
- What I can not explain is why the total execution time with GIN and datetime conversion is higher than the total execution time without GIN and datetime conversion. If we remove the SQL time from the total execution time of these graphs (JSONB with GIN, with DT and JSONB no GIN with DT), these results become even more inexplicable. In a few words, it seems that the datetime conversion takes more time for the same nodes when a GIN index is not used!! This difference & pattern appears in the benchmarks of this section (#1 & #2) but also, on a much smaller scale, at the measurements of the following sections (that could be also at the level of error). Any ideas?

**Source of the benchmarks**
The benchmarks that correspond to this section are #1 and #2 of the following notebook
https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/graphs.ipynb


Data come from the following files:
- speed_tests_aiida_gin_test_jsonb_with_gin_full_db.txt
- speed_tests_aiida_gin_test_jsonb_with_gin_no_datetime_full_db.txt
- speed_tests_aiida_gin_test_jsonb_without_gin_full_db.txt
- speed_tests_aiida_gin_test_jsonb_without_gin_no_datetime_full_db.txt

 Databases used:
- aiida_dj_jsonb_original_seb_copy_m37_copy (With GIN index on attributes)
- aiida_dj_jsonb_original_seb_copy_m37 (Without GIN index on attributes)


Django JSONB -  comparison on the benefits of a GIN index and datetime deactivation vs Django EAV (partial database)
----------------------------------------------------------------------------------------------------------------------------------------------------
In this set of benchmarks, we check the benefits of using a GIN index in JSONB related queries as well as  the benefits from using the datetime and we make the direct comparison with the performance of the Django EAV version of AiiDA.

The main characteristic of the benchmarks of this section is that the databases used contain only the nodes that interest us (200k / 300k) - in comparison to the benchmarks of the following sections that contain all the nodes and we focus only on a group of nodes that we find interesting. 

Having databases with only the nodes that interest us, allow us to demonstrate the benefits of a GIN index - from the analysis of the query plans, it seems that the GIN index is not used when querying the attributes of nodes that belong to a specific group.


**JSONB GIN and datetime benefits vs EAV with datetime - 200k node database - Cold DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_cold_gin_comparison.svg "")

**JSONB GIN and datetime benefits vs EAV with datetime - 200k node database - Warm DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_warm_gin_comparison.svg "")

**JSONB GIN and datetime benefits vs EAV with datetime - 300k node database - Cold DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_cold_gin_comparison.svg "")

**JSONB GIN and datetime benefits vs EAV with datetime - 300k node database - Warm DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_warm_gin_comparison.svg "")

**Comments:**
- The graphs are good to show the difference between the EAV and the JSONB approach.
- They are also good to show that the speed difference gets significant when a lot of attributes need to be de-serialized E.g. 'Sites'
- The graphs are not good to show the differences between the variations in the exeucution of JSONB approach (e.g. with or without GIN, with or without GIN serialization)
- Some of the results (200k nodes, cold DB, Sites, JSONB with GIN & no datetime) don't make a lot of sense. The execution time is too high. But maybe something happened during that measurement.

**Source of the benchmarks**
The benchmarks that correspond to this section are #3, #4, #5 and #6 of the following notebook
https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/graphs.ipynb

Data come from the following files:
- speed_tests_aiida_gin_test_eav.txt
    - the total time reported in the graphs is the addition of query time 
      and serialization time. The SQL time is the time reported by PostgreSQL
- speed_tests_aiida_gin_test_jsonb_with_gin_no_datetime.txt
- speed_tests_aiida_gin_test_jsonb_with_gin.txt
- speed_tests_aiida_gin_test_jsonb_without_gin_no_datetime.txt
- speed_tests_aiida_gin_test_jsonb_without_gin.txt

 Databases used:
- aiida_dj_jsonb_original_seb_copy_m37_copy_200_gin
- aiida_dj_jsonb_original_seb_copy_m37_copy_200_no_gin
- aiida_dj_jsonb_original_seb_copy_m36_copy_200_gin
- aiida_dj_jsonb_original_seb_copy_m37_copy_300_gin
- aiida_dj_jsonb_original_seb_copy_m37_copy_300_no_gin
- aiida_dj_jsonb_original_seb_copy_m36_copy_300_gin




Django JSONB (with and without datetime conversion)
---------------------------------------------------------------------------------
In this set of benchmarks we check the overhead of the datetime conversion for the Django JSONB version with cold and warm database. The database has a GIN index on the attributes but it is not used (maybe it is not considered useful for these queries). The queries were performed on a group containing 200k nodes of the full database of 7 milion nodes.

**With & without datetime conversion on a group of 200K nodes and a cold database**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_cold_with_attr_jsonb_datetime.svg "")

**With & without datetime conversion on a group of 200K nodes and a warm database**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_warm_with_attr_jsonb_datetime.svg "")

**With & without datetime conversion on a group of 300K nodes and a cold database**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_cold_with_attr_jsonb_datetime.svg "")

**With & without datetime conversion on a group of 300K nodes and a warm database**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_warm_with_attr_jsonb_datetime.svg "")

**Comments:**
- Even if the database had an index on the attributes it was not used. Look at the query plans in the result files speed_tests_aiida_jsonb_small.txt & speed_tests_aiida_jsonb_small_no_datetime.txt.
- The graphs are nice, especially the one on the warm database. The only downside that I find is that the dataset is small and the differences are not so obvious, especially for 'Cell' & 'Kinds'.

**Source of the benchmarks**
The benchmarks that correspond to this section are #7 and #8 of the following notebook
https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/graphs.ipynb

Data come from the following files:
- speed_tests_aiida_jsonb_small.txt (JSONB - with datetime conversion)
- speed_tests_aiida_jsonb_small_no_datetime.txt (JSONB - without datetime conversion)

Databases used:
- aiida_dj_jsonb_original_seb_copy_m37_copy


Django EAV vs Django JSONB (with datetime conversion - one EAV query)
--------------------------------------------------------------------------------------------------------------
In this set of benchmarks we check the difference between AiiDA Django EAV and Django JSONB with datetime conversion on a cold and a warm database. It is worth noting that in these benchmarks of Django EAV we issue one query to retrieve all the node information and attributes/extras of the nodes of a group. This is different than the default behaviour of AiiDA when using querybuilder that will first get the node information and then for each node, it will fetch its attributes/extras issuing a different query.

The deserialization/reconstruction of the attribuetes is performed at the Python level.

**Django EAV vs Django JSONB on a group of 200K nodes and a cold database - one EAV query**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_cold_with_attr_ser_one_eav_query.svg "")

**Django EAV vs Django JSONB on a group of 200K nodes and a warm database - one EAV query**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_warm_with_attr_ser_one_eav_query.svg "")

**Comments:**
- The graph for the warm database seems interesting.
- Regarding the graph for the cold database: I am a bit surprised by the constant high SQL time for the EAV case. It should have been lower for 'Cell' and 'Kinds' than 'Sites' since the size of the attributes is lower (and the transferred data). It is also surprising that such a difference in SQL time is shown for the warm database case (same scripts used)

**Source of the benchmarks**
The benchmarks that correspond to this section are #9 and #10 of the following notebook
https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/graphs.ipynb

Data come from the following files:
- speed_tests_aiida_eav_small_ser_v3.txt (EAV)
- speed_tests_aiida_jsonb_small.txt (JSONB)

Databases used:
- aiida_dj_jsonb_original_seb_copy_m36_copy
- aiida_dj_jsonb_original_seb_copy_m37_copy


Django EAV vs Django JSONB (with datetime conversion - multiple EAV queries)
----------------------------------------------------------------------------------------------------------------------
In this set of benchmarks we check the difference between AiiDA Django EAV and Django JSONB with datetime conversion on a cold and a warm database. 

The main difference between these benchmarks and those found just above is that a single query is issued for every node to get the attributes of the node. This results in many small queries for the Django EAV and this is the current behaviour QueryBuilder's queries. In the Django EAV benchmark the total time reported includes the deserialization/reconstruction of the attribuetes at the Pyhton level.

Because of the high volume of attribute queries issues, SQL time in the Django EAV can not be reported.

**Django EAV vs Django JSONB on a group of 200K nodes and a cold database - Multiple EAV queries**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_cold_with_attr_ser.svg "")

**Django EAV vs Django JSONB on a group of 200K nodes and a warm database - Multiple EAV queries**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_warm_with_attr_ser.svg "")

**Comments:**
- These graphs are valuable for understanding how bad the current EAV implementation for querying the attributes is/performs.

**Source of the benchmarks**
The benchmarks that correspond to this section are #11 and #12 of the following notebook
https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/graphs.ipynb

Data come from the following files:
- speed_tests_aiida_eav_small_ser_v2.txt (EAV)
- speed_tests_aiida_jsonb_small.txt (JSONB)

Databases used:
- aiida_dj_jsonb_original_seb_copy_m36_copy
- aiida_dj_jsonb_original_seb_copy_m37_copy


Data transfer benchmarks
=====================

In this benchmark, we measure the size of the reply at the at SQL level (the size of the output of the query to txt) 
and the size of the reply at Python level. It is interesting to note that for the Django EAV, one query is issued, 
which returns all the attributes of all the interesting nodes (no deserialization is included)

**Django EAV vs Django JSONB data transfer - One EAV query**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_size.svg "")

**Comments:**
- Nice graphs to see the difference in size of the reply for Django EAV and Django JSONB but also how the size changes for different attribute selection.
- This graphs can be combined with speed benchmarks to have a better understanding of the reported timings.
- The difference of the reply size between SQL and Python is negligible and moreover, the SQL reported size is questionable (size of the reply of the SQL query in a txt)

**Source of the benchmarks**
The benchmark that correspond to this section is #15 of the following notebook
https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/graphs.ipynb

Data come from the following files:
- speed_tests_aiida_eav_small.txt (EAV)
- speed_tests_aiida_jsonb_small.txt (JSONB)

Databases used:
- aiida_dj_jsonb_original_seb_copy_m36_copy
- aiida_dj_jsonb_original_seb_copy_m37_copy



Storage space benchmarks
======================
In this benchmark we measure the space occupied on disk by a selection of XSF files (converted the provided CIFs from Leopold to XSFs), the size of a Django EAV database with only this information as well as the size of a Django JSONB database with these files loaded. For the Django JSONB, we have a version without GIN index (it seemed that it is the default for the version that I had - the migration was not adding a GIN index on the attributes & extras) and a version with GIN index on these collumns (I added it manually on attributes & extras).

The measurements were taked after a full vacuum of the corresponding databases.


**Django EAV vs Django JSONB vs disk space size for 100.000 data structures**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/space_saving_tests/1.x_v2/space_v1_10k_with_gin.svg "")


**Comments:**
- I believe that the graph above demonstrates well the benefits of using JSONB and gives a good understanding of the space used in the various approaches (raw files, EAV, JSONB, JSONB with indexes)

Comments on structure data usage:
- we use structure data because they are a good example. I.e. they are used in calculations (inputs & outputs) and they have various information that are stored as attributes (interesting for our backend comparison)
- the CIF files contain more information than what we store in AiiDA (database) for a structure data object
- an XSF file contains information much closer to what AiIDA stores (in its database) for a structure data object
- the initial idea was to use an XYZ file but the information stored in it was incomplete (maybe the cell coordinates were missing?)

Space comparison among:
- space on disk of the XSF files (convert the provided CIFs to XSFs)
- Django JSONB database size when loading the XSF files
- Django EAV database size when loading the XSF files

The XSFs will not be stored in the repository when I load them in AiiDA.

**Source of the benchmarks**
The benchmark that correspond to this section is #b2 of the following notebook
https://github.com/szoupanos/aiida_experiments/blob/master/space_saving_tests/1.x_v2/graphs.ipynb

Data come from the following files:
- space_saving_tests/1.x_v2/results.txt

Databases used:
- aiidadb_django_eav_space_10k
- aiidadb_django_jsonb_space_10k
- aiidadb_django_jsonb_space_10k_copy_gin

