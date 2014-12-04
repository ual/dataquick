#!/bin/bash

# First apply leads and lags, then filter for matches

export PGPASSWORD=ucbdq
MY_PATH='/home/maurer/output'
cd $MY_PATH
FNAME='query_dup_sales_20141201'

psql -h tehran.ual.berkeley.edu -U dataquick_user dataquick -c "\copy (

SELECT
	q.*
FROM
	(SELECT 
		*,
		lag(sr_property_id) 
			OVER (ORDER BY sr_property_id, sr_date_transfer, sr_unique_id) 
			AS lag_id,
		lead(sr_property_id) 
			OVER (ORDER BY sr_property_id, sr_date_transfer, sr_unique_id) 
			AS lead_id,
		lag(sr_date_transfer) 
			OVER (ORDER BY sr_property_id, sr_date_transfer, sr_unique_id) 
			AS lag_dt,
		lead(sr_date_transfer) 
			OVER (ORDER BY sr_property_id, sr_date_transfer, sr_unique_id) 
			AS lead_dt,
		lag(sr_arms_length_flag) 
			OVER (ORDER BY sr_property_id, sr_date_transfer, sr_unique_id) 
			AS lag_armslen,
		lead(sr_arms_length_flag) 
			OVER (ORDER BY sr_property_id, sr_date_transfer, sr_unique_id) 
			AS lead_armslen
	FROM
		master.sales
	WHERE
		mm_fips_muni_code = 1
		AND sr_property_id > 0
	) AS q
WHERE
	((q.sr_property_id = q.lag_id
		AND q.sr_date_transfer = q.lag_dt
		AND q.sr_arms_length_flag = q.lag_armslen)
	OR (q.sr_property_id = q.lead_id
		AND q.sr_date_transfer = q.lead_dt
		AND q.sr_arms_length_flag = q.lead_armslen))
	AND q.sr_arms_length_flag = '1'

) TO $MY_PATH/$FNAME.csv WITH CSV HEADER;"

# zip $FNAME.zip $FNAME.csv 
# rm $FNAME.csv
