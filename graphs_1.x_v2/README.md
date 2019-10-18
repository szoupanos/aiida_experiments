# aiida_benchmarks using AiiDA v1

There are two different kinds of benchmarks that have been peformed.
Benchmarks to measure speed gains and benchmarks to measure space gains.
All the benchmarks found below are based on the Django EAV version which is just before and after the conversion to AiiDA Django JSONB.
This corresponds to commit 1956cfad8 for AiiDA Django EAV and a7c3ac4e4 of aiida/django_jsonb branch.


Speed benchmarks
================
These benchmarks were performed using the AiiDA Django JSONB and AiiDA Django EAV using an extension of Mounet's database provided by Davide. The benchmarks were peformed on the full database (around 7 milion nodes) as well as on subsets of the database (on 200K nodes and 300K nodes). The results using a cold database (database after restart with clean cache) and a warm database (launching the same query for a second time - the database cache containes the previous results) are presented.

All the benchmarks were run once (so there might be a few descrepancies in the numbers - especially for timings that could be less than a second).


Django JSONB -  comparison on the benefits of a GIN index and datetime deactivation (full database)
----------------------------------------------------------------------------------------------------------------------------------------------------
In this set of benchmarks, we check the benefints of using a GIN index in JSONB related queries as well as well the benefits from using the datetime.

**GIN and datetime benefits on a cold database - Full database benchmark**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_cold_gin_comparison.svg "")

**GIN and datetime benefits on a warm database - Full database benchmark**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_warm_gin_comparison.svg "")

**Comments:**
- Overall the graphs seem normal. 
- The performance gains of the GIN index can be seen mainly in the benchmarks of 'Cells' and 'Kinds' (total execution time). 
- The performance gains are also obvious at the SQL time of the graphs for all kinds of attributes 'Cells', 'Kinds' and 'Sites'.
- The usage of GIN index doesn't seem to have an effect on the total execution time for 'Sites'.
- What I can not explain is why the total execution time with GIN and datetime conversion is higher than the total execution time without GIN and datetime conversion. If we remove the SQL time from the total execution time of these graphs (JSONB with GIN, with DT and JSONB no GIN with DT), these results become even more inexplicable. In a few words, it seems that the datetime conversion takes more time for the same nodes when a GIN index is not used!! What is even worse is that this doesn't seem to be a mistake in the measurements since this difference & pattern appears in the benchmarks of this sectio (#1 & #2) but also at the measurements of the following sections. Any ideas?

**Notes on the benchmarks**
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
In this set of benchmarks, we check the benefints of using a GIN index in JSONB related queries as well as well the benefits from using the datetime and we make the direct comparison with the performance of the Django EAV version of AiiDA.


=========== UNTIL HERE ===========




Django JSONB (with and without datetime conversion)
---------------------------------------------------------------------------------
In this set of benchmarks we check the overhead of the datetime conversion for the Django JSONB version with cold and warm database

**With & without datetime conversion on a group of 200K nodes and a cold database**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_cold_with_attr_jsonb_datetime.svg "")


**With & without datetime conversion on a group of 200K nodes and a warm database**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_warm_with_attr_jsonb_datetime.svg "")

Input data can be found at the following files:
- speed_tests_aiida_jsonb_small.txt (JSONB - with datetime conversion)
- speed_tests_aiida_jsonb_small_no_datetime.txt (JSONB - without datetime conversion)


Django EAV vs Django JSONB (with datetime conversion - one EAV query)
--------------------------------------------------------------------------------------------------------------
In this set of benchmarks we check the difference between AiiDA Django EAV and Django JSONB with datetime conversion on a cold and a warm database. It is worth noting that in these benchmarks of Django EAV we issue one query to retrieve all the node information and attributes/extras of the nodes of a group. This is different than the default behaviour of AiiDA when using querybuilder that will first get the node information and then for each node, it will fetch its attributes/extras issueing a different query.

The serialization is performed at the Python level

**Django EAV vs Django JSONB on a group of 200K nodes and a cold database - one EAV query**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_cold_with_attr_jsonb_datetime.svg "")

**Django EAV vs Django JSONB on a group of 200K nodes and a warm database - one EAV query**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_warm_with_attr_ser_one_eav_query.svg "")

Input data can be found at the following files:
- speed_tests_aiida_eav_small_ser_v3.txt (EAV)
- speed_tests_aiida_jsonb_small.txt (JSONB)

Django EAV vs Django JSONB (with datetime conversion - multiple EAV queries)
----------------------------------------------------------------------------------------------------------------------
In this set of benchmarks we check the difference between AiiDA Django EAV and Django JSONB with datetime conversion on a cold and a warm database. 

The main difference between these benchmarks and those found just above is that a single query is issued for every node to get the attributes of the node. This results in many small queries for the Django EAV and this is the current behaviour QueryBuilder's queries.

Because of the high volume of attribute queries issues, SQL time in the Django EAV can not be reported.

**Django EAV vs Django JSONB on a group of 200K nodes and a cold database - Multiple EAV queries **
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_cold_with_attr_ser.svg "")

**Django EAV vs Django JSONB on a group of 200K nodes and a warm database - Multiple EAV queries **
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_300_warm_with_attr_ser.svg "")

Input data can be found at the following files:
- speed_tests_aiida_jsonb_small.txt (JSONB)
- to be found for the EAV

Space benchmarks
================
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

**Django EAV vs Django JSONB vs disk space size for 100.000 data structures**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/space_saving_tests/1.x_v2/space_v1_10k.svg "")


Notes for Spyros
==============
What remains to be added - mentioned
    - I should show the size of the final result in the speed benchmarks
    - I should give an intution of the GIN index speed increase
