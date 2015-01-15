# This script tabulates sales
# Takes about 4 min to run on server

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t0 = time.time()
cur.execute('''

SELECT 
	ucb_geo_id, 
	(sr_date_transfer/10000) AS sr_year
FROM 
	master.sales_clean 
	
''')

out = cur.fetchall()
print int(time.time()-t0), 'sec. for postgres'

t0 = time.time()
geo = np.array([r[0] for r in out])
year = np.array([r[1] for r in out])

geo_list = np.unique(geo).tolist()
year_list = np.unique(year).tolist()

geo_fltr = {g: (geo==g) for g in geo_list}
year_fltr = {y: (year==y) for y in year_list}

def my_stats(g):
	year_counts = [len(year[geo_fltr[g]*year_fltr[y]]) for y in year_list]
	return [g] + year_counts

table = [my_stats(g) for g in geo_list]
labels = ['geo_id'] + year_list
print int(time.time()-t0), 'sec. for numpy'

outname = '../output/stats_sales_residential_20150114.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
