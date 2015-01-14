#!/bin/bash

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_dup_id_20150112b'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

WITH sales_base AS (
	SELECT
		s.*,
		a.sa_census_tract,
		a.sa_sqft,
		a.use_code_std
	FROM
		master.sales AS s
	INNER JOIN
		master.assessor AS a
	ON
		a.sa_property_id = s.sr_property_id
	WHERE
		s.sr_property_id IS NOT null
		AND s.sr_property_id > 0
		AND s.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
		AND (s.sr_date_transfer/10000) >= 1988
		AND s.sr_arms_length_flag = '1'
		AND s.sr_val_transfer > 0
		AND a.sa_census_tract <> ''
		AND a.sa_sqft IS NOT null
		AND a.sa_sqft > 0
		AND a.use_code_std <> ''
		AND (s.sr_tran_type = 'R'
			OR s.sr_tran_type = 'S')
		AND s.sr_buyer NOT ILIKE '% trust%'
		AND s.sr_seller NOT ILIKE '% trust%'
		AND s.sr_buyer NOT ILIKE '%city%'
		AND s.sr_seller NOT ILIKE '%city%'
		AND s.sr_buyer NOT ILIKE '%county%'
		AND s.sr_seller NOT ILIKE '%county%'
		AND s.sr_buyer NOT ILIKE '%agency%'
		AND s.sr_seller NOT ILIKE '%agency%'
		AND s.sr_buyer NOT ILIKE '%redevelopment%'
		AND s.sr_seller NOT ILIKE '%redevelopment%'
),

sales_ext AS (
	SELECT 
		s.*,
		grp.dup_count,
		grp.price_count,
		grp.price_sum,
		grp.grp_id,
		ROW_NUMBER() OVER 
			(PARTITION BY grp.grp_id) AS grp_row,
		grp.grp_rand
	FROM
		sales_base AS s
	LEFT OUTER JOIN
		(SELECT
			mm_fips_muni_code,
			sr_date_transfer,
			sr_property_id,
			COUNT(*) AS dup_count,
			COUNT (DISTINCT sr_val_transfer) AS price_count,
			SUM (sr_val_transfer) AS price_sum,
			ROW_NUMBER() OVER () AS grp_id,
			RANDOM() AS grp_rand
		FROM 
			sales_base
		GROUP BY
			mm_fips_muni_code,
			sr_date_transfer,
			sr_property_id) AS grp
	ON
		grp.mm_fips_muni_code = s.mm_fips_muni_code
		AND grp.sr_date_transfer = s.sr_date_transfer
		AND grp.sr_property_id = s.sr_property_id
)
		
SELECT 
	*
FROM 
	sales_ext
WHERE
	dup_count > 1
	AND grp_rand < 0.01
ORDER BY
	mm_fips_muni_code,
	sr_date_transfer
	
	
) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
