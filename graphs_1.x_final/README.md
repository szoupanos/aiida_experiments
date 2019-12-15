# aiida_benchmarks using AiiDA v1 - Final graphs

In this report we summarise the EAV - JSONB comparison benchmarks that will be used for the AiiDA paper. In the first section we do a speed comparison of the two approaches and in the second section we do a space savings comparison.

## Django JSONB -  speed comparison on the benefits of JSONB (no GIN index and without datetime vs Django EAV (partial database)

This section focuses on speed comparisons of the two approaches for storing data.
In the first sub-section we present the graphs for 200k and 300k nodes that were run only once. In the second sub-section we focus on the 300k node set graphs and we have re-run the benchmarks 3 times for more accurate speed results.

### 200k & 300k node Django EAV - JSONB speed comparison - One repetition

This is the final set of speed benchmarks that we have decided to keep from a bigger list of benchmarks that can be found at the following page: [Speed & space benchmarks using AiiDA 1.0](https://github.com/szoupanos/aiida_experiments/tree/master/graphs_1.x_v2)

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
- [speed_tests_aiida_gin_test_eav.txt](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/results/speed_tests_aiida_gin_test_eav.txt)
    - the total time reported in the graphs is the addition of query time 
      and serialization time. The SQL time is the time reported by PostgreSQL
- [speed_tests_aiida_gin_test_jsonb_without_gin_no_datetime.txt](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_v2/results/speed_tests_aiida_gin_test_jsonb_without_gin_no_datetime.txt)


 Databases used:
- aiida_dj_jsonb_original_seb_copy_m37_copy_200_no_gin
- aiida_dj_jsonb_original_seb_copy_m36_copy_200_gin
- aiida_dj_jsonb_original_seb_copy_m37_copy_300_no_gin
- aiida_dj_jsonb_original_seb_copy_m36_copy_300_gin

### 300k node Django EAV - JSONB speed comparison - Three repetitions

In this sub-section we have run the Django EAV - JSONB speed comparison shown above for the dataset of 300k nodes and it was repeated 3 times.

**JSONB (without GIN and datetime) vs EAV with datetime - 300k node database - Cold DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/attr_queries_300_cold_eav_json_comparison_3times.svg "")

**JSONB (without GIN and datetime) vs EAV with datetime - 300k node database - Warm DB**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/attr_queries_300_warm_eav_json_comparison_3times.svg "")

**Source of the benchmarks**
https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/graphs_isolated_specific_measures.ipynb

Data come from the following files:
- [speed_tests_aiida_gin_test_eav.txt](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/results/speed_tests_aiida_gin_test_eav.txt)
    - the total time reported in the graphs is the addition of query time 
      and serialization time. The SQL time is the time reported by PostgreSQL
- [speed_tests_aiida_gin_test_jsonb_without_gin_no_datetime.txt](https://github.com/szoupanos/aiida_experiments/blob/master/speedup_experiments/1.x_final/results/speed_tests_aiida_gin_test_jsonb_without_gin_no_datetime.txt)


 Databases used:
- aiida_dj_jsonb_original_seb_copy_m37_copy_200_no_gin
- aiida_dj_jsonb_original_seb_copy_m36_copy_200_gin
- aiida_dj_jsonb_original_seb_copy_m37_copy_300_no_gin
- aiida_dj_jsonb_original_seb_copy_m36_copy_300_gin

## Django EAV vs Django JSONB -  space comparison (partial database)

The graph of this section is a simplified version of space comparison graph (last one, after full vacuum of the corresponding databases) found at the following page: [Speed & space benchmarks using AiiDA 1.0](https://github.com/szoupanos/aiida_experiments/tree/master/graphs_1.x_v2)

which comes from the following notebook: 
[Space comparison notebook](https://github.com/szoupanos/aiida_experiments/blob/master/space_saving_tests/1.x_v2/graphs.ipynb)

And data can be found at the following files:
- [space_saving_tests/1.x_v2/results.txt](https://github.com/szoupanos/aiida_experiments/blob/master/space_saving_tests/1.x_v2/results.txt)

Using the data of the above mentioned results file, we construct the following graph (measurements after full vacumm of the databases).

**Django EAV vs Django JSONB vs disk space size for 100.000 data structures**
![alt text](https://github.com/szoupanos/aiida_experiments/blob/master/space_saving_tests/1.x_final/space_v1_10k_eav_vs_jsonb_without_gin_final.svg "")

The graph was constructed at the following notebook file
[Space comparison notebook](https://github.com/szoupanos/aiida_experiments/blob/master/space_saving_tests/1.x_final/graphs.ipynb)

Information about the size of the indexes and the tables of the databases used in the above graphs.

aiidadb_django_jsonb_space_10k
|   oid   | table_schema |       table_name       | row_estimate | total_bytes | index_bytes | toast_bytes | table_bytes |  total  |  index  |   toast    |   table    |
|---------|--------------|------------------------|--------------|-------------|-------------|-------------|-------------|---------|---------|------------|------------|
| 2929631 | public       | django_content_type    |           12 |       40960 |       32768 |             |        8192 | 40 kB   | 32 kB   |            | 8192 bytes |
| 2929620 | public       | django_migrations      |           47 |       32768 |       16384 |        8192 |        8192 | 32 kB   | 16 kB   | 8192 bytes | 8192 bytes |
| 2929659 | public       | auth_group_permissions |            0 |       32768 |       32768 |             |           0 | 32 kB   | 32 kB   |            | 0 bytes    |
| 2929811 | public       | db_dblog               |            0 |       65536 |       57344 |        8192 |           0 | 64 kB   | 56 kB   | 8192 bytes | 0 bytes    |
| 2929841 | public       | db_dbsetting           |            1 |       65536 |       49152 |        8192 |        8192 | 64 kB   | 48 kB   | 8192 bytes | 8192 bytes |
| 2929641 | public       | auth_permission        |           36 |       57344 |       49152 |             |        8192 | 56 kB   | 48 kB   |            | 8192 bytes |
| 2929795 | public       | db_dblink              |            0 |       65536 |       57344 |        8192 |           0 | 64 kB   | 56 kB   | 8192 bytes | 0 bytes    |
| 2929784 | public       | db_dbgroup             |            1 |      147456 |      131072 |        8192 |        8192 | 144 kB  | 128 kB  | 8192 bytes | 8192 bytes |
| 2929911 | public       | db_dbgroup_dbnodes     |        10000 |     1433600 |      983040 |             |      450560 | 1400 kB | 960 kB  |            | 440 kB     |
| 2929730 | public       | db_dbauthinfo          |            0 |       40960 |       32768 |        8192 |           0 | 40 kB   | 32 kB   | 8192 bytes | 0 bytes    |
| 2929749 | public       | db_dbcomment           |            0 |       40960 |       32768 |        8192 |           0 | 40 kB   | 32 kB   | 8192 bytes | 0 bytes    |
| 2929760 | public       | db_dbcomputer          |            0 |       40960 |       32768 |        8192 |           0 | 40 kB   | 32 kB   | 8192 bytes | 0 bytes    |
| 2929690 | public       | db_dbuser              |            1 |       65536 |       49152 |        8192 |        8192 | 64 kB   | 48 kB   | 8192 bytes | 8192 bytes |
| 2929822 | public       | db_dbnode              |        10000 |   447414272 |     3579904 |   441614336 |     2220032 | 427 MB  | 3496 kB | 421 MB     | 2168 kB    |
| 2929649 | public       | auth_group             |            0 |       24576 |       24576 |             |           0 | 24 kB   | 24 kB   |            | 0 bytes    |