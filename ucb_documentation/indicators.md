indicators
==========

Documentation of tract-level indicators

Output  
General to-do items  
A. Number of properties by type  
B. Number of sales  
C. Median sale price  
D. Ratio of improvement value to land value  
E. Median square footage  
F. Median number of rooms and bedrooms  
G. Absentee ownership  
H. Property flips  
I. Condo conversions


#### Output

Indicators will be saved as CSV files with one row per census tract. File names will be brief, descriptive, and include the date produced as a versioning mechanism. 

For aggregate statistics (like median), include a separate field with the count of applicable records from each census tract. 

Master copy of output files:  
https://github.com/ual/dataquick/tree/master/indicator_output  
(to download, click on a file name, then "Raw", then save it)

Code used to generate output files:  
https://github.com/ual/dataquick/tree/master/maurer_code  
https://github.com/ual/dataquick/tree/master/blanchard_code


#### General to-do items

• Are the Dataquick census tract assignments correct?  
• What are the reporting dates for the annual assessor snapshots?  


#### A. Number of properties by type

Based on Dataquick standard use code (`use_code_std`) in assessor tables. First divided into high-level categories (commercial, industrial, residential, etc) and then into detailed categories. 

Do for each year if possible, or else 2004, 2006, 2010, 2014.

**Output**

**Next steps**


#### B. Number of sales

For residential and commercial properties separately. Filter for arms-length transactions. Do each year since 1988, or start with 2004, 2006, 2010, 2014 if simpler.

**Output**

**Next steps**


#### C. Median sale price

Use transfer value field (`sr_val_transfer`) in sales table. Filter for arms-length transactions. Calculate for residential and commercial properties separately. 

Units should be price per square foot. Square footage is in the assessor table. 

Adjust for constant dollars using national headline CPI. 
http://www.bls.gov/data/inflation_calculator.htm

**Output**

**Next steps**
• 