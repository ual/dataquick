#!/bin/bash

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_sales_20141117'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (SELECT *  FROM master.sales AS s INNER JOIN master.assessor AS a ON a.sa_property_id = s.sr_property_id WHERE a.ucb_geo_id in ('06001420400', '06001981900', '06041122000', '06075033203', '06075980401', '06081984300', '06085504700', '06085505008', '06085511609', '06095252802', '06095253000', '06095980000')) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
