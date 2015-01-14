#!/bin/bash

# This script generates CSV extracts of Assessor History data from Postgres
# Generates one file per bay area county per year from 2004 to 2014

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/Dataquick/Assessor_History/County_extracts'
cd $MY_PATH

CTY_CD=(1 13 41 55 75 81 85 95 97)
CTY_NM=('ALAMEDA' 'CONTRA_COSTA' 'MARIN' 'NAPA' 'SAN_FRANCISCO' 'SAN_MATEO' 'SANTA_CLARA' 'SOLANO' 'SONOMA')

for y in `seq 2004 2014`;
do 
	for i in `seq 0 8`;
	do
		FNAME='AH_'$y'_'${CTY_NM[$i]}
		psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (SELECT * FROM master.ahist WHERE ah_history_yr=$y AND mm_fips_muni_code=${CTY_CD[$i]} ORDER BY sa_property_id, ah_history_yr_version) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"
		zip $FNAME.zip $FNAME.csv 
		rm $FNAME.csv
	done
done