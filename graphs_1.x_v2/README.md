# aiida_benchmarks using AiiDA v1

There are two different kinds of benchmarks that have been peformed.
Benchmarks to measure speed gains and benchmarks to measure space gains.
All the benchmarks found below are based on the Django EAV version which is just before and after the conversion to AiiDA Django JSONB.
This correspond to commit 1956cfad8 for AiiDA Django EAV and a7c3ac4e4 of aiida/django_jsonb branch.


Speed benchmarks
================
These are benchmarks performed using the AiiDA Django JSONB and AiiDA Django EAV using an extension of Mounet's database provided by Davide. They were performed using a group of 200.000 nodes. The results using a cold database (database after restart with clean cache) and a warm database (launching the same query for a second time - the database cached contained the previous results).


Django JSONB (with and without datetime conversion)
---------------------------------------------------------------------------------
In this set of benchmarks we check the overhead of the datetime conversion for the Django JSONB version with cold and warm database

**With & without datetime conversion on a group of 200K nodes and a cold database**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_cold_with_attr_jsonb_datetime.svg "")


**With & without datetime conversion on a group of 200K nodes and a warm database**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/graphs/attr_queries_200_warm_with_attr_jsonb_datetime.svg "")

Data come from the following files:
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

Data come from the following files:
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

Data come from the following files:
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
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/space_saving_tests/1.x_v2/space_v1_10k.svg"")


Notes for Spyros
==============
What remains to be added - mentioned
    - I should show the size of the final result in the speed benchmarks
    - I should give an intution of the GIN index speed increase
