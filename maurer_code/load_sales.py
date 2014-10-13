# This script imports the Sales data

import psycopg2
import time
import zipfile

fields = ["SR_UNIQUE_ID", "SR_PROPERTY_ID", "SR_SCM_ID",
"MM_STATE_CODE", "MM_MUNI_NAME", "MM_FIPS_STATE_CODE",
"MM_FIPS_MUNI_CODE", "MM_FIPS_COUNTY_NAME", "SR_PARCEL_NBR_RAW",
"SR_SITE_ADDR_RAW", "SR_MAIL_ADDR_RAW", "SR_MAIL_HOUSE_NBR",
"SR_MAIL_FRACTION", "SR_MAIL_DIR", "SR_MAIL_STREET_NAME", "SR_MAIL_SUF",
"SR_MAIL_POST_DIR", "SR_MAIL_UNIT_PRE", "SR_MAIL_UNIT_VAL",
"SR_MAIL_CITY", "SR_MAIL_STATE", "SR_MAIL_ZIP", "SR_MAIL_PLUS_4",
"SR_MAIL_CRRT", "SR_LGL_DSCRPTN", "SR_LGL_KEYED_BLOCK",
"SR_LGL_KEYED_LOT", "SR_LGL_KEYED_PLAT_BOOK", "SR_LGL_KEYED_PLAT_PAGE",
"SR_LGL_KEYED_RANGE", "SR_LGL_KEYED_SECTION", "SR_LGL_KEYED_SUB_NAME",
"SR_LGL_KEYED_TOWNSHIP", "SR_LGL_KEYED_TRACT", "SR_LGL_KEYED_UNIT",
"SR_BUYER", "SR_SELLER", "SR_VAL_TRANSFER", "SR_TAX_TRANSFER",
"SR_DOC_NBR_RAW", "SR_DOC_NBR_FMT", "SR_DATE_TRANSFER",
"SR_DATE_FILING", "SR_DOC_TYPE", "SR_DEED_TYPE", "SR_TRAN_TYPE",
"SR_QUITCLAIM", "SR_ARMS_LENGTH_FLAG", "SR_FULL_PART_CODE",
"SR_MULT_APN_FLAG_KEYED", "SR_MULT_PORT_CODE", "SR_LNDR_SELLER_FLAG",
"SR_TD_DOC_NBR_1", "SR_LOAN_ID_1", "SR_LOAN_ID_1_EXT", "SR_LOAN_VAL_1",
"SR_LOAN_TYPE_1", "SR_INT_RATE_TYPE_1", "SR_LNDR_CREDIT_LINE_1",
"SR_LNDR_CODE_1", "SR_LNDR_FIRST_NAME_1", "SR_LNDR_LAST_NAME_1",
"SR_LENDER_TYPE_1", "SR_TD_DOC_NBR_2", "SR_LOAN_ID_2",
"SR_LOAN_ID_2_EXT", "SR_LOAN_VAL_2", "SR_LOAN_TYPE_2",
"SR_INT_RATE_TYPE_2", "SR_LNDR_CREDIT_LINE_2", "SR_LNDR_CODE_2",
"SR_LNDR_FIRST_NAME_2", "SR_LNDR_LAST_NAME_2", "SR_LENDER_TYPE_2",
"SR_TD_DOC_NBR_3", "SR_LOAN_ID_3", "SR_LOAN_ID_3_EXT", "SR_LOAN_VAL_3",
"SR_LOAN_TYPE_3", "SR_INT_RATE_TYPE_3", "SR_LNDR_CODE_3",
"SR_LNDR_CREDIT_LINE_3", "SR_LNDR_FIRST_NAME_3", "SR_LNDR_LAST_NAME_3",
"SR_LENDER_TYPE_3", "DISTRESS_INDICATOR", "PROCESS_ID"]
# final FILLER field not in the tab-delimited files

field_types = ["int", "int", "int", "varchar", "varchar", "tinyint", "smallint",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "int",
"numeric", "varchar", "varchar", "int", "int", "varchar", "varchar",
"varchar", "bit", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "int", "varchar", "varchar", "varchar",
"int", "varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"int", "varchar", "varchar", "varchar", "int", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "int", "varchar", "varchar",
"int", "varchar", "varchar", "varchar", "varchar", "varchar", "int"]

# Replace SQL Server types with Postgres types as needed
for i, t in enumerate(field_types):

	if (t == 'tinyint'):
		field_types[i] = 'smallint'

	if (t == 'datetime'):
		field_types[i] = 'timestamp'

	if (t == 'bit'):
		field_types[i] = 'boolean'
				
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

# Set up table with field definitions
cur.execute("CREATE TABLE master.sales (" + field_defs +
			", CONSTRAINT sales_pkey PRIMARY KEY (sr_unique_id));")
cur.execute("GRANT SELECT ON TABLE master.sales TO dataquick_user;")
conn.commit()

path = '/home/maurer/Dataquick/Sales_tab_dlm/'
table = 'master.sales'


# Load data into Postgres

t0 = time.time()
count = 0
N = 200 # set for testing only

for fnum in range(1,31):
	zname = 'ARB_HIST_' + str(fnum).zfill(2) + '.zip'
	fname = 'ARB_HIST_' + str(fnum).zfill(2) + '.txt'
	
	with zipfile.ZipFile(path+zname) as z:
		with z.open(fname) as f:
			for line in f:
			#for i in range(N):
				#line = f.readline()

				# split by tabs, remove trailing spaces and final EOL value
				arr = [x.rstrip(' ') for x in line.split('\t')][:-1]
				values = ''
				for i in range(len(fields)):
					val = arr[i]

					# enquote strings, escape single quotes, escape backslashes
					# (the backslashes in the code have to be escaped too, for Python)
					if (field_types[i] == 'varchar'):
						val = "'" + val.replace("'", "''").replace("\\","\\\\") + "'" 

					# replace empty numeric values with nulls
					elif (val == ''):
						val = 'null'

					# also enquote booleans and timestamps
					elif (field_types[i] in ['boolean', 'timestamp']):
						val = "'" + val + "'" 
						
					values += val + ', '
					
				# remove trailing punctuation	
				values = values[:-2]
					
				try:
					cur.execute("INSERT INTO " + table + " VALUES (" + values + ")")
				except:
					print fnum
					print count+1
					print len(line)
					print line
					print values
					
				count += 1
				if (count % 1000000 == 0):
					print "rows //", count
			
conn.commit()
cur.execute("SELECT count(sr_unique_id) FROM " + table)
print "rows //", cur.fetchone()[0]
print "hours //", round((time.time() - t0)*1.0/60/60, 2)


# Add indexes

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX sales_fips_index ON master.sales " +
			" USING btree (mm_fips_muni_code);")
conn.commit()
print "sales_fips_index", round(time.time() - t0)

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX sales_property_index ON master.sales " +
			"USING btree (sr_property_id);")
conn.commit()
print "sales_property index", round(time.time() - t0)

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX sales_date_index ON master.sales " +
			"USING btree (sr_date_transfer);")
conn.commit()
print "sales_property index", round(time.time() - t0)
