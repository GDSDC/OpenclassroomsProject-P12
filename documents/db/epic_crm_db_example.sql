--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

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

ALTER TABLE ONLY public.users_user_user_permissions DROP CONSTRAINT users_user_user_permissions_user_id_20aca447_fk_users_user_id;
ALTER TABLE ONLY public.users_user_user_permissions DROP CONSTRAINT users_user_user_perm_permission_id_0b93982e_fk_auth_perm;
ALTER TABLE ONLY public.users_user_groups DROP CONSTRAINT users_user_groups_user_id_5f6f5a90_fk_users_user_id;
ALTER TABLE ONLY public.users_user_groups DROP CONSTRAINT users_user_groups_group_id_9afc8d0e_fk_auth_group_id;
ALTER TABLE ONLY public.events_event DROP CONSTRAINT events_event_support_id_32d9d666_fk_users_user_id;
ALTER TABLE ONLY public.events_event DROP CONSTRAINT events_event_client_id_dc0c6190_fk_clients_client_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_user_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE ONLY public.contracts_contract DROP CONSTRAINT contracts_contract_sales_id_ececed8c_fk_users_user_id;
ALTER TABLE ONLY public.contracts_contract DROP CONSTRAINT contracts_contract_client_id_14fe7bca_fk_clients_client_id;
ALTER TABLE ONLY public.clients_client DROP CONSTRAINT clients_client_sales_id_f6b589ae_fk_users_user_id;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX public.users_user_user_permissions_user_id_20aca447;
DROP INDEX public.users_user_user_permissions_permission_id_0b93982e;
DROP INDEX public.users_user_groups_user_id_5f6f5a90;
DROP INDEX public.users_user_groups_group_id_9afc8d0e;
DROP INDEX public.users_user_email_243f6e77_like;
DROP INDEX public.events_event_support_id_32d9d666;
DROP INDEX public.events_event_client_id_dc0c6190;
DROP INDEX public.django_session_session_key_c0390e0f_like;
DROP INDEX public.django_session_expire_date_a5c62663;
DROP INDEX public.django_admin_log_user_id_c564eba6;
DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX public.contracts_contract_sales_id_ececed8c;
DROP INDEX public.contracts_contract_client_id_14fe7bca;
DROP INDEX public.clients_client_sales_id_f6b589ae;
DROP INDEX public.auth_permission_content_type_id_2f476e4b;
DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX public.auth_group_name_a6ea08ec_like;
ALTER TABLE ONLY public.users_user_user_permissions DROP CONSTRAINT users_user_user_permissions_user_id_permission_id_43338c45_uniq;
ALTER TABLE ONLY public.users_user_user_permissions DROP CONSTRAINT users_user_user_permissions_pkey;
ALTER TABLE ONLY public.users_user DROP CONSTRAINT users_user_pkey;
ALTER TABLE ONLY public.users_user_groups DROP CONSTRAINT users_user_groups_user_id_group_id_b88eab82_uniq;
ALTER TABLE ONLY public.users_user_groups DROP CONSTRAINT users_user_groups_pkey;
ALTER TABLE ONLY public.users_user DROP CONSTRAINT users_user_email_key;
ALTER TABLE ONLY public.events_event DROP CONSTRAINT events_event_pkey;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public.contracts_contract DROP CONSTRAINT contracts_contract_pkey;
ALTER TABLE ONLY public.clients_client DROP CONSTRAINT clients_client_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
DROP TABLE public.users_user_user_permissions;
DROP TABLE public.users_user_groups;
DROP TABLE public.users_user;
DROP TABLE public.events_event;
DROP TABLE public.django_session;
DROP TABLE public.django_migrations;
DROP TABLE public.django_content_type;
DROP TABLE public.django_admin_log;
DROP TABLE public.contracts_contract;
DROP TABLE public.clients_client;
DROP TABLE public.auth_permission;
DROP TABLE public.auth_group_permissions;
DROP TABLE public.auth_group;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: clients_client; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.clients_client (
    id bigint NOT NULL,
    first_name character varying(25) NOT NULL,
    last_name character varying(25) NOT NULL,
    email character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    mobile character varying(20) NOT NULL,
    company_name character varying(250) NOT NULL,
    is_client boolean NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_updated timestamp with time zone NOT NULL,
    sales_id bigint
);


