# This script tabulates improvement value
# Takes about 10 sec to run on server

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t0 = time.time()
cur.execute(""" SELECT ucb_geo_id, 
					sa_imprv_pct,
					substring(use_code_std from 1 for 1) AS use
				FROM master.assessor 
				WHERE mm_fips_muni_code IN (1, 13, 41, 55, 75, 81, 85, 95, 97) 
					AND substring(use_code_std from 1 for 1) in ('R', 'C') 
					AND sa_property_id IN (
					
						SELECT distinct(sr_property_id)
						FROM master.sales
						WHERE mm_fips_muni_code IN (1, 13, 41, 55, 75, 81, 85, 95, 97) 
							AND sr_arms_length_flag = '1' 
							AND (sr_date_transfer/10000) = 2012
						) """)

out = cur.fetchall()
print int(time.time()-t0), 'sec. for postgres'

t0 = time.time()
geo = np.array([r[0] for r in out])
imp = np.array([float(r[1]) for r in out])
use = np.array([r[2] for r in out])

geo_fltr = {g: (geo==g) for g in np.unique(geo)}
use_fltr = {u: (use==u) for u in np.unique(use)}

def my_stats(g):
	stats = []
	for u in ['R', 'C']:
		fltr = geo_fltr[g] * use_fltr[u]
		med_pct= ''
		stdev_pct = ''
		count = len(imp[fltr])
		if (count > 0):
			med_pct = round(np.median(imp[fltr]), 2)
			stdev_pct = round(np.std(imp[fltr]), 1)
		stats += [med_pct, stdev_pct, count]
	return [g] + stats
	
table = [my_stats(g) for g in np.unique(geo)]
labels = ['geo_id', 'res_imprv_pct_median', 'res_imprv_pct_stdev', 'res_count', 'com_imprv_pct_median', 'com_imprv_pct_stdev', 'com_count']
print int(time.time()-t0), 'sec. for numpy'

outname = '../output/stats_improvement_current_20141017.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
