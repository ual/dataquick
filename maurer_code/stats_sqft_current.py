# This script tabulates square footage
# Takes about 3 min to run on server

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t0 = time.time()
cur.execute(""" SELECT ucb_geo_id, sa_sqft, (sa_date_transfer/10000) AS yr
				FROM master.assessor 
				WHERE mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
					AND substring(use_code_std from 1 for 1) = 'R'; """)

out = cur.fetchall()
print int(time.time()-t0), 'sec. for postgres'

t0 = time.time()
geo = np.array([r[0] for r in out])
sqft = np.array([r[1] for r in out])
yr = np.array([r[2] for r in out])

geo_list = np.unique(geo).tolist()
geo_fltr = {g: (geo==g) for g in geo_list}

def my_stats(g):
	med_sqft = np.median(sqft[geo_fltr[g]])
	count1 = len(sqft[geo_fltr[g]])
	med_sqft_sales = '' # for recent sales
	count2 = len(sqft[geo_fltr[g]*(yr==2014)])
	if (count2 > 0):
		med_sqft_sales = np.median(sqft[geo_fltr[g]*(yr==2014)])
	return [g, med_sqft, count1, med_sqft_sales, count2]

table = [my_stats(g) for g in geo_list]
labels = ['geo_id', 'med_sqft', 'count1', 'med_sqft_2014_sales', 'count2']
print int(time.time()-t0), 'sec. for numpy'

outname = '../output/stats_sqft_current_20141017.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