ALTER TABLE public.clients_client OWNER TO admin;

--
-- Name: clients_client_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.clients_client ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.clients_client_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: contracts_contract; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.contracts_contract (
    id bigint NOT NULL,
    status boolean NOT NULL,
    amount double precision NOT NULL,
    payment_due timestamp with time zone,
    date_created timestamp with time zone NOT NULL,
    date_updated timestamp with time zone NOT NULL,
    client_id bigint,
    sales_id bigint
);


ALTER TABLE public.contracts_contract OWNER TO admin;

--
-- Name: contracts_contract_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.contracts_contract ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.contracts_contract_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- Name: events_event; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.events_event (
    id bigint NOT NULL,
    status boolean NOT NULL,
    attendees integer NOT NULL,
    event_date timestamp with time zone NOT NULL,
    notes text NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_updated timestamp with time zone NOT NULL,
    client_id bigint,
    support_id bigint
);


ALTER TABLE public.events_event OWNER TO admin;

--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.events_event ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.events_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    email character varying(60) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    phone character varying(12) NOT NULL,
    mobile character varying(12) NOT NULL,
    role character varying(12) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL,
    is_superuser boolean NOT NULL
);


ALTER TABLE public.users_user OWNER TO admin;

--
-- Name: users_user_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_user_groups OWNER TO admin;

--
-- Name: users_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_user_user_permissions OWNER TO admin;

--
-- Name: users_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group (id, name) FROM stdin;
1	STAFF
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
1	1	32
2	1	33
3	1	34
4	1	35
5	1	36
6	1	12
7	1	21
8	1	22
9	1	23
10	1	24
11	1	25
12	1	26
13	1	27
14	1	28
15	1	29
16	1	30
17	1	31
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	6	add_user
22	Can change user	6	change_user
23	Can delete user	6	delete_user
24	Can view user	6	view_user
25	Can add client	7	add_client
26	Can change client	7	change_client
27	Can delete client	7	delete_client
28	Can view client	7	view_client
29	Can add contract	8	add_contract
30	Can change contract	8	change_contract
31	Can delete contract	8	delete_contract
32	Can view contract	8	view_contract
33	Can add event	9	add_event
34	Can change event	9	change_event
35	Can delete event	9	delete_event
36	Can view event	9	view_event
\.


--
-- Data for Name: clients_client; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.clients_client (id, first_name, last_name, email, phone, mobile, company_name, is_client, date_created, date_updated, sales_id) FROM stdin;
2	prospect_2_first_name	prospect_2_last_name	prospect_2@email.com	06XXXXXXXX		prospect_2_company_name	f	2022-10-06 17:43:04.100975+02	2022-10-06 17:43:04.103173+02	4
1	client_1_first_name	client_1_last_name	client_1@email.com	06XXXXXXXX		client_1_company_name	t	2022-10-06 17:39:11.748097+02	2022-10-06 17:39:11.750264+02	3
\.


