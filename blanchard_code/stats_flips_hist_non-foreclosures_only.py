### Created by Sam Blanchard - October 2014
### Total script run time on local machine ~30 min
### Script to count number of property flips in historical (assessor) dataquick database.
### Flips = properties that have a transaction sale date within 2 or less years. Filter for arms-length transactions.

##########################################
##Import required libraries
import psycopg2 #required for postgres database connection and selection query
import numpy as np
import time
import pandas
import datetime
from datetime import date #required to convert field to date format
from datetime import timedelta
##########################################

##########################################
##Connect to the database
conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string) # Connect
cur = conn.cursor() # Define cursor

##Define SQL selection query
t0 = time.time() #Start time index
#cur.execute("""SELECT ucb_geo_id, sr_date_transfer, (sr_date_transfer/10000) AS sr_year, sr_property_id FROM master.sales_clean_res; """)
cur.execute("""SELECT s.ucb_geo_id, s.sr_date_transfer, (s.sr_date_transfer/10000) AS sr_year, s.sr_property_id FROM master.sales_clean_res as s left outer join master.foreclosure as f on s.sr_property_id = f.sa_property_id where f.sa_property_id is null; """) # selects records in master.sales_clean_res that are not in the master.foreclosure table by selecting records that do not join to the two tables
out = cur.fetchall() #Set returned queried data to 'out' dataframe
print int(time.time()-t0), 'sec. for postgres' #End time index
print 'postgres selection complete'
##########################################

##########################################
##Set arrays
t0 = time.time() #Start time index
geo = np.array([r[0] for r in out]) #Create array for all rows in out for column 0
yr = np.array([r[1] for r in out])
print 'geo and year arrays done'

##Set lists and filters
#List of unique FIPS codes
geo_list = np.unique(geo).tolist()#list of keys
geo_fltr = {g: (geo==g) for g in geo_list}#
print 'geo list done'

#List of transaction years
yr_list = range(1988, 2015)
yr_fltr = {y: (yr==y) for y in yr_list}
print 'year list done'
print int(time.time()-t0), 'sec. for arrays, lists, and filters' #End time index
##########################################

##########################################
##Create pandas dataframe to hold 'out' data
t0 = time.time()
df = pandas.DataFrame(out)

#Set labels for field names
df.columns = ['ucb_geo_id', 'sr_date_transfer', 'sr_year', 'sr_property_id']

print 'data frame complete'
print int(time.time()-t0), 'sec. for pandas'
##########################################

##########################################
##Transform sr_date_transfer to proper format for date to compute time difference in count function
t0 = time.time()
#Convert integer sr_date_transfer to string sr_date_transfer_v2
df['sr_date_transfer_v2'] = df['sr_date_transfer'].astype(str)
print 'transfer date converted to string'

#Parse string sr_date_transfer field into 3 date components (year,month,day) needed for date conversion function
y = df['sr_date_transfer_v2'].str[0:4] #year at 0-3 position in string
m = df['sr_date_transfer_v2'].str[4:6] #month at 4-5 position in string
d = df['sr_date_transfer_v2'].str[6:8] #day at 6-8 position in string

#Convert year, month, day components created above to integer - needed for date function
y2 = map(int, y.values) #map computes function 'int' - convert each y value to integer - for all values in variable
m2 = map(int, m.values)
d2 = map(int, d.values)

##Run a series of tests to check potential issues with month that may lead to date conversion failure

#Test month variable to make sure all values are a proper month value <= 12
#Do true/false test to see if records in month field are incorrect > 12
print any([m2[i] > 12 for i in range(len(m2))]), '= there are records in the month field that are incorrect > 12'
#Convert m2 to an array m3 for further testing
m3 = np.array(m2)
#Test length of sr_date_transfer_v2 field to ensure it is only 8 characters
print np.unique([len(x) for x in df['sr_date_transfer_v2'].astype(str).values]), 'is the length of the sr_date_transfer_v2 field' #checks and prints all the unique lengths of the field
#Count number of records that have incorrect month value > 12
print len(m3[m3 > 12]), 'records have an incorrect month value that is > 12' #print count of records that have a incorrect month value of > 12
#Show the values of month that are incorrect > 12
print (m3[m3 > 12]), 'are the incorrect values in month that are > 12'
print 'month field tests complete'

##Remove incorrect month value '92' from month and create corrected dataframe for date function
#Create new dataframe to hold corrected date field
year_month_day = pandas.DataFrame({'year':y2, 'month':m2, 'day':d2}) #create dataframe with data from year, month, day fields with given labels
year_month_day = year_month_day[year_month_day['month'] != 92].copy() #recreate dataframe only with values that are not equal to the incorrect value '92'
print 'year_month_day dataframe created'

#Convert date fields to string and print date field data types
for x in ['year','month','day']:
    year_month_day[x] = year_month_day[x].astype(str)
print year_month_day.dtypes

