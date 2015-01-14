# This script imports the Foreclosure data

import psycopg2
import time
import zipfile
import sys

# try unique_id_notice as primary key...

fields = ["SA_PROPERTY_ID", "SCM_ID", "MM_STATE_CODE", "MM_MUNI_NAME",
"MM_FIPS_STATE_CODE", "MM_FIPS_MUNI_CODE", "MM_FIPS_COUNTY_NAME",
"SR_UNIQUE_ID", "UNIQUE_ID_NOTICE", "RECORD_TYPE", "PARCEL_NBR_RAW",
"RECORDING_DATE", "DOCUMENT_NO", "DOC_TYPE", "DATE_ORIG_LOAN",
"DOC_NBR_ORIG_LOAN", "ORIG_LOAN_AMT", "TRUSTOR_FIRST_NAME",
"TRUSTOR_LAST_NAME", "TRUSTEE_NAME_FIRST", "TRUSTEE_NAME_LAST",
"TRUSTEE_HOUSE_NBR", "TRUSTEE_STREET_NAME", "TRUSTEE_UNIT_NBR",
"TRUSTEE_CITY", "TRUSTEE_STATE", "TRUSTEE_ZIP", "TRUSTEE_PHONE",
"TRUSTEE_SALE_NBR", "TITLE_COMPANY_CODE", "TITLE_COMPANY_NAME",
"PROCESS_ID", "FD_DELINQUENT_DATE", "FD_DELINQUENT_AMT",
"FD_BALANCE_PRINCIPAL", "FD_BENEFICIARY_NAME_FIRST",
"FD_BENEFICIARY_NAME_LAST", "FD_BENEFICIARY_HOUSE_NBR",
"FD_BENEFICIARY_STREET_NAME", "FD_BENEFICIARY_UNIT_NBR",
"FD_BENEFICIARY_CITY", "FD_BENEFICIARY_STATE", "FD_BENEFICIARY_ZIP",
"FD_BENEFICIARY_PHONE", "FD_NOD_T_AUCT_DATE", "FD_NOD_T_SALE_TIME",
"FD_NOD_T_TIME_TYPE", "FD_NOD_T_AUCT_STREET_NO",
"FD_NOD_T_AUCT_STREET_NAME", "FD_NOD_T_AUCT_CITY",
"FT_AMOUNT_OF_DEFAULT", "FT_BALANCE_PRINCIPAL", "FT_SITE_HOUSE_NBR",
"FT_SITE_STREET_NAME", "FT_SITE_UNIT_NBR", "FT_SITE_CITY",
"FT_SITE_STATE", "FT_SITE_ZIP", "FT_NOT_SALE_DATE", "FT_NOT_SALE_TIME",
"FT_NOT_TIME_TYPE", "FT_NOT_SALE_STREET_NO", "FT_NOT_SALE_STREET_NAME",
"FT_NOT_SALE_CITY", "FT_NTDS_AUCTION_BID_AMOUNT", "FILLER"]

# orig_loan_amt needs to be changed from int to bigint,
# possibly because of an error in the data?

field_types = ["int", "int", "varchar", "varchar", "tinyint",
"smallint", "varchar", "int", "int", "varchar", "varchar", "int",
"varchar", "varchar", "int", "varchar", "bigint", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "int", "varchar", "int",
"int", "numeric", "numeric", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "int", "varchar",
"varchar", "varchar", "varchar", "varchar", "numeric", "numeric",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "int",
"varchar", "varchar", "varchar", "varchar", "varchar", "numeric", "varchar"]

# Replace SQL Server types with Postgres types as needed
for i, t in enumerate(field_types):

	if (t == 'tinyint'):
		field_types[i] = 'smallint'

	if (t == 'datetime'):
		field_types[i] = 'timestamp'

field_lengths = [12, 12, 2, 24, 2, 3, 35, 12, 12, 1, 35, 8, 20, 1, 8, 20, 12, 50, 25, 50,
25, 10, 50, 5, 50, 2, 5, 10, 15, 12, 30, 12, 8, 12, 12, 50, 25, 10, 50,
5, 50, 2, 5, 10, 8, 5, 1, 10, 50, 50, 12, 12, 10, 50, 5, 50, 2, 5, 8, 5,
1, 10, 50, 50, 12, 13]

# Generate field strings for sql queries
field_defs = ''
for i in range(len(fields)):
	field_defs += fields[i] + ' ' + field_types[i] + ', '
field_defs = field_defs[:-2] # remove trailing punctuation


################################################################

# Connect to the database
conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_admin' password='Visua1ization'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

path = '/home/maurer/Dataquick/Foreclosure/'
table = 'master.foreclosure'

# Set up table with field definitions
try:
	cur.execute("CREATE TABLE " + table + " (" + field_defs +
				", CONSTRAINT foreclosure_pkey PRIMARY KEY (unique_id_notice));")
	cur.execute("GRANT SELECT ON TABLE " + table + " TO dataquick_user;")
except:
	pass

# Load data into Postgres

conn.commit()
t0 = time.time()
count = 0
N = 100 # set for testing only

with zipfile.ZipFile(path+'ARB_FORE.zip') as z:
	with z.open('ARB_FORE.txt') as f:
		for line in f:
		#for i in range(N):
			#line = f.readline()

			pos = 0
			values = ''
		
			for i in range(len(fields)):
				flen = field_lengths[i]
				val = line[pos:pos+flen].rstrip(' ')
				pos += flen
			
				# enquote strings, escape single quotes, escape backslashes
				# (the backslashes in the code have to be escaped too, for Python)
				if (field_types[i] == 'varchar'):
					val = "'" + val.replace("'", "''").replace("\\","\\\\") + "'" 

				# replace empty numeric values with nulls
				elif (val == ''):
					val = 'null'

				# also enquote timestamps
				elif (field_types[i] == 'timestamp'):
					val = "'" + val + "'" 
				
				values += val + ', '
				
			values = values[:-2] # remove trailing punctuation
				
			try:
				cur.execute("INSERT INTO " + table + " VALUES (" + values + ")")
			except Exception, e:
				print str(e)
				print count+1
				print len(line)
				print line
				print values
				sys.exit()
				
			count += 1
			if (count % 1000000 == 0):
				print "rows //", count

conn.commit()
		
cur.execute("SELECT count(unique_id_notice) FROM " + table)
print "rows //", cur.fetchone()[0]
print "hours //", round((time.time() - t0)*1.0/60/60, 2)
print "seconds //", int(time.time()-t0)


# Add indexes

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX foreclosure_property_index ON " + table + 
			" USING btree (sa_property_id);")
conn.commit()
print "foreclosure_property_index", round(time.time() - t0)

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX foreclosure_fips_index ON " + table + 
			" USING btree (mm_fips_muni_code);")
conn.commit()
print "foreclosure_fips_index", round(time.time() - t0)
