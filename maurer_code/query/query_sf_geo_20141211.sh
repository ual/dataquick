#!/bin/bash

# SF use codes with x,y coordinates

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_sf_geo_20141211'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT
	substring(use_code_std from 1 for 1) AS use_code,
	sa_x_coord,
	sa_y_coord,
	sa_geo_qlty_code
FROM
	master.assessor
WHERE
	mm_fips_muni_code = 75

) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
