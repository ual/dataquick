### Created by Sam Blanchard - November 2014
### Total script run time on server machine ~90 min for each usecode stats table
### Script to count number the of parcel use code changes in historical (assessor) dataquick database.
### Use code change = properties that have a different land use code from year to year. Filter parcel update history version 1.
### Note: Do not run this script on local machine, instead run on server due to memory limitations on local machines.
### Note: does not give count of prop id change which can denote conversions.

##########################################
##Import required libraries
import psycopg2
import numpy as np
import time
import pandas
import datetime
##########################################

##########################################
# Connect to the database
conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_user' password='ucbdq'"
conn = psycopg2.connect(conn_string) # Connect
cur = conn.cursor() # Define cursor

# Define SQL selection query
t0 = time.time() #Start time index
##Note: For testing it is suggested to use only 1 county due to memory requirements on local machines

## Note: Use the below SQL code for broad use code changes for every use code to every use code
#cur.execute("""SELECT assessor.ucb_geo_id, ahist.use_code_std, ahist.sa_property_id, ahist.ah_history_yr, ahist.sa_parcel_nbr_primary, ahist.sa_parcel_nbr_previous FROM master.ahist LEFT JOIN master.assessor ON assessor.sa_property_id = ahist.sa_property_id WHERE assessor.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97) AND ahist.ah_history_yr_version = '1' AND (ahist.ah_history_yr >= 2006 AND ahist.ah_history_yr <= 2011); """)

## Note: Use the below SQL code for only specific 4 digit residential to residential use code changes
cur.execute("""SELECT assessor.ucb_geo_id, ahist.use_code_std, ahist.sa_property_id, ahist.ah_history_yr, ahist.sa_parcel_nbr_primary, ahist.sa_parcel_nbr_previous FROM master.ahist LEFT JOIN master.assessor ON assessor.sa_property_id = ahist.sa_property_id WHERE assessor.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97) AND (substring(ahist.use_code_std from 1 for 1) = 'R') AND ahist.ah_history_yr_version = '1' AND (ahist.ah_history_yr >= 2006 AND ahist.ah_history_yr <= 2011); """)

out = cur.fetchall() #Set returned queried data to 'out' dataframe
print int(time.time()-t0), 'sec. for postgres' #End time index
print 'postgres selection complete'
##Note: Takes about 6.5 min to run
##########################################

##########################################
##Set arrays
t0 = time.time() #Start time index
geo = np.array([r[0] for r in out]) #Create array for all rows in out for column 0
yr = np.array([r[3] for r in out])
use = np.array([r[1] for r in out])
broad_use = np.array([r[1][0] for r in out])
print 'geo, year, use arrays done'

##Set lists and filters
#List of unique FIPS codes
geo_list = np.unique(geo).tolist()#list of keys
geo_fltr = {g: (geo==g) for g in geo_list}#
print 'geo list done'

#List of transaction years
yr_list = range(2006, 2012)
yr_fltr = {y: (yr==y) for y in yr_list}
print 'year list done'

#List of unique FIPS codes

##When doing only specific 4 digit residential to residential use code changes use: "use"
##When doing broad use code changes for every use code to every use code use: "broad_use"
#List of use codes
use_list = np.unique(use).tolist()#list of keys
use_fltr = {u: (use==u) for u in use_list}

use_combos = [] #Create empty container to store use_combos

#Create list of all possible combinations of usecode to usecode
for u1 in use_list:
    for u2 in use_list:
        if u1 != u2: #If use code 1 does not equal use code 2 then
            use_combos.append(u1 + "_" + u2) # Create label: usecode1_usecode2

year_use_combos = [] #Create empty container to store year and use_combos

#Create list of all use code combinations produced above and all years
for u in use_combos:
    for y2 in yr_list:
            year_use_combos.append(u + "_" + str(y2)) #append use code combination to year. Force y2 to be string

print 'use code combination and year list done'
print int(time.time()-t0), 'sec. for arrays, lists, and filters' #End time index
##########################################

##########################################
##Create pandas dataframe to hold 'out' data
t0 = time.time()
df = pandas.DataFrame(out)

