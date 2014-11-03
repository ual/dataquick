#!/usr/bin/python

# This script tabulates absentee ownership
# Takes about 10 min to run on server

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t_total = time.time()

# each data structure is a dictionary of years..

year_list = range(2004, 2015)
geo_list = {}
geo_fltr = {}
abs_list = {}
abs_fltr = {}

for y in year_list:

	t0 = time.time()
	cur.execute(""" SELECT a.ucb_geo_id, 
						ah.sa_site_mail_same
					FROM master.ahist AS ah
					INNER JOIN master.assessor AS a 
					ON a.sa_property_id = ah.sa_property_id
					WHERE ah.ah_history_yr = %s 
						AND ah.ah_history_yr_version = 1 
						AND ah.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
						AND substring(ah.use_code_std from 1 for 1) = 'R'; 
				""", (y,))

	out = cur.fetchall()
	print int(time.time()-t0), 'sec. for postgres', y

	t0 = time.time()
	geo = np.array([r[0] for r in out])
	abs = np.array([r[1] for r in out])

	geo_list[y] = np.unique(geo).tolist()
	geo_fltr[y] = {g: (geo==g) for g in geo_list[y]}

	abs_list[y] = ['Y', 'N', 'U']
	abs_fltr[y] = {a: (abs==a) for a in abs_list[y]}
	
	print int(time.time()-t0), 'sec. for numpy filter setup', y

def my_stats(g):
	stats = []
	for y in year_list:
		for a in abs_list[y]:
			if g in geo_list[y]:
				s = np.sum(geo_fltr[y][g] * abs_fltr[y][a])
			else:
				s = 0
			stats.append(s)
	return [g] + stats

t0 = time.time()
master_geo_list = np.unique([g for y in year_list for g in geo_list[y]]).tolist()

table = [my_stats(g) for g in master_geo_list]
print int(time.time()-t0), 'sec. for numpy stats'
print int(time.time()-t_total), 'sec. total'

labels = ['geo_id'] 
for y in year_list:
	labels += [str(y) + '_' + a for a in abs_list[y]]

outname = '../output/stats_absentee_hist_20141102.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
