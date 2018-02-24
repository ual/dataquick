dataquick
=========

Code for parsing and analytics of Dataquick assessor and sales data

#### Update, Feb. 2018

This repository documents data parsing and analysis performed in 2014-15. None of the database servers referenced are live anymore. 

**Additional documentation**  
• [Indicators](https://github.com/ual/dataquick/blob/master/ucb_documentation/indicators.md)  
• [Data processing procedures](https://github.com/ual/dataquick/blob/master/ucb_documentation/data_processing.md)

=========

**Contacts**  
• Miriam Zuk, project lead – `mzuk@berkeley.edu`  
• Sam Maurer, code – `maurer@berkeley.edu`  

**Documentation from the data vendor**  
• "Layout" spreadsheets with database schema information  
• "Totals Report" spreadsheets with record counts by county  
• "Catalog/Data Dictionary" spreadsheet with more detailed field definitions  

=========
#### Contents of raw data files

**Assessor**  
• one record per legal property  
• most recent snapshot, from 2013 or 2014 depending on the county  
• provided as one large fixed-width text file (dated 5-28-2014)  
• identical data provided as sequence of smaller tab-delimited files (dated 7-11-2014)  
• do not use intermediate tab-delimited version from June, which had formatting errors

**Assessor history**  
• yearly snapshots of records from each county (frequency varies beginning in 2012)  
• data covers 2004–2013 for all counties, plus 2014 for some counties  
• provided as sequence of large fixed-width text files (dated 7-20 or 7-21-2014)  
• do not use earlier May/June version of the files, which didn't match the schema

**Sales**  
• one record per transaction  
• covers 1988 to mid-2014, plus earlier transactions for certain counties  
• provided as one large fixed-width text file (dated 5-28-2014)  
• equivalent data provided as sequence of smaller tab-delimited files (dated 7-9-2014), including some additional transaction types  
• do not use intermediate tab-delimited version from June, which had formatting errors  

**Foreclosure**  
• provided as one large fixed-width text file (dated 5-28-2014)  
• same data also provided as a tab-delimited file (dated 6-16-2014)  
