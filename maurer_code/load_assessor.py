# This script imports the Assessor data

import psycopg2
import time
import zipfile

fields = ["SA_PROPERTY_ID", "SA_SCM_ID", "MM_STATE_CODE", "MM_MUNI_NAME",
"MM_FIPS_STATE_CODE", "MM_FIPS_MUNI_CODE", "MM_FIPS_COUNTY_NAME", 
"SA_PARCEL_NBR_PRIMARY", "SA_PARCEL_NBR_REFERENCE",
"SA_PARCEL_ACCOUNT_NBR", "SA_PARCEL_NBR_ALT", "SA_PARCEL_NBR_PREVIOUS",
"SA_PARCEL_NBR_CHANGE_YR", "SA_YR_APN_ADDED", "SA_OWNER_1",
"SA_OWNER_1_FIRST", "SA_OWNER_1_MID", "SA_OWNER_1_LAST",
"SA_OWNER_1_SUF", "SA_OWNER_1_SP_FIRST", "SA_OWNER_1_SP_MID",
"SA_OWNER_1_SP_SUF", "SA_OWNER_1_GROUP", "SA_OWNER_1_ET_FLAG",
"SA_OWNER_1_TRUST_FLAG", "SA_OWNER_1_TYPE", "SA_OWNER_2",
"SA_OWNER_2_FIRST", "SA_OWNER_2_MID", "SA_OWNER_2_LAST",
"SA_OWNER_2_SUF", "SA_OWNER_2_SP_FIRST", "SA_OWNER_2_SP_MID",
"SA_OWNER_2_SP_SUF", "SA_OWNER_2_GROUP", "SA_OWNER_2_ET_FLAG",
"SA_OWNER_2_TRUST_FLAG", "SA_OWNER_2_TYPE", "SA_OWNERSHIP_STATUS_CODE",
"SA_COMPANY_FLAG", "SA_SITE_HOUSE_NBR", "SA_SITE_FRACTION",
"SA_SITE_DIR", "SA_SITE_STREET_NAME", "SA_SITE_SUF", "SA_SITE_POST_DIR",
"SA_SITE_UNIT_PRE", "SA_SITE_UNIT_VAL", "SA_SITE_CITY", "SA_SITE_STATE",
"SA_SITE_ZIP", "SA_SITE_PLUS_4", "SA_SITE_CRRT", "SA_MAIL_HOUSE_NBR",
"SA_MAIL_FRACTION", "SA_MAIL_DIR", "SA_MAIL_STREET_NAME", "SA_MAIL_SUF",
"SA_MAIL_POST_DIR", "SA_MAIL_UNIT_PRE", "SA_MAIL_UNIT_VAL",
"SA_MAIL_CITY", "SA_MAIL_STATE", "SA_MAIL_ZIP", "SA_MAIL_PLUS_4",
"SA_MAIL_CRRT", "SA_SITE_MAIL_SAME", "SA_LGL_DSCRPTN", "SA_LOT_NBR_1",
"SA_LOT_NBR_2", "SA_LOT_NBR_3", "SA_BLK_NBR_1", "SA_BLK_NBR_2",
"SA_TOWNSHIP", "SA_RANGE", "SA_SECTION", "SA_QUARTER",
"SA_QUARTER_QUARTER", "SA_SUBDIVISION", "SA_TRACT_NBR", "SA_LGL_UNIT",
"USE_CODE_STD", "USE_CODE_MUNI", "SA_ZONING", "ASSR_YEAR",
"SA_VAL_ASSD", "SA_VAL_ASSD_LAND", "SA_VAL_ASSD_IMPRV", "SA_IMPRV_PCT",
"SA_APPRAISE_YR", "SA_YR_LAND_APPRAISE", "SA_APPRAISE_VAL",
"SA_VAL_APPRAISE_LAND", "SA_VAL_APPRAISE_IMPRV",
"SA_IMPRV_PCT_APPRAISE", "SA_VAL_MARKET", "SA_VAL_MARKET_LAND",
"SA_VAL_MARKET_IMPRV", "SA_IMPRV_PCT_MRKT", "SA_EXEMP_FLAG_1",
"SA_EXEMP_VAL_1", "SA_EXEMP_FLAG_2", "SA_EXEMP_VAL_2",
"SA_EXEMP_FLAG_3", "SA_EXEMP_VAL_3", "SA_EXEMP_FLAG_4",
"SA_EXEMP_VAL_4", "SA_EXEMP_FLAG_5", "SA_EXEMP_VAL_5",
"SA_EXEMP_FLAG_6", "SA_EXEMP_VAL_6", "SA_VAL_FULL_CASH",
"SA_VAL_ASSD_PREV", "TAXYEAR", "SA_TAX_VAL", "SA_TAX_YEAR_DELINQ",
"LAST_ASSR_UPD", "LAST_TAX_UPDT", "SA_ADDTNS_SQFT",
"SA_ARCHITECTURE_CODE", "SA_ATTIC_SQFT", "SA_BLDG_CODE",
"SA_BLDG_SHAPE_CODE", "SA_BLDG_SQFT", "SA_BSMT_2_CODE",
"SA_BSMT_FIN_SQFT", "SA_BSMT_UNFIN_SQFT", "SA_CONDITION_CODE",
"SA_CONSTRUCTION_CODE", "SA_CONSTRUCTION_QLTY", "SA_COOL_CODE",
"SA_EXTERIOR_1_CODE", "SA_FIN_SQFT_1", "SA_FIN_SQFT_2", "SA_FIN_SQFT_3",
"SA_FIN_SQFT_4", "SA_FIN_SQFT_TOT", "SA_FIREPLACE_CODE",
"SA_FOUNDATION_CODE", "SA_GARAGE_CARPORT", "SA_GRG_1_CODE",
"SA_GRG_SQFT_1", "SA_HEAT_CODE", "SA_HEAT_SRC_FUEL_CODE",
"SA_LOT_DEPTH", "SA_LOT_WIDTH", "SA_LOTSIZE", "SA_NBR_BATH",
"SA_NBR_BATH_1QTR", "SA_NBR_BATH_HALF", "SA_NBR_BATH_3QTR",
"SA_NBR_BATH_FULL", "SA_NBR_BATH_BSMT_HALF", "SA_NBR_BATH_BSMT_FULL",
"SA_NBR_BATH_DQ", "SA_NBR_BEDRMS", "SA_NBR_RMS", "SA_NBR_STORIES",
"SA_NBR_UNITS", "SA_PATIO_PORCH_CODE", "SA_POOL_CODE",
"SA_PRIVACY_CODE", "SA_ROOF_CODE", "SA_SQFT", "SA_SQFT_ASSR_TOT",
"SA_SQFT_DQ", "SA_STRUCTURE_CODE", "SA_STRUCTURE_NBR", "SA_VIEW_CODE",
"SA_YR_BLT", "SA_YR_BLT_EFFECT", "SR_UNIQUE_ID", "SR_UNIQUE_ID_NOVAL",
"SA_DATE_TRANSFER", "SA_VAL_TRANSFER", "SA_DOC_NBR_FMT",
"SA_DATE_NOVAL_TRANSFER", "SA_DOC_NBR_NOVAL", "PROCESS_ID",
"SA_X_COORD", "SA_Y_COORD", "SA_GEO_QLTY_CODE", "SA_CENSUS_TRACT",
"SA_CENSUS_BLOCK_GROUP", "CORE_BASED_STATISTICAL_AREA_CODE",
"MINOR_CIVIL_DIVISION_CODE", "FIPS_PLACE_CODE",
"SA_INACTIVE_PARCEL_FLAG", "SA_SHELL_PARCEL_FLAG", "UCB_GEO_ID"]
# final FILLER field not in the tab-delimited files
# add ucb_geo_id as final field

