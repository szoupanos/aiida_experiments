#!/bin/bash

# Define the list of groups that we run the following tests
group_list=("20160903-021949" "20160216-163305" "20160223-122131" "20160216-213117" "20160222-225236")
# group_list=('Verdi autogroup on 2017-02-17 12:50:31' "20160903-021949")
# declare -a group_list=('Verdi\ autogroup on 2017-02-17 12:50:31' "20160903-021949")
attr_list=("cell" "kinds" "sites")

# Run the Django tests for various group choices
for group in ${group_list[@]}; do
    echo "===> Running experiments for group choice" $group

	for attr_choice in ${attr_list[@]}; do
		echo "Running Django experiments for attribute filter choice" $attr_choice
		verdi -p mounet_dj run q_py_dj.py $group $attr_choice
		echo "==================="
	done
	
	echo "==================="

	for attr_choice in ${attr_list[@]}; do
		echo "Running SQLA experiments for attribute filter choice" $attr_choice
		verdi -p mounet_sqla run q_py_sqla.py $group $attr_choice
		echo "==================="
	done
	
	echo "+++++++++++++++++++"
	echo "+++++++++++++++++++"
done

# echo "================================================"
# echo "================================================"
# 
# # Run the SQLA tests for various group choices
# for group in ${group_list[@]}; do
#     echo "Running SQLA experiments for group choice" $group
#     
# 	for attr_choice in ${attr_list[@]}; do
# 		echo "Running SQLA experiments for attribute filter choice" $attr_choice
# 		verdi -p mounet_sqla run q_py_sqla.py $group $attr_choice
# 		echo "================================================"
# 	done
# done