#Make year, month, day fields a list
y = year_month_day['year'].tolist()
m = year_month_day['month'].tolist()
d = year_month_day['day'].tolist()

#Convert year, month, day fields to integer required for date function
y2 = map(int, y)
m2 = map(int, m)
d2 = map(int, d)
#print ([type(x) for x in y2[:5]]) #test to make sure fields converted to integer
#Do true/false test to see if records in month field are incorrect > 12
print any([m2[i] > 12 for i in range(len(m2))]), '= there are records in the month field that are incorrect > 12'

##Run date format conversion using required format Y, M, D for all values in list
date = [datetime.date(y2[i], m2[i], d2[i]) for i in range(len(y2))] #datetime.date is the date format conversion function
print 'datetime field created'

#Remove incorrect month value '92' from dataframe
df2 = df[df['sr_date_transfer_v2'].str[4:6] != '92'].copy()
#Create new field 'datetime' that holds the date formatted transaction date
df2['datetime'] = date
print 'date conversion and cleaning complete'
print int(time.time()-t0), 'sec. for date conversion and cleaning'
##########################################

##########################################
t0 = time.time()
#Define function to generate count of property ids that have a transaction year within two consecutive years of each other
def stats(records, geography):
    year_counts = pandas.Series([str(geography)] + [0 for x in yr_list], index = ['geo_id'] + yr_list) # Create index of years in list. ie series = indexed array
    correct_geo = records[records["ucb_geo_id"] == geography] # Filter records by geoid, iterating through geolist
    property_groups = correct_geo.groupby("sr_property_id") # Group by unique property_ids and send each unique group to a new dataframe
    relevant_groups = property_groups.size()[property_groups.size() >= 2].keys() # Subset unique property ids to only those where there are >= 2. Where keys are the id, value is the size of group ie number of records or number of ids for unique ids
    count = 0 #reset count to 0
    for property_id in relevant_groups: # Iterate through unique property_ids within relevant_groups dataframe
        group = property_groups.get_group(property_id) # 'get_group' = force getting records for group
        group = group.sort('datetime')# Sort ascending by transaction date for unique property ids
        i = 0 #Reset index to 0
        while i < len(group) - 1: # If "while" the number of transaction dates are > 0 then count the number of transactions. '-1' accounts for index starting at 0
            if group.iloc[i + 1]['datetime'] - group.iloc[i]['datetime'] <= datetime.timedelta(365): # If the number of years is <= 1 year (365 days) then count. 'datetime' is a datetime object and by default is in units days. By default subtracting two datetime objects results in a datetime object 'datetime.timedelta' which is then compared to the value specified in the () in this case 730 days. Note: Resulting timedelta value is always negative if difference is being calculated between early date - later date or is positive if difference is between later date - early date. Change to 1 to see transaction occurring in 1 day.
                # listname.append
                year_counts.at[group.iloc[i + 1]['datetime'].year] += 1 # Increment count by 1 iterating years
            i += 1 #incremement through index of groups
    print (geography) # Print FIPS code currently iterating through to give indication of progress
    return year_counts # return the count of flips
##########################################

##########################################
##Run function above
table = [stats(df2,g) for g in geo_list] # Run 'stats' function defined above with dataframe 'df' as records for each unique FIPS code in geo_list as an iterating variable
print 'Count table function complete'
print int(time.time()-t0), 'sec. for count' #End time index ---Takes about 21 min to run
##########################################

##########################################
#Set output CSV path and filename
t0 = time.time()
outpath = 'C:/Users/Work/Desktop/Data/' #Output CSV path
today = datetime.date.today() #Todays run date
today_str = today.strftime('%Y%m%d') #Convert date format to string in format yearmonthday
outfilename = 'stats_flips_' + today_str + '.csv' #Output CSV file name with todays run date
outfile = outpath + outfilename #Full path and file name of export CSV file
##########################################

##########################################
out_df = pandas.DataFrame(table) #Make count output 'table' a new dataframe
out_df.to_csv(outfile,index=False) #export dataframe to CSV file. Do not output index column.
print 'CSV successfully created:' + (outfile)
print int(time.time()-t0), 'sec. for table export' #End time index
print 'Script complete'
##########################################

##########################################
##Scratch code:
#Check sql code for fips and compare with output count:
#SELECT ucb_geo_id, (sr_date_transfer/10000) AS sr_year, sr_date_transfer, sr_property_id FROM master.sales LEFT JOIN master.assessor ON sa_property_id = sr_property_id WHERE ucb_geo_id = '06001422600' AND sales.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97) AND substring(use_code_std from 1 for 1) = 'R' AND sr_arms_length_flag = '1' AND (sr_date_transfer/10000) >= 1988 AND (sr_date_transfer/10000) <= 2014 order by sr_property_id ASC, sr_year ASC, sr_date_transfer ASC;
#Can also use 06075033201 (should have 1), 06013450300 (should have 3), or 06001422600 (should have 0)
##########################################