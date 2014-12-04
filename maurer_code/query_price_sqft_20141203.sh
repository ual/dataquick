#!/bin/bash

# Alameda sales with duplicate doc numbers

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_price_sqft_20141203'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT
	(s.sr_val_transfer/a.sa_sqft) AS ucb_price_sqft
FROM
	master.sales AS s
INNER JOIN
	master.assessor AS a
ON
	a.sa_property_id = s.sr_property_id
WHERE
	s.mm_fips_muni_code = 1
	AND s.sr_arms_length_flag = '1'
	AND a.sa_sqft > 0
	AND s.sr_val_transfer > 0

) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