field_types = ["int", "int", "varchar", "varchar", "tinyint", "smallint", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "smallint",
"smallint", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "int", "smallint", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "int", "smallint", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar", "int",
"varchar", "varchar", "varchar", "varchar", "varchar", "int", "int",
"int", "numeric", "smallint", "smallint", "int", "int", "int",
"numeric", "int", "int", "int", "numeric", "varchar", "int", "varchar",
"int", "varchar", "int", "varchar", "int", "varchar", "int", "varchar",
"int", "int", "int", "varchar", "numeric", "smallint", "datetime",
"datetime", "smallint", "varchar", "smallint", "varchar", "varchar",
"smallint", "varchar", "smallint", "smallint", "numeric", "varchar",
"numeric", "varchar", "varchar", "int", "int", "int", "int", "int",
"varchar", "varchar", "varchar", "varchar", "smallint", "varchar",
"varchar", "smallint", "smallint", "numeric", "numeric", "smallint",
"smallint", "smallint", "smallint", "smallint", "smallint", "numeric",
"smallint", "smallint", "tinyint", "smallint", "varchar", "varchar",
"varchar", "varchar", "int", "int", "int", "varchar", "smallint",
"varchar", "smallint", "smallint", "int", "int", "int", "int",
"varchar", "int", "varchar", "int", "numeric", "numeric", "varchar",
"varchar", "varchar", "varchar", "varchar", "varchar", "varchar",
"varchar", "varchar"]

