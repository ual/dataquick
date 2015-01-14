#!/bin/bash

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_nonarms_nonzero_20141216'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT
	*
FROM
	master.sales
WHERE
	mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
	AND (sr_date_transfer/10000) >= 1988
	AND sr_arms_length_flag <> '1'
	AND sr_val_transfer > 0
	AND random() < 0.01
ORDER BY 
	mm_fips_muni_code,
	sr_date_transfer

) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
