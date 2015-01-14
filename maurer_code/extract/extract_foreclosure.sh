#!/bin/bash

# This script generates a CSV extract of Foreclosure data from Postgres
# Attaches some fields from the current assessor table:
# - ucb_geo_id, sa_x_coord, sa_y_coord, sa_geo_qlty_code

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/Dataquick/Foreclosure'
cd $MY_PATH
FNAME='ARB_FORE_BAY_AREA_v2'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (SELECT f.*, a.ucb_geo_id, a.sa_x_coord, a.sa_y_coord, a.sa_geo_qlty_code FROM master.foreclosure AS f LEFT OUTER JOIN master.assessor AS a ON a.sa_property_id=f.sa_property_id WHERE f.mm_fips_muni_code in (1,13,41,55,75,81,85,95,97)) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

zip $FNAME.zip $FNAME.csv 
rm $FNAME.csv
