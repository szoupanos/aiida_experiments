# aiida_benchmarks using AiiDA v1 - Final graphs

Django JSONB -  comparison on the benefits of JSONB (no GIN index and without datetime vs Django EAV (partial database)
----------------------------------------------------------------------------------------------------------------------------------------------------

This is the final set of speed benchmarks that we have decided to keep from a bigger list of benchmarks that can be found at the following page:

[Speed & space benchmarks using AiiDA 1.0](https://github.com/szoupanos/aiida_experiments/tree/master/graphs_1.x_v2)

The main characteristic of the benchmarks of this section is that the databases used contain only the nodes that interest us (200k / 300k). Nodes that we consider interesting.


**JSONB (without GIN and datetime) vs EAV with datetime - 200k node database - Cold DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/attr_queries_200_cold_eav_json_comparison.svg "")

**JSONB (without GIN and datetime) vs EAV with datetime - 200k node database - Warm DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/attr_queries_200_warm_eav_json_comparison.svg "")

**JSONB (without GIN and datetime) vs EAV with datetime - 300k node database - Cold DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/attr_queries_300_cold_eav_json_comparison.svg "")

**JSONB (without GIN and datetime) vs EAV with datetime - 300k node database - Warm DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/attr_queries_300_warm_eav_json_comparison.svg "")

**Comments:**
- The benchmarks to create the graphs mentioned above were run only once.

**Source of the benchmarks**
https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/graphs_isolated_specific_measures.ipynb

Data come from the following files:
- speed_tests_aiida_gin_test_eav.txt
    - the total time reported in the graphs is the addition of query time 
      and serialization time. The SQL time is the time reported by PostgreSQL
- speed_tests_aiida_gin_test_jsonb_without_gin_no_datetime.txt

 Databases used (to be verified):
- aiida_dj_jsonb_original_seb_copy_m37_copy_200_gin
- aiida_dj_jsonb_original_seb_copy_m37_copy_200_no_gin
- aiida_dj_jsonb_original_seb_copy_m36_copy_200_gin
- aiida_dj_jsonb_original_seb_copy_m37_copy_300_gin
- aiida_dj_jsonb_original_seb_copy_m37_copy_300_no_gin
- aiida_dj_jsonb_original_seb_copy_m36_copy_300_gin

