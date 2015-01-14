# This script tabulates use codes
# Takes about 1 hour to run on server

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t0 = time.time()
cur.execute(""" SELECT a.ucb_geo_id, h.use_code_std, h.ah_history_yr
				FROM master.ahist AS h
				INNER JOIN master.assessor AS a
				ON a.sa_property_id = h.sa_property_id
				WHERE h.ah_history_yr_version = 1 
					AND h.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97); """)

out = cur.fetchall()
print int(time.time()-t0), 'sec. for postgres'

t0 = time.time()
geo = np.array([r[0] for r in out])
uses1 = np.array([r[1][0] if r[1] is not '' else '' for r in out]) # first char of use cd
#uses2 = np.array([r[1] for r in out]) # full use codes
year = np.array([r[2] for r in out])

geo_list = np.unique(geo).tolist()
uses1_list = np.unique(uses1).tolist()
#uses2_list = np.unique(uses2[uses2!='']).tolist() # skip missing use codes this time
year_list = np.unique(year).tolist()

geo_fltr = {g: (geo==g) for g in geo_list}
uses1_fltr = {u: (uses1==u) for u in uses1_list}
#uses2_fltr = {u: (uses2==u) for u in uses2_list}
year_fltr = {y: (year==y) for y in year_list}

def my_stats(g):
	use1_counts = []
	for y in year_list:
		fltr = geo_fltr[g]*year_fltr[y]
		use1_counts += [np.sum(fltr*uses1_fltr[u]) for u in uses1_list]
	return [g] + use1_counts

table = [my_stats(g) for g in geo_list]
print int(time.time()-t0), 'sec. for numpy'

labels = ['geo_id']
for y in year_list:
	for u in ['blank'] + uses1_list[1:]:
		labels.append(str(y) + '_' + u)

outname = '../output/stats_use_code_hist_20141102.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
