#!/usr/bin/env bash

list_file_modi=$(git ls-files -m |grep .py)
fix_str=""
br_ln="########################### AutoFlake ###########################"

for file in $list_file_modi
do
	echo Format file "$file"
	echo "########################### AutoFlake ###########################"
	tmp=$(autoflake --remove-all-unused-imports --recursive --remove-unused-variables --exclude=__init__.py --recursive "$file")
	if [ -n "${tmp}" ];then
		fix_str="${fix_str}"$'\n\n'"${br_ln}"$'\n'"${tmp}"
	fi

	echo "###########################   Isort   ###########################"
	tmp=$(isort "$file")

	echo "###########################   Black   ###########################"
	tmp=$(black "$file")

	# echo "###########################   Pylint  ###########################"
	# pylint "$file"
	echo
	echo
done



list_file_untracked=$(git ls-files --others --exclude-standard |grep .py)

for file in $list_file_untracked
do
	echo Format file "$file"
	echo "########################### AutoFlake ###########################"
	tmp=$(autoflake --remove-all-unused-imports --recursive --remove-unused-variables --exclude=__init__.py --recursive "$file")
	if [ -n "${tmp}" ];then

		fix_str="${fix_str}"$'\n\n\n'"${br_ln}"$'\n'"${tmp}"
	fi

	echo "###########################   Isort   ###########################"
	tmp=$(isort "$file")

	echo "###########################   Black   ###########################"
	tmp=$(black "$file")

	# echo "###########################   Pylint  ###########################"
	#pylint "$file"

	echo
	echo
done

if [ -n "${fix_str}" ];then
	echo "##################################################################"
	echo "#                           Should Fix                           #"
	echo "##################################################################"
	echo "$fix_str"
fi
