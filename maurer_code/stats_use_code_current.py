# This script tabulates use codes
# Takes about 5 min to run locally

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t0 = time.time()
cur.execute(""" SELECT ucb_geo_id, use_code_std
				FROM master.assessor 
				WHERE mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97); """)

out = cur.fetchall()
print int(time.time()-t0), 'sec. for postgres'

t0 = time.time()
geo = np.array([r[0] for r in out])
uses1 = np.array([r[1][0] if r[1] is not '' else '' for r in out]) # first char of use cd
uses2 = np.array([r[1] for r in out]) # full use codes

geo_list = np.unique(geo).tolist()
uses1_list = np.unique(uses1).tolist()
uses2_list = np.unique(uses2[uses2!='']).tolist() # skip missing use codes this time

geo_fltr = {g: (geo==g) for g in geo_list}
uses1_fltr = {u: (uses1==u) for u in uses1_list}
uses2_fltr = {u: (uses2==u) for u in uses2_list}

def my_stats(g):
	use1_counts = [len(uses1[geo_fltr[g]*uses1_fltr[u]]) for u in uses1_list]
	use2_counts = [len(uses2[geo_fltr[g]*uses2_fltr[u]]) for u in uses2_list]
	return [g] + use1_counts + use2_counts

table = [my_stats(g) for g in geo_list]
labels = ['geo_id'] + uses1_list + uses2_list
print int(time.time()-t0), 'sec. for numpy'

outname = '../output/stats_use_code_current_20141017.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
