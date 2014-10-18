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
E. Median square footage  
F. Median number of rooms and bedrooms  
G. Absentee ownership  
H. Property flips  
I. Use conversions  
J. New construction


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
• output is in `stats_use_code_current_20141017.csv`  
• geo_id with only state and county means the tract id was missing from dataquick  
• one column for each broad use cateogry, then for each sub-category  
• the use code definitions are here: [USE_CODES.xls](https://github.com/ual/dataquick/blob/master/vendor_documentation/data_dictionary/USE_CODES.xls])  
• a missing column means the category was not used in the bay area  
• the 'R---' subcategories should add up to the 'R' total, and so forth  
• code is in `stats_use_code_current.py`

**Next steps**  
• Repeat for each year in the historical assessor table


==========
#### B. Number of sales

For residential and commercial properties separately. Filter for arms-length transactions. Look at each year since 1988, or start with 2004, 2006, 2010, 2014 if simpler.

**Output**  
• output is in `stats_sales_residential_20141017.csv` and `stats_sales_commercial_20141017.csv`  
• one row for each bay area geo_id with relevant sale transactions  
• one column for each calendar year from 1988 to 2014 (sales through 6/2014)  
• values are the count of residential or commercial sale transactions in a given year  
• sales are filtered for `sr_arms_length_flag = 1`  
• sales are filtered for the first character of `use_code_std` being `R` or `C`  
• code is in `stats_sales_residential.py` and `stats_sales_commercial.py`

**Next steps**  
• None


==========
#### C. Median sale price

Use transfer value field (`sr_val_transfer`) in sales table. Filter for arms-length transactions. Calculate for residential and commercial properties separately. Unit is price per square foot (square footage is in the assessor table). 

Structures are changed over time, especially prior to sales, so the best way to get an accurate square footage is probably to match sale data to the assessor data from the following year. The 2004 assessor data will have to be used for all sales from 1988-2004. 

Adjust for constant dollars using national headline CPI. 
http://www.bls.gov/data/inflation_calculator.htm

**Output**  
`price_sqft_v2.csv` (Sam M.)

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
`improvement_value_recent_10-3.csv` (Sam M.)

Data fields:  
`imprv_pct_median` = median portion of assessed value allocated to improvements  
`imprv_pct_stdev` = standard deviation, to indicate dispersion in underlying values    
`count` = count of applicable properties for each tract

This is based on residential properties in the current assessor table, using the `sa_imprv_pct` field. Filtered for properties sold in 2012, but only if the sales were arms-length (`sr_arms_length_flag` = 1).

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
• Replace tract id with GeoID  
• Calculate for all years  
• Add commercial properties


==========
#### E. Median square footage

For all residential properties. And separately for only properties that were sold. Match sales to subsequent assessor year. 

**Output**

**Next steps**


==========
#### F. Median number of rooms and bedrooms

For all residential properties. And separately to only properties that were sold. Match sales to subsequent assessor year. 

**Output**

**Next steps**


==========
#### G. Absentee ownership

For all residential properties in 2004 and 2014, plus percent change. Start with `sa_site_mail_same` field from current and historical assessor tables. 

**Output**

**Next steps**


==========
#### H. Property flips

Count of properties that were sold 2 or more times within 2 years. Filter for arms-length transactions.

**Output**

**Next steps**


==========
#### I. Use conversions

We're interested in condo conversions, residential to commercial, multifamily to single family, rental to ownership. 

**Output**

**Next steps**


==========
#### J. New construction

Assessor tables include a year built field.

**Output**

**Next steps**


