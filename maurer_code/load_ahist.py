# This script imports the Assessor data

import psycopg2
import time
import zipfile
import sys

# Add ucb_ahist_id, so we can stick all the years together into a single table
# It's a 16-digit concatenation of year + property id

# (looks like the max value of sa_property_id is 9 digits, but the Dataquick
#  schema specification allows it to be 12 digits, so this seems safest)

fields = ["SA_PROPERTY_ID", "AH_HISTORY_YR", "AH_HISTORY_YR_VERSION", "SA_SCM_ID",
"MM_STATE_CODE", "MM_MUNI_NAME", "MM_FIPS_STATE_CODE",
"MM_FIPS_MUNI_CODE", "MM_FIPS_COUNTY_NAME", "SA_PARCEL_NBR_PRIMARY",
"SA_PARCEL_NBR_PREVIOUS", "SA_OWNER_1", "SA_OWNER_1_FIRST",
"SA_OWNER_1_MID", "SA_OWNER_1_LAST", "SA_OWNER_1_SUF",
"SA_OWNER_1_SP_FIRST", "SA_OWNER_1_SP_MID", "SA_OWNER_1_SP_SUF",
"SA_OWNER_1_GROUP", "SA_OWNER_1_ET_FLAG", "SA_OWNER_1_TRUST_FLAG",
"SA_OWNER_1_TYPE", "SA_OWNER_2", "SA_OWNER_2_FIRST", "SA_OWNER_2_MID",
"SA_OWNER_2_LAST", "SA_OWNER_2_SUF", "SA_OWNER_2_SP_FIRST",
"SA_OWNER_2_SP_MID", "SA_OWNER_2_SP_SUF", "SA_OWNER_2_GROUP",
"SA_OWNER_2_ET_FLAG", "SA_OWNER_2_TRUST_FLAG", "SA_OWNER_2_TYPE",
"SA_OWNERSHIP_STATUS_CODE", "SA_SITE_HOUSE_NBR", "SA_SITE_FRACTION",
"SA_SITE_DIR", "SA_SITE_STREET_NAME", "SA_SITE_SUF", "SA_SITE_POST_DIR",
"SA_SITE_UNIT_PRE", "SA_SITE_UNIT_VAL", "SA_SITE_CITY", "SA_SITE_STATE",
"SA_SITE_ZIP", "SA_SITE_PLUS_4", "SA_SITE_CRRT", "SA_MAIL_HOUSE_NBR",
"SA_MAIL_FRACTION", "SA_MAIL_DIR", "SA_MAIL_STREET_NAME", "SA_MAIL_SUF",
"SA_MAIL_POST_DIR", "SA_MAIL_UNIT_PRE", "SA_MAIL_UNIT_VAL",
"SA_MAIL_CITY", "SA_MAIL_STATE", "SA_MAIL_ZIP", "SA_MAIL_PLUS_4",
"SA_MAIL_CRRT", "SA_SITE_MAIL_SAME", "OWNER_OCCUPANCY_CODE",
"USE_CODE_STD", "ASSR_YEAR", "SA_VAL_ASSD", "SA_VAL_ASSD_LAND",
"SA_VAL_ASSD_IMPRV", "SA_APPRAISE_VAL", "SA_VAL_APPRAISE_LAND",
"SA_VAL_APPRAISE_IMPRV", "SA_IMPRV_PCT_APPRAISE", "SA_VAL_MARKET",
"SA_VAL_MARKET_LAND", "SA_VAL_MARKET_IMPRV", "SA_EXEMP_FLAG_1",
"SA_EXEMP_VAL_1", "SA_EXEMP_FLAG_2", "SA_EXEMP_VAL_2",
"SA_EXEMP_FLAG_3", "SA_EXEMP_VAL_3", "SA_EXEMP_FLAG_4",
"SA_EXEMP_VAL_4", "SA_EXEMP_FLAG_5", "SA_EXEMP_VAL_5",
"SA_EXEMP_FLAG_6", "SA_EXEMP_VAL_6", "TAXYEAR", "SA_TAX_VAL",
"SA_ARCHITECTURE_CODE", "SA_ATTIC_SQFT", "SA_BLDG_SQFT",
"SA_BSMT_2_CODE", "SA_BSMT_FIN_SQFT", "SA_BSMT_UNFIN_SQFT",
"SA_COOL_CODE", "SA_EXTERIOR_1_CODE", "SA_FIN_SQFT_1", "SA_FIN_SQFT_2",
"SA_FIN_SQFT_3", "SA_FIN_SQFT_4", "SA_FIN_SQFT_TOT",
"SA_FIREPLACE_CODE", "SA_FOUNDATION_CODE", "SA_GRG_1_CODE",
"SA_GRG_SQFT_1", "SA_HEAT_CODE", "SA_LOTSIZE", "SA_NBR_BATH",
"SA_NBR_BATH_1QTR", "SA_NBR_BATH_HALF", "SA_NBR_BATH_3QTR",
"SA_NBR_BATH_FULL", "SA_NBR_BATH_BSMT_HALF", "SA_NBR_BATH_BSMT_FULL",
"SA_NBR_BEDRMS", "SA_NBR_RMS", "SA_NBR_STORIES", "SA_NBR_UNITS",
"SA_PATIO_PORCH_CODE", "SA_POOL_CODE", "SA_PRIVACY_CODE",
"SA_ROOF_CODE", "SA_SQFT", "SA_SQFT_ASSR_TOT", "SA_SQFT_DQ",
"SA_STRUCTURE_CODE", "SA_YR_BLT", "SA_YR_BLT_EFFECT",
"SA_DATE_TRANSFER", "SA_VAL_TRANSFER", "SA_DOC_NBR_FMT",
"SA_DATE_NOVAL_TRANSFER", "SA_DOC_NBR_NOVAL", "PROCESS_ID",
"SA_INACTIVE_PARCEL_FLAG", "SA_SHELL_PARCEL_FLAG", "FILLER", "UCB_AHIST_ID"]

