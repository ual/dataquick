#!/bin/bash

# This script generates CSV extracts of cleaned sales data from Postgres,
# (generates one file per bay area county)

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/Dataquick/Sales/County_extracts_v3'
cd $MY_PATH

CTY_CD=(1 13 41 55 75 81 85 95 97)
CTY_NM=('ALAMEDA' 'CONTRA_COSTA' 'MARIN' 'NAPA' 'SAN_FRANCISCO' 'SAN_MATEO' 'SANTA_CLARA' 'SOLANO' 'SONOMA')

for i in `seq 0 8`;
do
	FNAME='ARB_HIST_'${CTY_NM[$i]}'_v3'
	psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (SELECT * FROM master.sales_clean WHERE mm_fips_muni_code=${CTY_CD[$i]}) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"
	zip $FNAME.zip $FNAME.csv 
	rm $FNAME.csv
done
