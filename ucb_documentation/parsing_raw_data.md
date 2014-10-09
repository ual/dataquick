#### Data parsing procedures

Initial data parsing was done by Sam Maurer in Python. Code is provided in this repository. 

The first stage was basic parsing of the text files to see whether field values, row lengths, and row counts matched the schemas and totals reports. The second stage was generating data extracts for each county in CSV format, so the data could be opened in Stata and other software. The third stage was loading the data into a Postgres database. 

**Procedure for generating CSV county extracts**

Each row of raw data is read into Python and parsed into fields according to the tab delimiters or the character lengths in the layout file. If the `mm_fips_county_name` matches a county of interest, the record is kept, and otherwise it is discarded. Trailing spaces are removed, but there is no other formatting of data values; the CSV files are character-by-character equivalent to the original data contents. Text values that contain commas are placed inside quotes for the CSV output.

**Procedure for loading data into Postgres**

For each table, a Postgres schema is created to match the field names and data types in the Dataquick layout file. To account for differences between Dataquick’s SQL Server system and Postgres, data types are changed as follows: `tinyint` to `smallint`, `bit` to `boolean`, and `datetime` to `timestamp`. 

Each row of raw data is read into Python and parsed into fields according to the tab delimiters or the character lengths in the layout file. Trailing spaces are removed, and some minimal formatting is done so that the raw text will be parsed correctly by Postgres: strings, booleans, and timestamps are placed inside quotes, and empty numeric values are replaced with `null`. The data values are fed into the database using a separate `insert` statement for each record. This is slow (~10 hours per table) but robust and easy to troubleshoot. 

Note that we are retaining whatever data formatting quirks Dataquick may have adopted. Rather than convert a field storing `1` and `0` as strings into boolean format, for example, it seemed better to store data in the exact same format that Dataquick uses and then investigate the contents of particular fields later on. 

Unique id's are used as primary table keys, and indexes are added on fields that may frequently appear in queries: county and census tract codes, dates, other id's, and so on. 
