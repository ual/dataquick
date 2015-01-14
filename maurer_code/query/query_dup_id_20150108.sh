#!/bin/bash

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_dup_id_20150108'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT 
	*
FROM
	master.sales AS s
LEFT OUTER JOIN
	(SELECT
		mm_fips_muni_code,
		sr_date_transfer,
		sr_property_id,
		count(*) AS cnt,
		random() AS rnd
	FROM 
		master.sales
	WHERE
		mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
		AND (sr_date_transfer/10000) >= 1988
		AND sr_val_transfer > 0
		AND sr_property_id > 0
	GROUP BY
		mm_fips_muni_code,
		sr_date_transfer,
		sr_property_id) AS grp_a
ON
	grp_a.mm_fips_muni_code = s.mm_fips_muni_code
	AND grp_a.sr_date_transfer = s.sr_date_transfer
	AND grp_a.sr_property_id = s.sr_property_id
	
WHERE
	grp_a.cnt > 1 
	AND grp_a.rnd < 0.01
	
ORDER BY
	s.mm_fips_muni_code,
	s.sr_date_transfer
	
) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
