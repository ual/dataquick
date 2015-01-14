#!/bin/bash

# Alameda sales with duplicate doc numbers

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_doc_nbr_20141203'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT
	q.*,
	a.sa_sqft,
	(q.sr_val_transfer/a.sa_sqft) AS ucb_price_sqft
FROM
	(SELECT 
		*,
		lag(sr_doc_nbr_fmt) 
			OVER (ORDER BY sr_doc_nbr_fmt, sr_date_transfer, sr_unique_id) 
			AS lag_doc,
		lead(sr_doc_nbr_fmt) 
			OVER (ORDER BY sr_doc_nbr_fmt, sr_date_transfer, sr_unique_id) 
			AS lead_doc,
		lag(sr_date_transfer) 
			OVER (ORDER BY sr_doc_nbr_fmt, sr_date_transfer, sr_unique_id) 
			AS lag_dt,
		lead(sr_date_transfer) 
			OVER (ORDER BY sr_doc_nbr_fmt, sr_date_transfer, sr_unique_id) 
			AS lead_dt,
		lag(sr_arms_length_flag) 
			OVER (ORDER BY sr_doc_nbr_fmt, sr_date_transfer, sr_unique_id) 
			AS lag_armslen,
		lead(sr_arms_length_flag) 
			OVER (ORDER BY sr_doc_nbr_fmt, sr_date_transfer, sr_unique_id) 
			AS lead_armslen
	FROM
		master.sales
	WHERE
		mm_fips_muni_code = 1
	) AS q
INNER JOIN
	master.assessor AS a
ON
	a.sa_property_id = q.sr_property_id
WHERE
	((q.sr_doc_nbr_fmt = q.lag_doc
		AND q.sr_date_transfer = q.lag_dt
		AND q.sr_arms_length_flag = q.lag_armslen)
	OR (q.sr_doc_nbr_fmt = q.lead_doc
		AND q.sr_date_transfer = q.lead_dt
		AND q.sr_arms_length_flag = q.lead_armslen))
	AND q.sr_arms_length_flag = '1'
	AND a.sa_sqft > 0

) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
