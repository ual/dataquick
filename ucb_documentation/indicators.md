indicators
==========

Documentation of tract-level indicators

#### Contents

• Output  
• General to-do items  
A. Number of properties by type  
B. Number of sales  
C. Median sale price  
D. Ratio of improvement value to land value  
E. Median square footage, number of rooms and bedrooms  
F. Absentee ownership  
G. Property flips  
H. Use conversions  
I. New construction


==========
#### Output

• Indicators are saved as CSV files with one row per census tract  
• File names include the date produced as a versioning mechanism  
• Census tract identifier is the GeoID, which is a concatenation of state, county, and tract id's (census tract id's are not unique between counties)  

**Master copy of output files:**  
https://github.com/ual/dataquick/tree/master/indicator_output  
(to download, click on a file name, then "raw", then save it)

**Code used to generate output files:**  
https://github.com/ual/dataquick/tree/master/maurer_code  
https://github.com/ual/dataquick/tree/master/blanchard_code


==========
#### General to-do items

• Are the Dataquick census tract assignments correct?  
• What are the reporting dates for the annual assessor snapshots?  
• Do assessor tables include block groups? They're in the data dictionary


==========
#### A. Number of properties by type

Based on Dataquick standard use code (`use_code_std`) in assessor tables. All codes have four characters, with the first character indicating the broad land use category (commercial, industrial, residential, etc) and the remainder specifying the sub-category. 

Count the properties in each broad use category, then count them a second time by sub-category. Do for each year if possible, or else 2004, 2006, 2010, 2014.

