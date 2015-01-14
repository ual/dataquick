#!/bin/bash

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_sales_20141205'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT
	s.mm_fips_muni_code,
	(s.sr_date_transfer/10000) AS year,
	count(*) AS all_sales,
	count
		(CASE WHEN 
			(s.sr_arms_length_flag = '1') 
		THEN 1 ELSE NULL END) AS and_arms_length,
	count
		(CASE WHEN 
			(s.sr_arms_length_flag = '1' 
			AND ah.use_code_std <> '')
		THEN 1 ELSE NULL END) AS and_known_usecode,
	count
		(CASE WHEN 
			(s.sr_arms_length_flag = '1' 
			AND substring(ah.use_code_std from 1 for 1) = 'R')
		THEN 1 ELSE NULL END) AS and_residential,
	count
		(CASE WHEN 
			(s.sr_arms_length_flag = '1' 
			AND ah.use_code_std IN ('RSFR','RMOB'))
		THEN 1 ELSE NULL END) AS and_single_family,
	count
		(CASE WHEN 
			(s.sr_arms_length_flag = '1' 
			AND ah.use_code_std IN ('RSFR','RMOB')
			AND a.ucb_geo_id <> '')
		THEN 1 ELSE NULL END) AS and_known_tract,
	count
		(CASE WHEN 
			(s.sr_arms_length_flag = '1' 
			AND ah.use_code_std IN ('RSFR','RMOB')
			AND a.ucb_geo_id <> ''
			AND ah.sa_sqft > 0
			AND s.sr_val_transfer > 0)
		THEN 1 ELSE NULL END) AS and_known_price_sqft,
	count
		(CASE WHEN 
			(s.sr_arms_length_flag = '1' 
			AND ah.use_code_std IN ('RSFR','RMOB')
			AND a.ucb_geo_id <> ''
			AND ah.sa_sqft > 0
			AND s.sr_val_transfer > 0
			AND c.ucb_dup_count = 1)
		THEN 1 ELSE NULL END) AS and_unique_doc_num
FROM 
	master.sales AS s
LEFT OUTER JOIN
	master.ahist AS ah
ON
	ah.sa_property_id = s.sr_property_id
	AND ah.ah_history_yr = (s.sr_date_transfer/10000 + 1)
	AND ah.ah_history_yr_version = 1	
LEFT OUTER JOIN
	master.assessor as a
ON
	a.sa_property_id = s.sr_property_id
LEFT OUTER JOIN
	(SELECT
		mm_fips_muni_code,
		sr_date_transfer,
		sr_doc_nbr_fmt,
		count(*) AS ucb_dup_count
	FROM
		master.sales
	WHERE 
		mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
		AND sr_arms_length_flag = '1'
	GROUP BY
		mm_fips_muni_code,
		sr_date_transfer,
		sr_doc_nbr_fmt) AS c
ON
	c.mm_fips_muni_code = s.mm_fips_muni_code
	AND c.sr_date_transfer = s.sr_date_transfer
	AND c.sr_doc_nbr_fmt = s.sr_doc_nbr_fmt
WHERE
	s.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
	AND (s.sr_date_transfer/10000) >= 2007
	AND (s.sr_date_transfer/10000) <= 2012
GROUP BY
	s.mm_fips_muni_code,
	(s.sr_date_transfer/10000)
ORDER BY 
	s.mm_fips_muni_code,
	(s.sr_date_transfer/10000)


) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