#Set labels for field names
df.columns = ['ucb_geo_id', 'use_code_std', 'sa_property_id', 'ah_history_yr','sa_parcel_nbr_primary','sa_parcel_nbr_previous'] #set lables for field names
print 'data frame complete'
print int(time.time()-t0), 'sec. for pandas'
##########################################

##########################################
t0 = time.time()
#Define function to generate count of property ids that have a transaction year within two consecutive years of each other
def stats(records, geography):
    year_use_combo_counts = pandas.Series([str(geography)] + [0 for x in year_use_combos], index = ['geo_id'] + year_use_combos) # Create index of years in list. ie series = indexed array. Location where counts are stored based on use code and year column labels previously defined in lists
    correct_geo = records[records["ucb_geo_id"] == geography] # Filter records by geoid, iterating through geolist
    property_groups = correct_geo.groupby("sa_property_id") # Group by unique property_ids and send each unique group to a new dataframe
    relevant_groups = property_groups.size()[property_groups.size() >= 2].keys() # Subset unique property ids to only those where there are >= 2. Where keys are the id, value is the size of group ie number of records or number of ids for unique ids
    count = 0 #reset count to 0
    for property_id in relevant_groups: # Iterate through unique property_ids within relevant_groups dataframe
        group = property_groups.get_group(property_id) # 'get_group' = force getting records for group
        group = group.sort('ah_history_yr')# Sort ascending by year for unique property ids
        i = 0 #Reset index to 0
        try: #for error debugging- if no error then do:
            while i < len(group) - 1: # If "while" the number of props are > 0 then count the number of props. '-1' accounts for index starting at 0
                usecode1 = group.iloc[i]['use_code_std'] #define usecode at time 1
                usecode2 = group.iloc[i + 1]['use_code_std'] #define usecode at time 2
                year = group.iloc[i + 1]['ah_history_yr'] #define year of time 2 to use for label
                if usecode1 <> usecode2: #if usecode time 1 is not equal to usecode time 1 then count
                    year_use_combo_counts.at[usecode1 + '_' + usecode2 + '_' + str(year)] += 1 #count usecode change and place in column based on usecode change combos and year
                i += 1 #incremement through index of groups
        except: #for error debugging- if error then do:
            print year_use_combo_counts.at[usecode1 + '_' + usecode2 + '_' + str(year)] #prints use code combo and year where error has occured
    print (geography) # Print FIPS code currently iterating through to give indication of progress
    return year_use_combo_counts # return the count of usecode changes
##########################################

##########################################
##Run function above
table = [stats(df,g) for g in geo_list] # Run 'stats' function defined above with dataframe 'df' as records for each unique FIPS code in geo_list as an iterating variable
print 'Count table function complete'
print int(time.time()-t0), 'sec. for count' #End time index
##########################################

##########################################
#Set output CSV path and filename
t0 = time.time()
outpath = 'C:/Users/Work/Desktop/Data/' #Output CSV path
today = datetime.date.today() #Todays run date
today_str = today.strftime('%Y%m%d') #Convert date format to string in format yearmonthday
##Change file name here as needed for R 4 digit or broad stats tables
#outfilename = 'stats_usechange_broad_' + today_str + '.csv'
outfilename = 'stats_usechange_R4digit_' + today_str + '.csv' #Output CSV file name with todays run date
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
##########################################
#Check sql code for fips and compare with output count:
#SELECT assessor.ucb_geo_id, ahist.use_code_std, ahist.sa_property_id, ahist.ah_history_yr, ahist.sa_parcel_nbr_primary, ahist.sa_parcel_nbr_previous FROM master.ahist LEFT JOIN master.assessor ON assessor.sa_property_id = ahist.sa_property_id WHERE  ucb_geo_id = '06001400300' AND assessor.mm_fips_muni_code IN (1) AND (substring(ahist.use_code_std from 1 for 1) = 'R') AND ahist.ah_history_yr_version = '1' AND (ahist.ah_history_yr >= 2006 OR ahist.ah_history_yr <= 2011) order by sa_property_id ASC, ah_history_yr ASC;

#Can also use 06001400300
##########################################