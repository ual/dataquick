# This script loads cleaned sales data into a separate extended table

import psycopg2
import time

# Connect to the database
conn_string = "host='tehran.ual.berkeley.edu' dbname='dataquick' user='dataquick_admin' password='Visua1ization'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# Set up new table
try:
	cur.execute('''

	CREATE TABLE master.sales_clean_res
	(
	  sr_unique_id integer NOT NULL,
	  sr_property_id integer,
	  sr_scm_id integer,
	  mm_state_code character varying,
	  mm_muni_name character varying,
	  mm_fips_state_code smallint,
	  mm_fips_muni_code smallint,
	  mm_fips_county_name character varying,
	  sr_parcel_nbr_raw character varying,
	  sr_site_addr_raw character varying,
	  sr_mail_addr_raw character varying,
	  sr_mail_house_nbr character varying,
	  sr_mail_fraction character varying,
	  sr_mail_dir character varying,
	  sr_mail_street_name character varying,
	  sr_mail_suf character varying,
	  sr_mail_post_dir character varying,
	  sr_mail_unit_pre character varying,
	  sr_mail_unit_val character varying,
	  sr_mail_city character varying,
	  sr_mail_state character varying,
	  sr_mail_zip character varying,
	  sr_mail_plus_4 character varying,
	  sr_mail_crrt character varying,
	  sr_lgl_dscrptn character varying,
	  sr_lgl_keyed_block character varying,
	  sr_lgl_keyed_lot character varying,
	  sr_lgl_keyed_plat_book character varying,
	  sr_lgl_keyed_plat_page character varying,
	  sr_lgl_keyed_range character varying,
	  sr_lgl_keyed_section character varying,
	  sr_lgl_keyed_sub_name character varying,
	  sr_lgl_keyed_township character varying,
	  sr_lgl_keyed_tract character varying,
	  sr_lgl_keyed_unit character varying,
	  sr_buyer character varying,
	  sr_seller character varying,
	  sr_val_transfer integer,
	  sr_tax_transfer numeric,
	  sr_doc_nbr_raw character varying,
	  sr_doc_nbr_fmt character varying,
	  sr_date_transfer integer,
	  sr_date_filing integer,
	  sr_doc_type character varying,
	  sr_deed_type character varying,
	  sr_tran_type character varying,
	  sr_quitclaim boolean,
	  sr_arms_length_flag character varying,
	  sr_full_part_code character varying,
	  sr_mult_apn_flag_keyed character varying,
	  sr_mult_port_code character varying,
	  sr_lndr_seller_flag character varying,
	  sr_td_doc_nbr_1 character varying,
	  sr_loan_id_1 character varying,
	  sr_loan_id_1_ext character varying,
	  sr_loan_val_1 integer,
	  sr_loan_type_1 character varying,
	  sr_int_rate_type_1 character varying,
	  sr_lndr_credit_line_1 character varying,
	  sr_lndr_code_1 integer,
	  sr_lndr_first_name_1 character varying,
	  sr_lndr_last_name_1 character varying,
	  sr_lender_type_1 character varying,
	  sr_td_doc_nbr_2 character varying,
	  sr_loan_id_2 character varying,
	  sr_loan_id_2_ext character varying,
	  sr_loan_val_2 integer,
	  sr_loan_type_2 character varying,
	  sr_int_rate_type_2 character varying,
	  sr_lndr_credit_line_2 character varying,
	  sr_lndr_code_2 integer,
	  sr_lndr_first_name_2 character varying,
	  sr_lndr_last_name_2 character varying,
	  sr_lender_type_2 character varying,
	  sr_td_doc_nbr_3 character varying,
	  sr_loan_id_3 character varying,
	  sr_loan_id_3_ext character varying,
	  sr_loan_val_3 integer,
	  sr_loan_type_3 character varying,
	  sr_int_rate_type_3 character varying,
	  sr_lndr_code_3 integer,
	  sr_lndr_credit_line_3 character varying,
	  sr_lndr_first_name_3 character varying,
	  sr_lndr_last_name_3 character varying,
	  sr_lender_type_3 character varying,
	  distress_indicator character varying,
	  process_id integer,

	  use_code_std character varying,
	  sa_sqft integer,
	  sa_x_coord numeric,
	  sa_y_coord numeric,
	  sa_geo_qlty_code character varying,
  
	  ucb_geo_id character varying,
	  ucb_price_sqft integer,
	  ucb_price_sqft_adj integer,
	  ucb_condo_subdiv_flag integer,
	  ucb_condo_subdiv_sqft integer,

	  CONSTRAINT sales_clean_pkey PRIMARY KEY (sr_unique_id)
	)			
	''')
	cur.execute("GRANT SELECT ON TABLE master.sales_clean_res TO dataquick_user;")
	conn.commit()
except:
	pass
	