# Replace SQL Server types with Postgres types as needed
for i, t in enumerate(field_types):

	if (t == 'tinyint'):
		field_types[i] = 'smallint'

	if (t == 'datetime'):
		field_types[i] = 'timestamp'
		
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
cur.execute("CREATE TABLE master.assessor (" + field_defs +
			", CONSTRAINT assessor_pkey PRIMARY KEY (sa_property_id));")
cur.execute("GRANT SELECT ON TABLE master.assessor TO dataquick_user;")
conn.commit()

path = '/home/maurer/Dataquick/Assessor_tab_dlm/'
table = 'master.assessor'


# Load data into Postgres

t0 = time.time()
count = 0
N = 100 # set for testing only

for fnum in range(1,16):
	zname = 'ARB_ASSR_' + str(fnum).zfill(2) + '.zip'
	fname = 'ARB_ASSR_' + str(fnum).zfill(2) + '.txt'
	
	with zipfile.ZipFile(path+zname) as z:
		with z.open(fname) as f:
			for line in f:
			#for i in range(N):
				#line = f.readline()

				# split by tabs, remove trailing spaces and final EOL value
				arr = [x.rstrip(' ') for x in line.split('\t')][:-1]
				values = ''
				for i in range(len(fields)-1): # subtract 1 for geo_id
					val = arr[i]

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
					
				# if not adding geo_id, need to remove trailing punctuation
				geo_id = str(arr[4]).zfill(2) + str(arr[5]).zfill(3) + arr[182]
				values = values + "'" + geo_id + "'"
					
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
cur.execute("SELECT count(sa_property_id) FROM " + table)
print "rows //", cur.fetchone()[0]
print "hours //", round((time.time() - t0)*1.0/60/60, 2)
print "seconds //", int(time.time()-t0)


# Add indexes

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX assessor_fips_index ON master.assessor " +
			"USING btree (mm_fips_muni_code);")
conn.commit()
print "assessor_fips_index", round(time.time() - t0)

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX assessor_tract_index ON master.assessor " +
			"USING btree (sa_census_tract);")
conn.commit()
print "assessor_tract_index", round(time.time() - t0)

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX assessor_property_index ON master.assessor " +
			"USING btree (sa_property_id);")
conn.commit()
print "assessor_property_index", round(time.time() - t0)

t0 = time.time()
conn.commit()
cur.execute("CREATE INDEX assessor_geo_index ON master.assessor " +
			"USING btree (ucb_geo_id);")
conn.commit()
print "assessor_geo_index", round(time.time() - t0)
