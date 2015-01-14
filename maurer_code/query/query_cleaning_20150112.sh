#!/bin/bash

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_cleaning_20150112'

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
		prop_grp.dup_count AS prop_dup_count,
		doc_grp.dup_count AS doc_dup_count,
		doc_grp.price_count AS doc_price_count,
		doc_grp.grp_sqft AS doc_grp_sqft
	FROM
		sales_base AS s

	LEFT OUTER JOIN
		(SELECT
			sr_date_transfer,
			sr_property_id,
			COUNT(*) AS dup_count
		FROM 
			sales_base
		GROUP BY
			sr_date_transfer,
			sr_property_id) AS prop_grp
	ON
		prop_grp.sr_date_transfer = s.sr_date_transfer
		AND prop_grp.sr_property_id = s.sr_property_id

	LEFT OUTER JOIN
		(SELECT
			mm_fips_muni_code,
			sr_date_transfer,
			sr_doc_nbr_fmt,
			COUNT(*) AS dup_count,
			COUNT (DISTINCT sr_val_transfer) AS price_count,
			SUM (sa_sqft) AS grp_sqft
		FROM 
			sales_base
		GROUP BY
			mm_fips_muni_code,
			sr_date_transfer,
			sr_doc_nbr_fmt) AS doc_grp
	ON
		doc_grp.mm_fips_muni_code = s.mm_fips_muni_code
		AND doc_grp.sr_date_transfer = s.sr_date_transfer
		AND doc_grp.sr_doc_nbr_fmt = s.sr_doc_nbr_fmt
)
		
SELECT 
	mm_fips_muni_code,
	(sr_date_transfer/10000) AS year,
	sa_census_tract,
	sr_property_id,
	(CASE 
		WHEN doc_dup_count > 1 AND doc_price_count = 1 
			THEN sr_val_transfer*doc_dup_count/doc_grp_sqft
		ELSE
			sr_val_transfer/sa_sqft
	END) AS val_sqft
FROM 
	sales_ext
WHERE
	prop_dup_count = 1
	AND SUBSTRING(use_code_std FROM 1 FOR 1) = 'R'
ORDER BY
	mm_fips_muni_code,
	sr_date_transfer
	
	
) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

zip $FNAME.zip $FNAME.csv 
rm $FNAME.csv