--
-- Data for Name: contracts_contract; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.contracts_contract (id, status, amount, payment_due, date_created, date_updated, client_id, sales_id) FROM stdin;
1	t	20000	2022-10-27 02:00:00+02	2022-10-06 17:54:07.585427+02	2022-10-06 17:54:07.588506+02	1	3
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2022-10-06 15:47:14.507068+02	1	STAFF	1	[{"added": {}}]	3	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	users	user
7	clients	client
8	contracts	contract
9	events	event
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2022-10-06 18:26:18.08079+02
2	contenttypes	0002_remove_content_type_name	2022-10-06 18:26:18.087924+02
3	auth	0001_initial	2022-10-06 18:26:18.116854+02
4	auth	0002_alter_permission_name_max_length	2022-10-06 18:26:18.12157+02
5	auth	0003_alter_user_email_max_length	2022-10-06 18:26:18.127785+02
6	auth	0004_alter_user_username_opts	2022-10-06 18:26:18.133273+02
7	auth	0005_alter_user_last_login_null	2022-10-06 18:26:18.138396+02
8	auth	0006_require_contenttypes_0002	2022-10-06 18:26:18.140021+02
9	auth	0007_alter_validators_add_error_messages	2022-10-06 18:26:18.145501+02
10	auth	0008_alter_user_username_max_length	2022-10-06 18:26:18.152075+02
11	auth	0009_alter_user_last_name_max_length	2022-10-06 18:26:18.157334+02
12	auth	0010_alter_group_name_max_length	2022-10-06 18:26:18.163265+02
13	auth	0011_update_proxy_permissions	2022-10-06 18:26:18.168646+02
14	auth	0012_alter_user_first_name_max_length	2022-10-06 18:26:18.174522+02
15	users	0001_initial	2022-10-06 18:26:18.247225+02
16	admin	0001_initial	2022-10-06 18:26:18.265169+02
17	admin	0002_logentry_remove_auto_add	2022-10-06 18:26:18.272552+02
18	admin	0003_logentry_add_action_flag_choices	2022-10-06 18:26:18.280338+02
19	clients	0001_initial	2022-10-06 18:26:18.285838+02
20	clients	0002_initial	2022-10-06 18:26:18.29733+02
21	contracts	0001_initial	2022-10-06 18:26:18.314336+02
22	contracts	0002_initial	2022-10-06 18:26:18.327126+02
23	events	0001_initial	2022-10-06 18:26:18.344069+02
24	events	0002_initial	2022-10-06 18:26:18.358455+02
25	sessions	0001_initial	2022-10-06 18:26:18.36608+02
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
da00zxx3n2n5vfep6q29dod8qchq2f45	.eJxVjEEOwiAQRe_C2hCgMBSX7j0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnEWRpx-N8L0yG0HfMd2m2Wa27pMJHdFHrTL68z5eTncv4OKvX7rMhqPEIwySpPXQBZMAhuCKkGTc0iaBwZV2AYXiJ0aKQ0aindJewPi_QG6Szbk:1ogSit:yis1mk5C7C_eu33OPzTp5xcUAfj9uOnDRGyJCnkzbMo	2022-10-20 17:23:43.452172+02
w47wlyw99eb7lqkajyqlpb4g0yrpjem7	.eJxVjMsOwiAQRf-FtSHQ8nBcuvcbyMAMUjWQlHZl_HfbpAvd3nPOfYuA61LC2nkOE4mLGMXpd4uYnlx3QA-s9yZTq8s8Rbkr8qBd3hrx63q4fwcFe9lqNdpsvdZszwM5BQmtAm-SV461ZaQc0WejtANmMHkAzxTZ0QhbmaL4fAHQdjgW:1ogT2U:vtZSWWnUgNJUlgmV81GZFCUdbWbzf5cN72iSV2jWJsU	2022-10-20 17:43:58.409382+02
ka5geqlodjf888psvwxaerhv37kw7y2h	.eJxVjEEOwiAQRe_C2pCBKUhduu8ZyDCMUjU0Ke3KeHfbpAvd_vfef6tI61Li2mSOY1YXZdTpd0vET6k7yA-q90nzVJd5THpX9EGbHqYsr-vh_h0UamWr0SZkDtyziD9T6KwBm4kSISALBs-ARIH9rQOwshHrxDkk5B4Mq88X-w44YA:1ogRqc:5MjSmBoNzi5H4C29ZNx9p5GhaODTGvHBwt0SiZ1VG8I	2022-10-20 16:27:38.483627+02
45om6bzirt5em84b2m0arw6zw4irjlzz	.eJxVjEEOwiAQRe_C2hCgMBSX7j0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnEWRpx-N8L0yG0HfMd2m2Wa27pMJHdFHrTL68z5eTncv4OKvX7rMhqPEIwySpPXQBZMAhuCKkGTc0iaBwZV2AYXiJ0aKQ0aindJewPi_QG6Szbk:1ogTkA:Bs3tbZtFqPu0WRt5f1beZpxkycH4BF_2rAi7qTaEH38	2022-10-20 18:29:06.926154+02
\.


