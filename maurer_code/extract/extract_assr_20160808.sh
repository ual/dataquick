#!/bin/bash

# This script generates CSV extracts of Assessor data from Postgres
# Generates one file with the entire table

source config.sh  # read database connection settings

FNAME='ARB_ASSR_CALIFORNIA'
psql -h $HOSTNAME -U $USERNAME -d $DBNAME -c "\copy (SELECT * FROM master.assessor ORDER BY mm_fips_muni_code, sa_property_id) TO $OUTPATH/$FNAME.csv WITH CSV HEADER;"

cd $OUTPATH
zip $FNAME.csv.zip $FNAME.csv 
# rm $FNAME.csv
