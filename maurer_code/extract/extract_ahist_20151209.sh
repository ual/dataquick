#!/bin/bash

# This script generates CSV extracts of Assessor History data from Postgres
# Generates one file per county per year from 2004 to 2014

source config.sh  # read database connection settings

CTY_CD=(37 73)  # FIPS county codes, for database query
CTY_NM=('LOS_ANGELES' 'SAN_DIEGO')  # county labels, for filenames

for y in `seq 2004 2014`;
do 
	for i in `seq 0 1`;
	do
		FNAME='AH_'$y'_'${CTY_NM[$i]}
		psql -h $HOSTNAME -U $USERNAME -d $DBNAME -c "\copy (SELECT * FROM master.ahist WHERE ah_history_yr=$y AND mm_fips_muni_code=${CTY_CD[$i]} ORDER BY sa_property_id, ah_history_yr_version) TO $OUTPATH/$FNAME.csv WITH CSV HEADER;"
		cd $OUTPATH
		zip $FNAME.zip $FNAME.csv 
		rm $FNAME.csv
	done
done