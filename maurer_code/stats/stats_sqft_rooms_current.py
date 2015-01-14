# This script tabulates square footage, rooms, bedrooms
# Takes about 1.5 min to run on server

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
					sa_property_id IN (
						SELECT distinct(sr_property_id)
						FROM master.sales
						WHERE mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97) 
							AND sr_arms_length_flag = '1' 
							AND (sr_date_transfer/10000) = 2012
						) AS sale
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
sale = np.array([r[4] for r in out])

geo_list = np.unique(geo).tolist()
geo_fltr = {g: (geo==g) for g in geo_list}
sale_fltr = (sale==True)

sqft_nonzero = (sqft > 0)
rms_nonzero = (rms > 0)
bedrms_nonzero = (bedrms > 0)

def med_cnt(data, fltr):
	cnt = np.sum(fltr)
	med = np.median(data[fltr]) if (cnt > 0) else ''
	return [med, cnt]

def my_stats(g):
	stats = []
	for f in (geo_fltr[g], geo_fltr[g]*sale_fltr):
		stats += med_cnt(sqft, f*sqft_nonzero)
		stats += med_cnt(rms, f*rms_nonzero)
		stats += med_cnt(bedrms, f*bedrms_nonzero)
	return [g] + stats

table = [my_stats(g) for g in geo_list]
labels = ['geo_id', 'sqft_median', 'sqft_count', 'rooms_median', 'rooms_count', 'bedrms_median', 'bedrms_count', 'sqft_median_2012_sales', 'sqft_count_2012_sales', 'rooms_median_2012_sales', 'rooms_count_2012_sales', 'bedrms_median_2012_sales', 'bedrms_count_2012_sales']
print int(time.time()-t0), 'sec. for numpy'

outname = '../output/stats_sqft_rooms_current_20141018.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
