dataquick
=========

Code for parsing and analytics of the Dataquick assessor and sales data

#### Project background

We obtained a large dataset of parcel and sales transaction records from Dataquick, covering the entire state of California and going back 10 to 25+ years. The data was purchased by the California Air Resources Board (ARB) for research we are performing on their behalf about residential displacement that’s linked to transit-oriented development.

**Contacts**  
• Miriam Zuk, project manager – `mzuk@berkeley.edu`  
• Sam Maurer, performed the initial data parsing – `maurer@berkeley.edu`  
• Courtney Smith, ARB contact – `cesmith@arb.ca.gov`  
• Christopher LaPage, Dataquick account manager – `clapage@dataquick.com`  
• Juan Qui, Dataquick fulfillment contact – `jqui@dataquick.com`  

**Documentation from Dataquick**  
• "Layout" spreadsheets with database schema information  
• "Totals Report" spreadsheets with record counts by county  
• "Catalog/Data Dictionary" spreadsheet with more detailed field definitions  
• These are available from Box or FTP (see below)  

#### Ways to access the data

1. Data is in Postgres on the UAL Paris server  
• URL: `paris.ual.berkeley.edu`  
• databse: `california`  
• schema: `dataquick`  
• tables: `assessor`, `assessorhist`, `sales`, `foreclosure`
2. Raw data files and CSV county extracts are in a shared folder on Box (contact Miriam Zuk for access)
3. Raw data files are also available from Dataquick by FTP  
• URL: `ftp.dataquick.com`  
• username: `ucbrkly`  
• password: `2a3jsv13`

#### Contents of raw data files

**Assessor**  
• one record per legal property  
• most recent snapshot, from 2013 or 2014 depending on the county  
• provided as one large fixed-width text file (dated 5-28-2014)  
• identical data provided as sequence of smaller tab-delimited files (dated 7-11-2014)  
• do not use intermediate tab-delimited version from June, which had formatting errors

**Assessor history**  
• yearly snapshots of records from each county  
• data covers 2004–2013 for all counties, plus 2014 for some counties  
• provided as sequence of large fixed-width text files (dated 7-20 or 7-21-2014)  
• do not use earlier May/June version of the files, which didn't match the schema

**Sales**  
• one record per transaction  
• covers 1988 to mid-2014, plus earlier transactions for certain counties  
• provided as one large fixed-width text file (dated 5-28-2014)  
• equivalent data provided as sequence of smaller tab-delimited files (dated 7-9-2014), including some additional transaction types  
• do not use intermediate tab-delimited version from June, which had formatting errors  
*check: do the later files also include additional records from the month of June?*

**Foreclosure = Foreclosure notice information**  
• provided as one large fixed-width text file (dated 5-28-2014)  
• same data also provided as a tab-delimited file (dated 6-16-2014)  
*check: have we compared the fixed-width and tab-delimited files yet?*

#### Data parsing procedures

Initial data parsing was done by Sam Maurer in Python. Code is provided in this repository. 

The first stage was basic parsing of the text files to see whether field values, row lengths, and row counts matched the schemas and totals reports. The second stage was generating data extracts for each county in CSV format, so the data could be opened in Stata and other software. The third stage was loading the data into a Postgres database. 

**Procedure for generating CSV county extracts**

Each row of raw data is read into Python and parsed into fields according to the tab delimiters or the character lengths in the layout file. If the `mm_fips_county_name` matches a county of interest, the record is kept, and otherwise it is discarded. Trailing spaces are removed, but there is no other formatting of data values; the CSV files are character-by-character equivalent to the original data contents. Text values that contain commas are placed inside quotes for the CSV output.

**Procedure for loading data into Postgres**

For each table, a Postgres schema is created to match the field names and data types in the Dataquick layout file. To account for differences between Dataquick’s SQL Server system and Postgres, `tinyint` fields are changed to `smallint`, `bit` is changed to `boolean`, and `datetime` is changed to `timestamp`. 

Each row of raw data is read into Python and parsed into fields according to the tab delimiters or the character lengths in the layout file. Trailing spaces are removed, and some minimal formatting is done so that the raw text will be parsed correctly by Postgres: strings, booleans, and timestamps are placed inside quotes, and empty numeric values are replaced with `null`. The data values are fed into the database using a separate `insert` statement for each record. This is slow (~10 hours per table) but robust and easy to troubleshoot. 

Note that we are retaining whatever data formatting quirks Dataquick may have adopted. Rather than convert a field storing `1` and `0` as strings into boolean format, for example, it seemed better to store data in the exact same format that Dataquick uses and then investigate the contents of particular fields later on. 

Unique id's are used as primary table keys, and indexes are added on fields that may frequently appear in queries: county and census tract codes, dates, other id's, and so on. 