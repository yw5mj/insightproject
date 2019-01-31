#! /bin/bash
alli='1 3 7 10 20 40 65 100 150'
for i in $alli; do
    echo -e "\n>> n_factors=$i"
    python validation_recommendor.py $i
done
	 