# Load data

t0 = time.time()
conn.commit()
cur.execute('''

WITH sales_base AS (
    SELECT
        s.*,
        a.sa_census_tract,
		a.ucb_geo_id,
        a.sa_sqft,
        a.use_code_std,
        a.sa_x_coord, 
		a.sa_y_coord, 
		a.sa_geo_qlty_code
    FROM
        master.sales AS s
    INNER JOIN
        master.assessor AS a
    ON
        a.sa_property_id = s.sr_property_id
    WHERE
        s.sr_property_id IS NOT null
        AND s.sr_property_id > 0
        AND s.mm_fips_muni_code IN (1,13,41,55,75,81,85,95,97)
        AND (s.sr_date_transfer/10000) >= 1988
        AND s.sr_arms_length_flag = '1'
        AND s.sr_val_transfer IS NOT null
        AND s.sr_val_transfer > 0
        AND a.sa_census_tract <> ''
        AND a.sa_sqft IS NOT null
        AND a.sa_sqft > 0
        AND a.use_code_std <> ''
        AND SUBSTRING(a.use_code_std FROM 1 FOR 1) = 'R'
        AND (s.sr_tran_type = 'R'
            OR s.sr_tran_type = 'S')
        AND s.sr_buyer NOT ILIKE '% trust%'
        AND s.sr_seller NOT ILIKE '% trust%'
        AND s.sr_buyer NOT ILIKE '%city%'
        AND s.sr_seller NOT ILIKE '%city%'
        AND s.sr_buyer NOT ILIKE '%county%'
        AND s.sr_seller NOT ILIKE '%county%'
        AND s.sr_buyer NOT ILIKE '%agency%'
        AND s.sr_seller NOT ILIKE '%agency%'
        AND s.sr_buyer NOT ILIKE '%redevelopment%'
        AND s.sr_seller NOT ILIKE '%redevelopment%'
),

sales_extended AS (
    SELECT 
        s.*,
        prop_grp.dup_count AS prop_dup_count,
        doc_grp.dup_count AS doc_dup_count,
        doc_grp.price_count AS doc_price_count,
        doc_grp.grp_sqft AS doc_grp_sqft,
        ROW_NUMBER() OVER
            (PARTITION BY doc_grp.grp_id
            ORDER BY s.sr_property_id) AS doc_grp_row,
        price_multiple
    FROM
        sales_base AS s

    LEFT OUTER JOIN
        (SELECT
            sr_date_transfer,
            sr_property_id,
            COUNT(*) AS dup_count
        FROM 
            sales_base
        GROUP BY
            sr_date_transfer,
            sr_property_id) AS prop_grp
    ON
        prop_grp.sr_date_transfer = s.sr_date_transfer
        AND prop_grp.sr_property_id = s.sr_property_id

    LEFT OUTER JOIN
        (SELECT
            mm_fips_muni_code,
            sr_date_transfer,
            sr_doc_nbr_fmt,
            COUNT (*) AS dup_count,
            COUNT (DISTINCT sr_val_transfer) AS price_count,
            SUM (sa_sqft) AS grp_sqft,
            ROW_NUMBER() OVER() AS grp_id
        FROM 
            sales_base
        GROUP BY
            mm_fips_muni_code,
            sr_date_transfer,
            sr_doc_nbr_fmt) AS doc_grp
    ON
        doc_grp.mm_fips_muni_code = s.mm_fips_muni_code
        AND doc_grp.sr_date_transfer = s.sr_date_transfer
        AND doc_grp.sr_doc_nbr_fmt = s.sr_doc_nbr_fmt
        
    LEFT OUTER JOIN
        (SELECT
            year,
            price_multiple
        FROM
            master.inflation_adjustment) AS infl
        ON
            infl.year = (s.sr_date_transfer/10000)
),

sales_extended2 AS (
	SELECT
		*, 
		(CASE 
			WHEN doc_dup_count > 1 AND doc_price_count = 1 
				THEN sr_val_transfer/doc_grp_sqft
			ELSE sr_val_transfer/sa_sqft
		END) AS ucb_price_sqft,
		(CASE 
			WHEN doc_dup_count > 1 AND doc_price_count = 1 
				THEN sr_val_transfer*price_multiple/doc_grp_sqft
			ELSE sr_val_transfer*price_multiple/sa_sqft
		END) AS ucb_price_sqft_adj,
		(CASE
			WHEN doc_dup_count > 1 THEN 1 ELSE 0
		END) AS ucb_condo_subdiv_flag,
		doc_grp_sqft AS ucb_condo_subdiv_sqft
	FROM
		sales_extended
	WHERE
		prop_dup_count = 1
		AND doc_grp_row = 1
)

INSERT INTO
	master.sales_clean_res
	
SELECT 
	sr_unique_id, sr_property_id, sr_scm_id, mm_state_code, mm_muni_name, mm_fips_state_code, mm_fips_muni_code, mm_fips_county_name, sr_parcel_nbr_raw, sr_site_addr_raw, sr_mail_addr_raw, sr_mail_house_nbr, sr_mail_fraction, sr_mail_dir, sr_mail_street_name, sr_mail_suf, sr_mail_post_dir, sr_mail_unit_pre, sr_mail_unit_val, sr_mail_city, sr_mail_state, sr_mail_zip, sr_mail_plus_4, sr_mail_crrt, sr_lgl_dscrptn, sr_lgl_keyed_block, sr_lgl_keyed_lot, sr_lgl_keyed_plat_book, sr_lgl_keyed_plat_page, sr_lgl_keyed_range, sr_lgl_keyed_section, sr_lgl_keyed_sub_name, sr_lgl_keyed_township, sr_lgl_keyed_tract, sr_lgl_keyed_unit, sr_buyer, sr_seller, sr_val_transfer, sr_tax_transfer, sr_doc_nbr_raw, sr_doc_nbr_fmt, sr_date_transfer, sr_date_filing, sr_doc_type, sr_deed_type, sr_tran_type, sr_quitclaim, sr_arms_length_flag, sr_full_part_code, sr_mult_apn_flag_keyed, sr_mult_port_code, sr_lndr_seller_flag, sr_td_doc_nbr_1, sr_loan_id_1, sr_loan_id_1_ext, sr_loan_val_1, sr_loan_type_1, sr_int_rate_type_1, sr_lndr_credit_line_1, sr_lndr_code_1, sr_lndr_first_name_1, sr_lndr_last_name_1, sr_lender_type_1, sr_td_doc_nbr_2, sr_loan_id_2, sr_loan_id_2_ext, sr_loan_val_2, sr_loan_type_2, sr_int_rate_type_2, sr_lndr_credit_line_2, sr_lndr_code_2, sr_lndr_first_name_2, sr_lndr_last_name_2, sr_lender_type_2, sr_td_doc_nbr_3, sr_loan_id_3, sr_loan_id_3_ext, sr_loan_val_3, sr_loan_type_3, sr_int_rate_type_3, sr_lndr_code_3, sr_lndr_credit_line_3, sr_lndr_first_name_3, sr_lndr_last_name_3, sr_lender_type_3, distress_indicator, process_id,
	
	use_code_std, 
	sa_sqft, 
	sa_x_coord, 
	sa_y_coord, 
	sa_geo_qlty_code, 
	ucb_geo_id, 
	
	ucb_price_sqft, 
	ucb_price_sqft_adj, 
	ucb_condo_subdiv_flag, 
	ucb_condo_subdiv_sqft
	
FROM 
    sales_extended2
WHERE
	(mm_fips_muni_code = 1 AND ucb_price_sqft_adj < 1054)
	OR (mm_fips_muni_code = 13 AND ucb_price_sqft_adj < 794)
	OR (mm_fips_muni_code = 41 AND ucb_price_sqft_adj < 1788)
	OR (mm_fips_muni_code = 55 AND ucb_price_sqft_adj < 1577)
	OR (mm_fips_muni_code = 75 AND ucb_price_sqft_adj < 2014)
	OR (mm_fips_muni_code = 81 AND ucb_price_sqft_adj < 1773)
	OR (mm_fips_muni_code = 85 AND ucb_price_sqft_adj < 1354)
	OR (mm_fips_muni_code = 95 AND ucb_price_sqft_adj < 729)
	OR (mm_fips_muni_code = 97 AND ucb_price_sqft_adj < 1260)

''')
conn.commit()
cur.execute("SELECT count(*) FROM master.sales_clean_res")
print "rows //", cur.fetchone()[0]
print "minutes //", round((time.time() - t0)*1.0/60, 2)


# Add some indexes

t0 = time.time()
cur.execute("CREATE INDEX sales_clean_fips_index ON master.sales_clean_res " +
			" USING btree (mm_fips_muni_code);")
conn.commit()
print "sales_clean_fips_index", round(time.time() - t0)

t0 = time.time()
cur.execute("CREATE INDEX sales_clean_property_index ON master.sales_clean_res " +
			"USING btree (sr_property_id);")
conn.commit()
print "sales_clean_property_index", round(time.time() - t0)

t0 = time.time()
cur.execute("CREATE INDEX sales_clean_date_index ON master.sales_clean_res " +
			"USING btree (sr_date_transfer);")
conn.commit()
print "sales_clean_date_index", round(time.time() - t0)

t0 = time.time()
cur.execute("CREATE INDEX sales_clean_geo_index ON master.sales_clean_res " +
			"USING btree (ucb_geo_id);")
conn.commit()
print "sales_clean_geo_index", round(time.time() - t0)
