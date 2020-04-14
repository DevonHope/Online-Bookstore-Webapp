--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

-- Started on 2020-04-14 14:14:16

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 8 (class 2615 OID 33189)
-- Name: allops; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA allops;


ALTER SCHEMA allops OWNER TO postgres;

--
-- TOC entry 2857 (class 0 OID 0)
-- Dependencies: 8
-- Name: SCHEMA allops; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA allops IS 'Handles all operations in a single schema';


--
-- TOC entry 208 (class 1255 OID 33190)
-- Name: p_cuser(character varying, character varying, character varying); Type: PROCEDURE; Schema: allops; Owner: postgres
--

CREATE PROCEDURE allops.p_cuser(p_name character varying, p_username character varying, p_password character varying)
    LANGUAGE plpgsql SECURITY DEFINER
    AS $$BEGIN
    if ( select exists (select 1 from allops.user where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into tbl_user ( user_name, user_username, user_pswd )
        values( p_name, p_username, p_password );
     
    END IF;
END; 
$$;


ALTER PROCEDURE allops.p_cuser(p_name character varying, p_username character varying, p_password character varying) OWNER TO postgres;

--
-- TOC entry 222 (class 1255 OID 33237)
-- Name: global_regexp_search(text, text[], text[], text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.global_regexp_search(search_re text, param_tables text[] DEFAULT '{}'::text[], param_schemas text[] DEFAULT '{public}'::text[], progress text DEFAULT NULL::text) RETURNS TABLE(schemaname text, tablename text, columnname text, columnvalue text, rowctid tid)
    LANGUAGE plpgsql
    AS $$
declare
  query text;
begin
  FOR schemaname,tablename IN
      SELECT table_schema, table_name
      FROM information_schema.tables t
      WHERE (t.table_name=ANY(param_tables) OR param_tables='{}')
        AND t.table_schema=ANY(param_schemas)
        AND t.table_type='BASE TABLE'
  LOOP
    IF (progress in ('tables','all')) THEN
      raise info '%', format('Searching globally in table: %I.%I',
         schemaname, tablename);
    END IF;

    query := format('SELECT ctid FROM %I.%I AS t WHERE cast(t.* as text) ~ %L',
	    schemaname,
	    tablename,
	    search_re);
    FOR rowctid IN EXECUTE query
    LOOP
      FOR columnname IN
	  SELECT column_name
	  FROM information_schema.columns
	  WHERE table_name=tablename
	    AND table_schema=schemaname
      LOOP
	query := format('SELECT %I FROM %I.%I WHERE cast(%I as text) ~ %L AND ctid=%L',
	  columnname, schemaname, tablename, columnname, search_re, rowctid);
        EXECUTE query INTO columnvalue;
	IF columnvalue IS NOT NULL THEN
	  IF (progress in ('hits', 'all')) THEN
	    raise info '%', format('Found in %I.%I.%I at ctid %s, value: ''%s''',
		   schemaname, tablename, columnname, rowctid, columnvalue);
	  END IF;
	  RETURN NEXT;
	END IF;
      END LOOP; -- for columnname
    END LOOP; -- for rowctid
  END LOOP; -- for table
END;
$$;


ALTER FUNCTION public.global_regexp_search(search_re text, param_tables text[], param_schemas text[], progress text) OWNER TO postgres;

--
-- TOC entry 221 (class 1255 OID 33236)
-- Name: global_search(text, text[], text[], text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.global_search(search_term text, param_tables text[] DEFAULT '{book}'::text[], param_schemas text[] DEFAULT '{allops}'::text[], progress text DEFAULT NULL::text) RETURNS TABLE(schemaname text, tablename text, columnname text, rowctid tid)
    LANGUAGE plpgsql
    AS $$
declare
  query text;
  hit boolean;
begin
  FOR schemaname,tablename IN
      SELECT table_schema, table_name
      FROM information_schema.tables t
      WHERE (t.table_name=ANY(param_tables) OR param_tables='{}')
        AND t.table_schema=ANY(param_schemas)
        AND t.table_type='BASE TABLE'
  LOOP
    IF (progress in ('tables','all')) THEN
      raise info '%', format('Searching globally in table: %I.%I',
         schemaname, tablename);
    END IF;

    query := format('SELECT ctid FROM %I.%I AS t WHERE strpos(cast(t.* as text), %L) > 0',
	    schemaname,
	    tablename,
	    search_term);
    FOR rowctid IN EXECUTE query
    LOOP
      FOR columnname IN
	  SELECT column_name
	  FROM information_schema.columns
	  WHERE table_name=tablename
	    AND table_schema=schemaname
      LOOP
	query := format('SELECT true FROM %I.%I WHERE cast(%I as text)=%L AND ctid=%L',
	  schemaname, tablename, columnname, search_term, rowctid);
        EXECUTE query INTO hit;
	IF hit THEN
	  IF (progress in ('hits', 'all')) THEN
	    raise info '%', format('Found in %I.%I.%I at ctid %s',
		   schemaname, tablename, columnname, rowctid);
	  END IF;
	  RETURN NEXT;
	END IF;
      END LOOP; -- for columnname
    END LOOP; -- for rowctid
  END LOOP; -- for table
END;
$$;


ALTER FUNCTION public.global_search(search_term text, param_tables text[], param_schemas text[], progress text) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 33191)
-- Name: book; Type: TABLE; Schema: allops; Owner: postgres
--

CREATE TABLE allops.book (
    bk_name character varying NOT NULL,
    bk_auth character varying,
    bk_isbn bigint,
    bk_genre character varying,
    bk_pages bigint,
    bk_numauth bigint,
    bk_price bigint,
    bk_type character varying,
    bk_lang character varying,
    bk_pub character varying,
    bk_remain bigint,
    bk_id character varying(45),
    bk_sold bigint,
    bk_published character varying
);


ALTER TABLE allops.book OWNER TO postgres;

--
-- TOC entry 2858 (class 0 OID 0)
-- Dependencies: 203
-- Name: TABLE book; Type: COMMENT; Schema: allops; Owner: postgres
--

COMMENT ON TABLE allops.book IS 'stores all info on each book';


--
-- TOC entry 2859 (class 0 OID 0)
-- Dependencies: 203
-- Name: COLUMN book.bk_id; Type: COMMENT; Schema: allops; Owner: postgres
--

COMMENT ON COLUMN allops.book.bk_id IS 'id for each book';


--
-- TOC entry 204 (class 1259 OID 33197)
-- Name: checkout; Type: TABLE; Schema: allops; Owner: postgres
--

CREATE TABLE allops.checkout (
    ch_userid bigint NOT NULL,
    ch_billaddr character varying,
    ch_shipaddr character varying,
    ch_books character varying[]
);


ALTER TABLE allops.checkout OWNER TO postgres;

--
-- TOC entry 2860 (class 0 OID 0)
-- Dependencies: 204
-- Name: TABLE checkout; Type: COMMENT; Schema: allops; Owner: postgres
--

COMMENT ON TABLE allops.checkout IS 'checkout per user_id';


--
-- TOC entry 205 (class 1259 OID 33203)
-- Name: order_track; Type: TABLE; Schema: allops; Owner: postgres
--

CREATE TABLE allops.order_track (
    order_num bigint NOT NULL,
    last_loc character varying,
    track_history character varying[],
    track_num character varying
);


ALTER TABLE allops.order_track OWNER TO postgres;

--
-- TOC entry 2861 (class 0 OID 0)
-- Dependencies: 205
-- Name: TABLE order_track; Type: COMMENT; Schema: allops; Owner: postgres
--

COMMENT ON TABLE allops.order_track IS 'tracking info for an order';


--
-- TOC entry 206 (class 1259 OID 33209)
-- Name: publisher; Type: TABLE; Schema: allops; Owner: postgres
--

CREATE TABLE allops.publisher (
    p_id bigint NOT NULL,
    p_name character varying,
    p_addr character varying,
    p_email character varying,
    p_phnum bigint,
    p_bacct bigint
);


ALTER TABLE allops.publisher OWNER TO postgres;

--
-- TOC entry 2862 (class 0 OID 0)
-- Dependencies: 206
-- Name: TABLE publisher; Type: COMMENT; Schema: allops; Owner: postgres
--

COMMENT ON TABLE allops.publisher IS 'table for all publishers';


--
-- TOC entry 207 (class 1259 OID 33215)
-- Name: user; Type: TABLE; Schema: allops; Owner: postgres
--

CREATE TABLE allops."user" (
    user_id bigint NOT NULL,
    user_name character varying(45),
    user_username character varying(45),
    user_pswd character varying(45),
    user_biladdr character varying,
    user_shipaddr character varying,
    user_email character varying
);


ALTER TABLE allops."user" OWNER TO postgres;

--
-- TOC entry 2863 (class 0 OID 0)
-- Dependencies: 207
-- Name: TABLE "user"; Type: COMMENT; Schema: allops; Owner: postgres
--

COMMENT ON TABLE allops."user" IS 'stores all users';


--
-- TOC entry 2864 (class 0 OID 0)
-- Dependencies: 207
-- Name: COLUMN "user".user_biladdr; Type: COMMENT; Schema: allops; Owner: postgres
--

COMMENT ON COLUMN allops."user".user_biladdr IS 'billing info for the user';


--
-- TOC entry 2865 (class 0 OID 0)
-- Dependencies: 207
-- Name: COLUMN "user".user_shipaddr; Type: COMMENT; Schema: allops; Owner: postgres
--

COMMENT ON COLUMN allops."user".user_shipaddr IS 'shipping info for the user';


--
-- TOC entry 2847 (class 0 OID 33191)
-- Dependencies: 203
-- Data for Name: book; Type: TABLE DATA; Schema: allops; Owner: postgres
--

COPY allops.book (bk_name, bk_auth, bk_isbn, bk_genre, bk_pages, bk_numauth, bk_price, bk_type, bk_lang, bk_pub, bk_remain, bk_id, bk_sold, bk_published) FROM stdin;
The Hitchhikers Guide To The Galaxy	Douglas Adams	9780345391803	Science Fiction	224	1	25	Paperback	English	Del Ray	1000	1	1	September 27 1995
Dune	Frank Herbert	9780240807720	Science Fiction	412	1	7	Paperback	English	Chilton Books	999	2	200	August 1 1965
Do Androids Dream Of Electric Sheep	Philip K. Dick	9781407234694	Science Fiction	210	1	6	Paperback	English	Doubleday	1200	3	400	1968
\.


--
-- TOC entry 2848 (class 0 OID 33197)
-- Dependencies: 204
-- Data for Name: checkout; Type: TABLE DATA; Schema: allops; Owner: postgres
--

COPY allops.checkout (ch_userid, ch_billaddr, ch_shipaddr, ch_books) FROM stdin;
1234	\N	\N	{Dune:7}
5	\N	\N	{Dune:7}
\.


--
-- TOC entry 2849 (class 0 OID 33203)
-- Dependencies: 205
-- Data for Name: order_track; Type: TABLE DATA; Schema: allops; Owner: postgres
--

COPY allops.order_track (order_num, last_loc, track_history, track_num) FROM stdin;
6	Origin state	{"Shipped from warehouse","Left origin state"}	LIB-5kxnefhzhnr
\.


--
-- TOC entry 2850 (class 0 OID 33209)
-- Dependencies: 206
-- Data for Name: publisher; Type: TABLE DATA; Schema: allops; Owner: postgres
--

COPY allops.publisher (p_id, p_name, p_addr, p_email, p_phnum, p_bacct) FROM stdin;
\.


--
-- TOC entry 2851 (class 0 OID 33215)
-- Dependencies: 207
-- Data for Name: user; Type: TABLE DATA; Schema: allops; Owner: postgres
--

COPY allops."user" (user_id, user_name, user_username, user_pswd, user_biladdr, user_shipaddr, user_email) FROM stdin;
5	Devon Hope	d_hope	popeey	123 d, d, d, d, d	123 d, d, d, d, d	d@mail.com
1234	dummy	udummy	pass	null	null	dumyy@mail.com
12	d	de	pass	null	null	d@mail.com
3	bunny	bunalou	gbuns	null	null	buns@garbunso.ca
4	bunalou	buns	gbuns	null	null	g@buns.ca
1	The Man	Mansly	not pass	123 mans way, no men, some state, old country, postal	123 mans way, no men, some state, old country, postal	mansly@mens.ca
\.


--
-- TOC entry 2711 (class 2606 OID 33222)
-- Name: book book_pkey; Type: CONSTRAINT; Schema: allops; Owner: postgres
--

ALTER TABLE ONLY allops.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (bk_name);


--
-- TOC entry 2713 (class 2606 OID 33224)
-- Name: checkout checkout_pkey; Type: CONSTRAINT; Schema: allops; Owner: postgres
--

ALTER TABLE ONLY allops.checkout
    ADD CONSTRAINT checkout_pkey PRIMARY KEY (ch_userid);


--
-- TOC entry 2715 (class 2606 OID 33226)
-- Name: order_track order_track_pkey; Type: CONSTRAINT; Schema: allops; Owner: postgres
--

ALTER TABLE ONLY allops.order_track
    ADD CONSTRAINT order_track_pkey PRIMARY KEY (order_num);


--
-- TOC entry 2717 (class 2606 OID 33228)
-- Name: publisher publisher_pkey; Type: CONSTRAINT; Schema: allops; Owner: postgres
--

ALTER TABLE ONLY allops.publisher
    ADD CONSTRAINT publisher_pkey PRIMARY KEY (p_id);


--
-- TOC entry 2719 (class 2606 OID 33230)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: allops; Owner: postgres
--

ALTER TABLE ONLY allops."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- TOC entry 2720 (class 2606 OID 33231)
-- Name: checkout user; Type: FK CONSTRAINT; Schema: allops; Owner: postgres
--

ALTER TABLE ONLY allops.checkout
    ADD CONSTRAINT "user" FOREIGN KEY (ch_userid) REFERENCES allops."user"(user_id);


-- Completed on 2020-04-14 14:14:20

--
-- PostgreSQL database dump complete
--

