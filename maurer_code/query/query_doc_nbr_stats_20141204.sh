#!/bin/bash

# Alameda sales with duplicate doc numbers

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_doc_nbr_stats_20141204'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT
	mm_fips_muni_code,
	sr_doc_nbr_fmt
FROM 
	master.sales
WHERE
	mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
	AND (sr_date_transfer / 10000) = 2010
	AND sr_arms_length_flag = '1'
ORDER BY
	mm_fips_muni_code,
	sr_date_transfer,
	sr_doc_nbr_fmt
	
) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
