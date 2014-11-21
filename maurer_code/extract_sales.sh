#!/bin/bash

# This script generates CSV extracts of Sales data from Postgres,
# merged with geographic fields from the Current Assessor table
# (generates one file per bay area county)

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/Dataquick/Sales/County_extracts_v2'
cd $MY_PATH

CTY_CD=(1 13 41 55 75 81 85 95 97)
CTY_NM=('ALAMEDA' 'CONTRA_COSTA' 'MARIN' 'NAPA' 'SAN_FRANCISCO' 'SAN_MATEO' 'SANTA_CLARA' 'SOLANO' 'SONOMA')

for i in `seq 0 8`;
do
	FNAME='ARB_HIST_'${CTY_NM[$i]}'_v2'
	psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (SELECT s.*, a.ucb_geo_id, a.sa_x_coord, a.sa_y_coord, a.sa_geo_qlty_code FROM master.sales AS s LEFT OUTER JOIN master.assessor AS a ON a.sa_property_id=s.sr_property_id WHERE s.mm_fips_muni_code=${CTY_CD[$i]}) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"
	zip $FNAME.zip $FNAME.csv 
	rm $FNAME.csv
done
