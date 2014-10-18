# This script tabulates new construction
# Takes about 2 min to run on server

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t0 = time.time()
cur.execute(""" SELECT ucb_geo_id, 
					sa_yr_blt
				FROM master.assessor 
				WHERE mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97) 
					AND substring(use_code_std from 1 for 1) = 'R' ; """)

out = cur.fetchall()
print int(time.time()-t0), 'sec. for postgres'

t0 = time.time()
geo = np.array([r[0] for r in out])
yr = np.array([r[1] for r in out])

geo_list = np.unique(geo).tolist()
geo_fltr = {g: (geo==g) for g in geo_list}

yr_list = range(1988, 2015)
yr_fltr = {y: (yr==y) for y in yr_list}

def my_stats(g):
	counts = [len(yr[geo_fltr[g]*yr_fltr[y]]) for y in yr_list]
	return [g] + counts

table = [my_stats(g) for g in geo_list]
labels = ['geo_id'] + yr_list
print int(time.time()-t0), 'sec. for numpy'

outname = '../output/stats_construction_20141017.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
