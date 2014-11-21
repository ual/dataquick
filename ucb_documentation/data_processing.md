#### Data parsing procedures

Initial data parsing was done by Sam Maurer in Python. Code is provided in the `maurer_code` directory: exploratory code in the iPython notebooks and production code in `load_assessor.py`, `load_sales.py`, `load_ahist.py`, `load_foreclosure.py`. 

The first stage was basic parsing of the text files to see whether field values, row lengths, and row counts matched the schemas and totals reports. The second stage was generating data extracts for each county in CSV format, so the data could be opened in Stata and other software. The third stage was loading the data into a Postgres database. 

**Procedure for generating CSV county extracts**

**Procedure using raw text files:** Each row of raw data was read into Python and parsed into fields according to the tab delimiters or the character lengths in the layout file. If the `mm_fips_county_name` matched a county of interest, the record was kept, and otherwise it was discarded. Trailing spaces were removed, but there was no other formatting of data values; the CSV files are character-by-character equivalent to the original data contents. Text values that contain commas are placed inside quotes for the CSV output. Extracts were produced using this procedure in Summer 2014. The code is in IPython notebooks, not in stand-alone scripts.

**Procedure using the Postgres database:** Now that the data is loaded into Postgres, CSV extracts can be more easily generated using the `psql /copy` command. This writes the output of a SQL query directly to a CSV file, which allows joining of fields from multiple tables. Some of the extracts were updating using this procedure in November 2014. Code is in the shell scripts named `extract_*.sh` under `maurer_code` in this repository, and CSV output is saved on Box. These "v2" sale and foreclosure extracts include geo fields from the current assessor table, for records that could be matched by property id. The assessor history extracts were generated using the first procedure for 2004 data only, and then again using the Postgres-based procedure for all years. 

**Procedure for loading data into Postgres**

For each table, a Postgres schema is created to match the field names and data types in the Dataquick layout file. To account for differences between Dataquick’s SQL Server system and Postgres, data types are changed as follows: `tinyint` to `smallint`, `bit` to `boolean`, and `datetime` to `timestamp`. 

Each row of raw data is read into Python and parsed into fields according to the tab delimiters or the character lengths in the layout file. Trailing spaces are removed, and some minimal formatting is done so that the raw text will be parsed correctly by Postgres: strings, booleans, and timestamps are placed inside quotes, and empty numeric values are replaced with `null`. The data values are fed into the database using a separate `insert` statement for each record. This is slow (~10 hours per table) but robust and easy to troubleshoot. 

Note that we are retaining whatever data formatting quirks Dataquick may have adopted. Rather than convert a field storing `1` and `0` as strings into boolean format, for example, it seemed better to store data in the exact same format that Dataquick uses and then investigate the contents of particular fields later on. 

Unique id's are used as primary table keys, and indexes are added on fields that may frequently appear in queries: county and census tract codes, dates, other id's, and so on. 