field_types = ["int", "int", "tinyint", "int", "varchar", "varchar", "tinyint",
"smallint", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "int", "smallint", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "int", "smallint",
"varchar", "varchar", "tinyint", "varchar", "varchar", "int", "int",
"int", "int", "int", "int", "numeric", "int", "int", "int", "varchar",
"int", "varchar", "int", "varchar", "int", "varchar", "int", "varchar",
"int", "varchar", "int", "varchar", "numeric", "varchar", "smallint",
"smallint", "varchar", "smallint", "smallint", "varchar", "varchar",
"int", "int", "int", "int", "int", "varchar", "varchar", "varchar",
"smallint", "varchar", "numeric", "numeric", "smallint", "smallint",
"smallint", "smallint", "smallint", "smallint", "smallint", "smallint",
"tinyint", "smallint", "varchar", "varchar", "varchar", "varchar",
"int", "int", "int", "varchar", "smallint", "smallint", "int", "int",
"varchar", "int", "varchar", "int", "varchar", "varchar", "varchar", "bigint"]

# Replace SQL Server types with Postgres types as needed
for i, t in enumerate(field_types):

	if (t == 'tinyint'):
		field_types[i] = 'smallint'

	if (t == 'datetime'):
		field_types[i] = 'timestamp'

field_lengths = [12, 4, 2, 12, 2, 24, 5, 7, 35, 35, 35, 50, 50, 20, 50, 5, 20, 20, 5, 15,
1, 1, 1, 50, 50, 20, 20, 5, 20, 20, 5, 15, 1, 1, 1, 2, 20, 10, 2, 40, 4,
2, 10, 6, 30, 2, 12, 7, 4, 20, 10, 2, 50, 4, 2, 10, 6, 50, 2, 12, 7, 4,
1, 2, 4, 4, 12, 12, 12, 12, 12, 12, 8, 12, 12, 12, 1, 12, 1, 12, 1, 12,
1, 12, 1, 12, 1, 12, 4, 12, 1, 7, 7, 2, 7, 7, 2, 2, 12, 12, 12, 12, 12,
2, 2, 2, 7, 2, 19, 8, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 2, 2, 1, 2, 12, 12,
12, 2, 4, 4, 12, 12, 20, 12, 20, 12, 1, 1, 40,]

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

path = '/home/maurer/Dataquick/Assessor_History/'
table = 'master.ahist'

# Set up table with field definitions
try:
	cur.execute("CREATE TABLE " + table + " (" + field_defs +
				", CONSTRAINT ahist_pkey PRIMARY KEY (ucb_ahist_id));")
	cur.execute("GRANT SELECT ON TABLE " + table + " TO dataquick_user;")
except:
	pass

# Load data into Postgres

conn.commit()
t0 = time.time()
count = 0
N = 100 # set for testing only

for fnum in range(2013, 2015):
	zname = 'AH_' + str(fnum) + '.ZIP'
	fname = 'AH_' + str(fnum) + '.TXT'
	
	with zipfile.ZipFile(path+zname) as z:
		with z.open(fname) as f:
			for line in f:
			#for i in range(N):
				#line = f.readline()

				pos = 0
				values = ''
			
				for i in range(len(fields)-1): # subtract 1 for ucb_ahist_id
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
					
				# if not adding ucb_ahist_id, need to remove trailing punctuation
				ahist_id = line[12:16] + line[0:12].rstrip(' ').zfill(12)	
				values = values + ahist_id
					
				try:
					cur.execute("INSERT INTO " + table + " VALUES (" + values + ")")
				except Exception, e:
					print str(e)
					print fnum
					print count+1
					print len(line)
					print line
					print values
					sys.exit()
					
				count += 1
				if (count % 1000000 == 0):
					print "rows //", count

	conn.commit() # after each year of data
		
cur.execute("SELECT count(ucb_ahist_id) FROM " + table)
print "rows //", cur.fetchone()[0]
print "hours //", round((time.time() - t0)*1.0/60/60, 2)
print "seconds //", int(time.time()-t0)


# Add indexes

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX ahist_property_index ON " + table + 
			" USING btree (sa_property_id);")
conn.commit()
print "ahist_property_index", round(time.time() - t0)

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX ahist_year_index ON " + table + 
			" USING btree (ah_history_yr);")
conn.commit()
print "ahist_year_index", round(time.time() - t0)

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX ahist_fips_index ON " + table + 
			" USING btree (mm_fips_muni_code);")
conn.commit()
print "ahist_fips_index", round(time.time() - t0)
