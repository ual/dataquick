#!/bin/bash

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_dup_id_20150112'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

WITH sales_temp AS
	(SELECT 
		s.*,
		grp.dup_count,
		grp.price_count,
		grp.grp_id,
		ROW_NUMBER() OVER 
			(PARTITION BY grp.grp_id) AS grp_row,
		grp.rand
	FROM
		master.sales AS s
	LEFT OUTER JOIN
		(SELECT
			mm_fips_muni_code,
			sr_date_transfer,
			sr_property_id,
			COUNT(*) AS dup_count,
			COUNT (DISTINCT sr_val_transfer) AS price_count,
			ROW_NUMBER() OVER () AS grp_id,
			RANDOM() AS rand
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
			sr_property_id) AS grp
	ON
		grp.mm_fips_muni_code = s.mm_fips_muni_code
		AND grp.sr_date_transfer = s.sr_date_transfer
		AND grp.sr_property_id = s.sr_property_id
		AND s.sr_val_transfer > 0)
		
SELECT 
	*
FROM 
	sales_temp
WHERE
	dup_count > 1
	AND price_count > 1
	AND rand < 0.01
ORDER BY
	mm_fips_muni_code,
	sr_date_transfer
	
	
) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
