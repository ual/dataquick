### Data processing procedures

#### 1. Initial parsing

Initial data parsing was done using Python to confirm the contents of files and whether field values, row lengths, and row counts matched the schemas and totals reports. This exploratory code is in IPython notebooks in the `maurer_code/ipynb/` directory.

#### 2. Loading data into the Postgres database

The raw data tables were loaded into a Postgres database using the `load_*.py` scripts under `maurer_code`. For each table, a Postgres schema was created using the field names and data types listed in the Dataquick layout file. 

Each row of raw data was read into Python and parsed into fields according to the tab delimiters or the character lengths in the layout file. Trailing spaces were removed, and some minimal formatting was done so that the raw text would be parsed correctly by Postgres. The data values were then fed into the database using a separate `insert` statement for each record. This is slow (~10 hours per table) but easy to verify and troubleshoot. Indexes were generated for all the fields likely to be used as query filters. 

Note that we've retained all of Dataquick's formatting quirks. For example, if Dataquick stored a boolean value as a text string, we do the same. This was done to avoid inadvertantly losing any data from the raw tables. 

Dataquick's unique id's are used as primary keys where possible. For the Assessor History table, we created our own unique `ucb_ahist_id` that's an 18-digit concatenation of the year, data version, and property id. For the Current Assessor table, we added a geographic identifier that's easier to match to census data. It's called `ucb_geo_id` and is an 11-character concatenation of the state, county, and census tract FIPS codes. 

#### 3. Generating CSV extracts *from raw text files*

Before the database was set up, CSV extracts were generated from the raw text files. Each row was parsed according to the tab delimiters or character lengths in the layout file. Trailing spaces were removed, but there was no other formatting of data values. The code for these extracts (produced in Summer 2014) is in IPython notebooks rather than stand-alone scripts.

#### 4. Generating CSV extracts *from the Postgres database*

Now that the data is loaded into Postgres, CSV extracts can be more easily generated using the command-line `psql /copy` tool. This writes the output of a SQL query directly to a CSV file, which allows data to be easily subsetted and fields to be joined from multiple tables. Many of the extracts were updated using this procedure in November 2014. 

Code is in the shell scripts named `extract_*.sh` under `maurer_code` in this repository, and CSV output is saved on Box. These "v2" sales and foreclosure extracts include geo fields joined from the current assessor table, for all the records that could be matched by property id. 

#### 4. Sales transaction data filtering

In January 2015 we implemented a detailed analysis and filtering of the sales table in order to isolate true market-rate sales, with valid price-per-square-foot and without duplication. [Please refer to the linked Word document for more info.](https://github.com/ual/dataquick/blob/master/ucb_documentation/Dataquick%20Cleaning%202015-01-14.docx?raw=true)

Filtered transaction records have been saved to the a new database table called `sales_clean_res`, which includes all sales fields, several assessor fields for convenience (`use_code_std`, `sa_sqft`, `sa_x_coord`, `sa_y_coord`, `sa_geo_qlty_code`), and some new custom fields: 

• `ucb_geo_id`: 11-character concatenation of the state, county, and census tract FIPS codes  
• `ucb_price_sqft`: price per square foot in nominal dollars  
• `ucb_price_sqft_adj`: price per square foot adjusted to 2010 dollars using national headline CPI  
• `ucb_condo_subdiv_flag`: marks a single record saved from a multi-property transaction  
• `ucb_condo_subdiv_sqft`: combined square footage from a multi-property transaction  

There is another table called `sales_clean_nonres` for nonresidential transactions. We used idential criteria, except for skipping the price outliers filter.