--
-- Data for Name: events_event; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.events_event (id, status, attendees, event_date, notes, date_created, date_updated, client_id, support_id) FROM stdin;
1	t	15000	2022-10-27 02:00:00+02	Some notes for this special event	2022-10-06 17:55:48.453728+02	2022-10-06 17:55:48.455603+02	1	3
\.


--
-- Data for Name: users_user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user (id, password, last_login, email, first_name, last_name, phone, mobile, role, date_created, is_active, is_staff, is_superuser) FROM stdin;
1	pbkdf2_sha256$390000$KfuRAqJBRs7OaKSgGU9Q2T$D4DJ51IyCuZhsZ0BmFgXoglYxD+CkCCd1wZp11ZQ7WQ=	2022-10-06 17:16:44.280705+02	admin@admin.com	admin	admin			STAFF	2022-10-06 15:44:37.51153+02	t	t	t
5	pbkdf2_sha256$390000$me9Sw6IFzQz8sx9eLvCAj8$gzcnErSvGzgOCL8lzVGMuSCvI/yGdrrd4vtyanQfqFE=	\N	support_1@email.com	support_1_first_name	support_1_last_name	06XXXXXXXX		SUPPORT	2022-10-06 17:27:44.11184+02	t	f	f
6	pbkdf2_sha256$390000$pxEXVSVwBs98Q9M7P8AS1d$uBSGj9iulvTD6FeOSoAfiNM4hWnpAjlDXIwlNR4EkM4=	\N	support_2@email.com	support_2_first_name	support_2_last_name	06XXXXXXXX		SUPPORT	2022-10-06 17:29:04.962873+02	t	f	f
4	pbkdf2_sha256$390000$QXFQXjnODSDirVNGp1bPJ4$ftYngFdTbVjGSpuswlqNGMepf9PYzBs3nVOceyuRkSQ=	2022-10-06 17:40:09.86475+02	sales_2@email.com	sales_2_first_name	sales_2_last_name	06XXXXXXXX		SALES	2022-10-06 17:27:09.715618+02	t	f	f
3	pbkdf2_sha256$390000$33gb3Gb8Nz3i1Em01fg5Te$qq5KJndwwlZja1Px3AAt0aTScITFMnPbZaIRmyDuR+o=	2022-10-06 17:43:58.406663+02	sales_1@email.com	sales_1_first_name	sales_1_last_name	06XXXXXXXX		SALES	2022-10-06 17:26:18.958178+02	t	f	f
2	pbkdf2_sha256$390000$0rh9Hgjy5iBo09WMwFRGv7$5aTMlRu/mVJQemnJ2jvj1VesvJ+XjwhoV4aekUH540g=	2022-10-06 18:29:06.923908+02	staff@staff.com	staff_first_name	staff_last_name			STAFF	2022-10-06 17:23:21.46691+02	t	t	f
\.


--
-- Data for Name: users_user_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user_groups (id, user_id, group_id) FROM stdin;
1	2	1
\.


--
-- Data for Name: users_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 17, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 36, true);


--
-- Name: clients_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.clients_client_id_seq', 1, false);


--
-- Name: contracts_contract_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.contracts_contract_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 9, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 25, true);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.events_event_id_seq', 1, false);


