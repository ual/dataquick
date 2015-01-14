#!/usr/bin/python

# This script tabulates prices for single-family homes
# Takes about 20 min to run on server

import psycopg2
import numpy as np
import time
import csv

conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

t_total = time.time()

year_list = range(1988, 2015)

# http://www.bls.gov/data/inflation_calculator.htm
price_index = {1988: 2.01, 1989: 1.92, 1990: 1.82, 1991: 1.75, 1992: 1.70, 1993: 1.65, 
	1994: 1.61, 1995: 1.56, 1996: 1.52, 1997: 1.48, 1998: 1.46, 1999: 1.43, 2000: 1.38, 
	2001: 1.34, 2002: 1.32, 2003: 1.29, 2004: 1.26, 2005: 1.22, 2006: 1.18, 2007: 1.15, 
	2008: 1.11, 2009: 1.11, 2010: 1.09, 2011: 1.06, 2012: 1.04, 2013: 1.02, 2014: 1.00}

# vars are dictionaries of arrays for each year
price_sqft = {} 
geo_list = {}
geo_fltr = {}

for y in year_list:

	t0 = time.time()
	
	cur.execute(""" 
		
SELECT 
	a.ucb_geo_id, 
	s.sr_val_transfer, 
	a.sa_sqft
FROM
	master.sales AS s
INNER JOIN 
	master.assessor AS a 
ON 
	a.sa_property_id = s.sr_property_id
INNER JOIN
	(SELECT
		mm_fips_muni_code,
		sr_date_transfer,
		sr_doc_nbr_fmt,
		count(*) AS ucb_dup_count
	FROM
		master.sales
	WHERE 
		mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
		AND (sr_date_transfer / 10000) = %s
		AND sr_arms_length_flag = '1'
	GROUP BY
		mm_fips_muni_code,
		sr_date_transfer,
		sr_doc_nbr_fmt) AS c
ON
	c.mm_fips_muni_code = s.mm_fips_muni_code
	AND c.sr_date_transfer = s.sr_date_transfer
	AND c.sr_doc_nbr_fmt = s.sr_doc_nbr_fmt
WHERE 
	s.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
	AND c.ucb_dup_count = 1
	AND (s.sr_date_transfer / 10000) = %s 
	AND s.sr_arms_length_flag = '1'
	AND s.sr_val_transfer > 0
	AND a.sa_sqft > 0
	AND substring(a.use_code_std from 1 for 1) = 'R'
	AND a.use_code_std NOT IN ('RSFR','RMOB');
					""", (y,y))

	out = cur.fetchall()
	
	print int(time.time()-t0), 'sec. for postgres', y

	t0 = time.time()
	geo = np.array([r[0] for r in out])

	price_sqft[y] = np.array([r[1]*price_index[y]/r[2] for r in out])

	geo_list[y] = np.unique(geo).tolist()
	geo_fltr[y] = {g: (geo==g) for g in geo_list[y]}
	
	print int(time.time()-t0), 'sec. for numpy filter setup', y

def my_stats(g):
	stats = []
	for y in year_list:
		price = ''
		count = 0
		if g in geo_list[y]:
			fltr = geo_fltr[y][g]
			price = round(np.median(price_sqft[y][fltr]), 2)
			count = np.sum(fltr)
		stats += [price, count]
	return [g] + stats

t0 = time.time()
master_geo_list = np.unique([g for y in year_list for g in geo_list[y]]).tolist()

table = [my_stats(g) for g in master_geo_list]
print int(time.time()-t0), 'sec. for numpy stats'
print int(time.time()-t_total), 'sec. total'

labels = ['geo_id'] 
for y in year_list:
	labels += [str(y)+'_price_sqft', str(y)+'_count']

outname = '../output/stats_price_multifam_20141206.csv'

with open(outname, 'wb') as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(labels)
	writer.writerows(table)

print 'done'
