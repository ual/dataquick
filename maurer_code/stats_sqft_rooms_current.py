# This script tabulates square footage, rooms, bedrooms
# Takes about 3 min to run on server

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t0 = time.time()
cur.execute(""" SELECT ucb_geo_id, 
					sa_sqft, 
					sa_nbr_rms, 
					sa_nbr_bedrms,
					(sa_date_transfer/10000) AS yr
				FROM master.assessor 
				WHERE mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
					AND substring(use_code_std from 1 for 1) = 'R'; """)

out = cur.fetchall()
print int(time.time()-t0), 'sec. for postgres'

t0 = time.time()
geo = np.array([r[0] for r in out])
sqft = np.array([r[1] for r in out])
rms = np.array([r[2] for r in out])
bedrms = np.array([r[3] for r in out])
yr = np.array([r[4] for r in out])

geo_list = np.unique(geo).tolist()
geo_fltr = {g: (geo==g) for g in geo_list}

sqft_nonzero = (sqft > 0)
rms_nonzero = (rms > 0)
bedrms_nonzero = (bedrms > 0)

def my_stats(g):
	filter1 = geo_fltr[g]
	
	sqft_med = ''
	sqft_cnt = len(sqft[filter1*sqft_nonzero])
	if (sqft_cnt > 0):
		sqft_med = np.median(sqft[filter1*sqft_nonzero])
	
	rms_med = ''
	rms_cnt = len(rms[filter1*rms_nonzero])
	if (rms_cnt > 0):
		rms_med = np.median(rms[filter1*rms_nonzero])
	
	bedrms_med = ''
	bedrms_cnt = len(bedrms[filter1*bedrms_nonzero])
	if (bedrms_cnt > 0):
		bedrms_med = np.median(bedrms[filter1*bedrms_nonzero])

	filter2 = geo_fltr[g]*(yr==2012)
	
	sqft_med_sales = ''
	sqft_cnt_sales = len(sqft[filter2*sqft_nonzero])
	if (sqft_cnt_sales > 0):
		sqft_med_sales = np.median(sqft[filter2*sqft_nonzero])
		
	rms_med_sales = ''
	rms_cnt_sales = len(rms[filter2*rms_nonzero])
	if (rms_cnt_sales > 0):
		rms_med_sales = np.median(rms[filter2*rms_nonzero])
		
	bedrms_med_sales = ''
	bedrms_cnt_sales = len(bedrms[filter2*bedrms_nonzero])
	if (bedrms_cnt_sales > 0):
		bedrms_med_sales = np.median(bedrms[filter2*bedrms_nonzero])

	return [g, sqft_med, sqft_cnt, rms_med, rms_cnt, bedrms_med, bedrms_cnt, sqft_med_sales, sqft_cnt_sales, rms_med_sales, rms_cnt_sales, bedrms_med_sales, bedrms_cnt_sales]

table = [my_stats(g) for g in geo_list]
labels = ['geo_id', 'sqft_median', 'sqft_count', 'rooms_median', 'rooms_count', 'bedrms_median', 'bedrms_count', 'sqft_median_2012_sales', 'sqft_count_2012_sales', 'rooms_median_2012_sales', 'rooms_count_2012_sales', 'bedrms_median_2012_sales', 'bedrms_count_2012_sales']
print int(time.time()-t0), 'sec. for numpy'

outname = '../output/stats_sqft_rooms_current_20141017.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