**Output**  
• Output is in `stats_use_code_current_20141017.csv`  
• Geo_id with only state and county means the tract id was missing from dataquick  
• One column for each broad use cateogry, then for each sub-category  
• The use code definitions are here: [USE_CODES.xls](https://github.com/ual/dataquick/blob/master/vendor_documentation/data_dictionary/USE_CODES.xls])  
• A missing column means the category was not used in the bay area  
• The 'R---' subcategories should add up to the 'R' total, and so forth  
• Code is in `stats_use_code_current.py`

**Update 11-02-2014**  
• Updated `stats_use_code_current_20141102.csv` to clarify that col 2 is the count of missing use codes  
• Created `stats_use_code_hist_20141102.csv` with yearly counts of the broad use categories (C, R, etc) from the assessor history table  
• One row per bay area census tract, labeled with geo_id  
• For years with multiple updates in the history table, I used the first one (`ah_history_yr_version = 1`)  
• Code is in `stats_use_code_hist.py`  

Tallying the detailed use codes would be an easy extension, but it would create quite a large spreadsheet (~80 codes x 10 years = 800 columns) -- so if this is needed let's plan out what specific format is most useful.

**Next steps**  
• None


==========
#### B. Number of sales

For residential and commercial properties separately. Filter for arms-length transactions. 

**Output**  
• Output is in `stats_sales_residential_20141017.csv` and `stats_sales_commercial_20141017.csv`  
• One row for each bay area geo_id with relevant sale transactions  
• One column for each calendar year from 1988 to 2014 (sales through 6/2014)  
• Values are the count of residential or commercial sale transactions in a given year  
• Sales are filtered for `sr_arms_length_flag = 1`  
• Sales are filtered for the first character of `use_code_std` being `R` or `C`  
• Code is in `stats_sales_residential.py` and `stats_sales_commercial.py`

**Update 1-14-2015**  
• Updated `stats_sales_residential_20150114.csv` based on the new, more thorough data cleaning

**Next steps**  
• None


==========
#### C. Median sale price

Use transfer value field (`sr_val_transfer`) in sales table. Filter for arms-length transactions. Calculate for residential and commercial properties separately. Unit is price per square foot (square footage is in the assessor table). 

Structures are changed over time, especially prior to sales, so the best way to get an accurate square footage is probably to match sale data to the assessor data from the following year. The 2004 assessor data will have to be used for all sales from 1988-2004. 

Adjust for constant dollars using national headline CPI. 
http://www.bls.gov/data/inflation_calculator.htm

**Output**  
`price_sqft_v2.csv`

This is a good first pass but needs to be updated. Includes median residential sale price for 2004 and 2014, plus proportional appreciation rate (calculated from the medians). Filtered for arms-length transactions, non-zero sale price, non-missing square footage, non-missing use code.

**Update 11-02-2014**  
• Output is in `stats_sale_price_hist.csv`  
• One row per census tract, with columns for 1988 through 2014 sales  
• `YYYY_price_sqft` column = median sale price per sqft for residential properties  
• `YYYY_count` column = count of the sales that went into the calculation  

• Prices are indexed to 2014 dollars using national headline CPI  
• Only arms-length, non-zero-value sale transactions are included (`sr_arms_length_flag = 1`, `sr_val_transfer > 0`)  
• Square footage comes from the *following year's* assessor table (with the exception of pre-2003 sales which are matched to 2004 square footage, and 2013-14 sales which are matched to the latest square footage on file)  
• The census tract id is only in the current assessor table, so in order to get census-tract-level stats we have to exclude sales of properties that no longer exist  
• Because early use code data is spotty, I used the *current* use code to filter for residential properties (if this seems like a problem we can do something more subtle)  
• Some counties are missing from these stats in 2011 or 2012 because Dataquick didn't provide complete assessor history updates. We can match those sales to earlier or later square footage on a per-county basis if needed.  
• Code is in `stats_sale_price_hist.py`  

**Update 12-06-2014**  
• Output is in `stats_price_singlefam_20141206.csv` and `_multifam_`  
• This update removes multi-property transactions, shifts to using the current assessor table for use codes and square footage, and divides results into single-family and multifamily tables  

• We found that multi-property transactions (often condo building or subdivision sales) frequently have incorrect price or square footage data because of how the information is provided to Dataquick  
• These transactions can be identified by duplicate `sr_doc_nbr_fmt` entries on a single day in a single county (after removing non-arms-length transactions)  
• We also found that idiosyncratic errors result in 1% to 10% of existing properties being missing in each historical assessor table, but present in the "current" table  
• Matching transactions to the current rather than contemporaneous assessor table (for use code and square footage) substantially increases our data coverage, although it presumably introduces occasional errors as well  

**Update 1-14-2015**  
• Updated `stats_sales_residential_20150114.csv` and `_multifam_`  
• Input reflects the new, more thorough data cleaning  
• Prices are now indexed to 2010 dollars  

**Next steps**  
• Repeat using panel methodology for individual properties?


==========
#### D. Ratio of improvement value to land value

Use assessment value fields in the assessor tables. Filter for properties that were sold in the prior calendar year to ensure that appraised values are current. Calculate annually, or use 2004, 2006, 2010, 2014 if that's too much. Commercial as well as residential. 

**Output**  
• Output is in `stats_improvement_current_20141017.csv`  
• `res_imprv_pct_median` = median portion of assessed value allocated to improvements, for residential properties  
• `res_imprv_pct_stdev` = standard deviation, to indicate dispersion in underlying values  
• `res_count` = count of applicable properties for each tract  
• The `com_` fields are analogous for commercial properties  
• Improvement portions are from the `sa_imprv_pct` field in current assessor table  
• Filtered for properties sold in 2012, but only if the sales were arms-length (`sr_arms_length_flag = 1`)

Based on these figures plus a quick look at the underlying data, here's how counties seem to be calculating improvement value:

• Alameda - usually 70% of total value  
• Contra Costa - precise numbers, wide variety  
• Marin - precise numbers, wide variety  
• Napa - precise numbers, wide variety  
• San Francisco - round numbers, wide variety  
• San Mateo - usually 50%  
• Santa Clara - round numbers, wide variety  
• Solano - precise numbers but all close to 75%  
• Sonoma - usually 60%

**Next steps**  
• Take a look at the data quality and decide whether to repeat calculations for the historical assessor table


==========
#### E. Median square footage, number of rooms, and bedrooms

For all residential properties. And separately for only properties that were sold. Match sales to subsequent assessor year. 

**Output**  
• Output is in `stats_sqft_rooms_current_20141018.csv`  
• `sqft_median` = median square footage of residential properties in the geo_id  
• `sqft_count` = number of properties in above calculation (other count fields are analogous)  
• `rooms_median`, `bedrms_median` = median number of rooms, bedrooms per residential property in geo_id  
• `sqft_median_2012_sales` = median square footage of residential properties sold in 2012  
• Other `_2012_sales` fields are analogous  
• Current assessor data is from 2013 or 2014, so the 2012 sales cohort is the last one guaranteed to have its stats updated in the current table  
• All medians and counts exclude zero or missing values (which is why the counts vary between fields)  
• Square footage is from the `sa_sqft` field in the assessor table  
• Rooms and bedrooms are from the `sa_nbr_rms` and `sa_nbr_bedrms` fields  
• Sale dates are from the `sr_date_transfer` field in the sales table  
• Sales are filtered for `sr_arms_length_flag = 1`  
• Code is in `stats_sqft_rooms_current.py`

**Next steps**  
• Repeat using the panel methodology so that we capture additions to existing properties rather than new construction  


==========
#### F. Absentee ownership

For all residential properties. Start with `sa_site_mail_same` field from current and historical assessor tables. 

**Output**  
• Output is in `stats_absentee_current_20141017.csv`  
• Absentee ownership rating is from the `sa_site_mail_same` field from the current assessor table  
• Columns are `Y` for yes, `N` for no, and `U` for undetermined (these are direct values from Dataquick, and the data dictionary doesn't specify what exactly `U` means)  
• Data values are the counts of properties matching each category  
• Code is in `stats_absentee_current.py`

**Update 11-02-2014**  
• Added `stats_absentee_hist.csv` based on the historical assessor table  
• One row per census tract, set of 3 columns for each year 2004-2014  
• 2004-05 counts are low because the use codes are mostly missing  
• For years with multiple updates, I used the first one (`ah_history_yr_version = 1`)  
• Code is in `stats_absentee_hist.py`  

**Next steps**  
• None


==========
#### G. Property flips

Count of residential properties that were sold 2 or more times within 2 years. Filter for arms-length transactions.  

**Output**  
• Output is in `stats_flips_20150127.csv` based on the new, more thorough data cleaning removing same day transactions
• Based on `sr_date_transfer` field in sales table  
• One column per year from 1988 to 2014  
• Values are the count of 2 or more residential property sale transactions that took place within 2 years for the year of transaction  
• Code is in `stats_flips_hist.py`  

**Next steps**  
• None

==========
#### H. Use conversions

Count of specific 4 digit residential to residential use code changes and broad use code changes for every use code to every use code for each year. This includes condo conversions, residential to commercial, multifamily to single family, rental to ownership. Filter for parcel update history version 1.

**Output**  
• Output for 4 digit residential to residential is in `stats_usechange_R4digit_20141207.csv`  
• Output for broad use code changes is in `stats_usechange_broad_20141207.csv`  
• Based on `use_code_std` field in assessor table  
• One column per use code type change and year from 2006 to 2011  
• Values are the count of residential properties that have changed the specified use code from one year to the next  
• Code is in `stats_usecode_hist.py`  

**Next steps**  
• None

==========
#### I. New residential construction

Assessor tables include a year built field.

**Output**  
• Output is in `stats_construction_20141017.csv`  
• Based on `sa_yr_blt` field in current assessor table  
• One column per year from 1988 to 2014 (through 6/2014)  
• Values are the count of currently standing residential properties that were built in each year  
• Code is in `stats_construction.py`

**Update 11-03-2014**  
• Added columns for all years going back to the earliest recorded construction  
• Years with no construction in any census tract are skipped  
• Output is in `stats_construction_20141103.csv`  

**Next steps**  
• None


