#!/bin/bash

# Define the list of groups that we run the following tests
# 1354 | 20160903-021949
# 2566 | materials_cod_Alvarez_3D_layered
# 5018 | materials_icsd_3D_not_in_cod_vdW_vcrelaxed_structures
# 11744 | materials_cod_3D_up_to_6species_40atoms_pseudoOK
# 19836 | 20160223-135015
# 38529 | 20160216-163305
# 81548 | 20160223-203757
# 177557 | 20160225-234037
# 1124139 | 20160222-225236

group_list=("20160903-021949" "materials_cod_Alvarez_3D_layered" "materials_icsd_3D_not_in_cod_vdW_vcrelaxed_structures" "materials_cod_3D_up_to_6species_40atoms_pseudoOK" "20160223-135015" "20160216-163305" "20160223-203757" "20160225-234037" "20160222-225236")

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

