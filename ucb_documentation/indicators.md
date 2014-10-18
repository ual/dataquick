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
• File names should  include the date produced as a versioning mechanism  
• Census tract identifier should be the GeoID, which is a concatenation of state, county, and tract id's (census tract id's are not unique between counties)  
• For aggregate statistics like medians, it's helpful to include a separate field with the count of applicable records from each census tract

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

**Next steps**  
• Repeat for each year in the historical assessor table


==========
#### B. Number of sales

For residential and commercial properties separately. Filter for arms-length transactions. Look at each year since 1988, or start with 2004, 2006, 2010, 2014 if simpler.

**Output**  
• Output is in `stats_sales_residential_20141017.csv` and `stats_sales_commercial_20141017.csv`  
• One row for each bay area geo_id with relevant sale transactions  
• One column for each calendar year from 1988 to 2014 (sales through 6/2014)  
• Values are the count of residential or commercial sale transactions in a given year  
• Sales are filtered for `sr_arms_length_flag = 1`  
• Sales are filtered for the first character of `use_code_std` being `R` or `C`  
• Code is in `stats_sales_residential.py` and `stats_sales_commercial.py`

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

**Next steps**  
• Replace tract id with GeoID  
• Calculate for all years  
• Add commercial properties  
• Adjust prices for inflation  
• Can we do time-series analysis of individual properties?


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
• Repeat for each year in the historical assessor table


==========
#### E. Median square footage, number of rooms, and bedrooms

For all residential properties. And separately for only properties that were sold. Match sales to subsequent assessor year. 

**Output**  
• Output is in `stats_sqft_rooms_current_20141017.csv`  
• `sqft_median` = median square footage of residential properties in the geo_id  
• `sqft_count` = number of properties in above calculation (other count fields are analogous)  
• `rooms_median`, `bedrms_median` = median number of rooms, bedrooms per residential property in geo_id  
• `sqft_median_2012_sales` = median square footage of residential properties sold in 2012  
• Other `_2012_sales` fields are analogous  
• Current assessor data is from 2013 or 2014, so the 2012 sales cohort is the last one guaranteed to have its stats updated in the current table  
• All medians and counts exclude zero or missing values (which is why the counts vary between fields)  
• Square footage is from the `sa_sqft` field in the assessor table  
• Rooms and bedrooms are from the `sa_nbr_rms` and `sa_nbr_bedrms` fields  
• Sale dates are from the `sa_date_transfer` field in the assessor table  
• Code is in `stats_sqft_rooms_current.py`

**Next steps**  
• Repeat for each year in the historical assessor table  
• We should confirm that `sa_date_transfer` in the assessor table excludes non-arms-length transactions


==========
#### F. Absentee ownership

For all residential properties in 2004 and 2014, plus percent change. Start with `sa_site_mail_same` field from current and historical assessor tables. 

**Output**  
• Output is in `stats_absentee_current_20141017.csv`  
• Absentee ownership rating is from the `sa_site_mail_same` field from the current assessor table  
• Columns are `Y` for yes, `N` for no, and `U` for undetermined  
• Data values are the counts of properties matching each category  
• Code is in `stats_absentee_current.py`

**Next steps**  
• Repeat for each year in the historical assessor data


==========
#### G. Property flips

Count of properties that were sold 2 or more times within 2 years. Filter for arms-length transactions.

**Output**

**Next steps**


==========
#### H. Use conversions

We're interested in condo conversions, residential to commercial, multifamily to single family, rental to ownership. 

**Output**

**Next steps**


==========
#### I. New residential construction

Assessor tables include a year built field.

**Output**  
• Output is in `stats_construction_20141017.csv`  
• Based on `sa_yr_blt` field in current assessor table  
• One column per year from 1988 to 2014 (through 6/2014)  
• Values are the count of currently standing residential properties that were built in each year  
• Code is in `stats_construction.py`

**Next steps**  
• None


