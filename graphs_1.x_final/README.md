# aiida_benchmarks using AiiDA v1 - Final graphs

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
- They are also good to show that the speed difference becomes significant when a lot of attributes need to be de-serialized E.g. 'Sites'
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

