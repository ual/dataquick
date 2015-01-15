# This script sets up the inflation adjustment data table

import psycopg2
import sys

# Connect to the database
conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_admin' password='Visua1ization'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# Set up table 
cur.execute("CREATE TABLE master.inflation_adjustment " +
			"(year INT, price_multiple NUMERIC, "
			"CONSTRAINT inflation_pkey PRIMARY KEY (year));")
cur.execute("GRANT SELECT ON TABLE master.inflation_adjustment TO dataquick_user;")

# http://www.bls.gov/data/inflation_calculator.htm
price_multiple = {1988: 1.84, 1989: 1.76, 1990: 1.67, 1991: 1.61, 1992: 1.56, 1993: 1.51, 
    1994: 1.48, 1995: 1.43, 1996: 1.39, 1997: 1.36, 1998: 1.34, 1999: 1.31, 2000: 1.27, 
    2001: 1.23, 2002: 1.21, 2003: 1.18, 2004: 1.16, 2005: 1.12, 2006: 1.08, 2007: 1.06, 
    2008: 1.02, 2009: 1.02, 2010: 1.00, 2011: 0.97, 2012: 0.95, 2013: 0.94, 2014: 0.92}

# Load data into Postgres
conn.commit()
for year in price_multiple:
	values = str(year) + ", " + str(price_multiple[year])
	try:
		cur.execute("INSERT INTO master.inflation_adjustment VALUES (" + values + ")")
	except Exception, e:
		print str(e)
		print values
		sys.exit()
				
conn.commit()
print "finished"