#!/bin/bash

# Alameda sales with duplicate doc numbers

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_doc_nbr_20141204'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT
	s.*,
	c.ucb_dup_count,
	a.sa_sqft,
	(CASE
		WHEN a.sa_sqft > 0 
			THEN (s.sr_val_transfer/a.sa_sqft)
		ELSE NULL
	END) AS ucb_price_sqft
FROM
	master.sales AS s
LEFT OUTER JOIN
	master.assessor AS a
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
	s.mm_fips_muni_code = 1
	AND c.ucb_dup_count > 1

) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