--
-- Name: users_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_groups_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- Name: users_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_user_permissions_id_seq', 1, false);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: clients_client clients_client_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.clients_client
    ADD CONSTRAINT clients_client_pkey PRIMARY KEY (id);


--
-- Name: contracts_contract contracts_contract_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.contracts_contract
    ADD CONSTRAINT contracts_contract_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: events_event events_event_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.events_event
    ADD CONSTRAINT events_event_pkey PRIMARY KEY (id);


--
-- Name: users_user users_user_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_email_key UNIQUE (email);


--
-- Name: users_user_groups users_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_pkey PRIMARY KEY (id);


--
-- Name: users_user_groups users_user_groups_user_id_group_id_b88eab82_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_user_id_group_id_b88eab82_uniq UNIQUE (user_id, group_id);


--
-- Name: users_user users_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_pkey PRIMARY KEY (id);


--
-- Name: users_user_user_permissions users_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_user_user_permissions users_user_user_permissions_user_id_permission_id_43338c45_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_user_id_permission_id_43338c45_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: clients_client_sales_id_f6b589ae; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX clients_client_sales_id_f6b589ae ON public.clients_client USING btree (sales_id);


--
-- Name: contracts_contract_client_id_14fe7bca; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX contracts_contract_client_id_14fe7bca ON public.contracts_contract USING btree (client_id);


--
-- Name: contracts_contract_sales_id_ececed8c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX contracts_contract_sales_id_ececed8c ON public.contracts_contract USING btree (sales_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: events_event_client_id_dc0c6190; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX events_event_client_id_dc0c6190 ON public.events_event USING btree (client_id);


--
-- Name: events_event_support_id_32d9d666; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX events_event_support_id_32d9d666 ON public.events_event USING btree (support_id);


--
-- Name: users_user_email_243f6e77_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_email_243f6e77_like ON public.users_user USING btree (email varchar_pattern_ops);


--
-- Name: users_user_groups_group_id_9afc8d0e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_groups_group_id_9afc8d0e ON public.users_user_groups USING btree (group_id);


--
-- Name: users_user_groups_user_id_5f6f5a90; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_groups_user_id_5f6f5a90 ON public.users_user_groups USING btree (user_id);


--
-- Name: users_user_user_permissions_permission_id_0b93982e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_user_permissions_permission_id_0b93982e ON public.users_user_user_permissions USING btree (permission_id);


--
-- Name: users_user_user_permissions_user_id_20aca447; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_user_permissions_user_id_20aca447 ON public.users_user_user_permissions USING btree (user_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: clients_client clients_client_sales_id_f6b589ae_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.clients_client
    ADD CONSTRAINT clients_client_sales_id_f6b589ae_fk_users_user_id FOREIGN KEY (sales_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contracts_contract contracts_contract_client_id_14fe7bca_fk_clients_client_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.contracts_contract
    ADD CONSTRAINT contracts_contract_client_id_14fe7bca_fk_clients_client_id FOREIGN KEY (client_id) REFERENCES public.clients_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contracts_contract contracts_contract_sales_id_ececed8c_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.contracts_contract
    ADD CONSTRAINT contracts_contract_sales_id_ececed8c_fk_users_user_id FOREIGN KEY (sales_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event events_event_client_id_dc0c6190_fk_clients_client_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.events_event
    ADD CONSTRAINT events_event_client_id_dc0c6190_fk_clients_client_id FOREIGN KEY (client_id) REFERENCES public.clients_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event events_event_support_id_32d9d666_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.events_event
    ADD CONSTRAINT events_event_support_id_32d9d666_fk_users_user_id FOREIGN KEY (support_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_groups users_user_groups_group_id_9afc8d0e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_group_id_9afc8d0e_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_groups users_user_groups_user_id_5f6f5a90_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_user_id_5f6f5a90_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_user_permissions users_user_user_perm_permission_id_0b93982e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_perm_permission_id_0b93982e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_user_permissions users_user_user_permissions_user_id_20aca447_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_user_id_20aca447_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

