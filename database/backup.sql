--
-- PostgreSQL database dump
--

\restrict 7rEMs8vDv3cGKnoRcuQ5oyxRAIZSrFSRn5KFJnqJ0SuVPbc2e3gRwbQ3ExCYhdZ

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-02-15 21:43:30

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 40962)
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.category OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 40961)
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.category_id_seq OWNER TO postgres;

--
-- TOC entry 4974 (class 0 OID 0)
-- Dependencies: 219
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;


--
-- TOC entry 222 (class 1259 OID 40972)
-- Name: decorators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.decorators (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    cost numeric(10,2) NOT NULL
);


ALTER TABLE public.decorators OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 40971)
-- Name: decorators_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.decorators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.decorators_id_seq OWNER TO postgres;

--
-- TOC entry 4975 (class 0 OID 0)
-- Dependencies: 221
-- Name: decorators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.decorators_id_seq OWNED BY public.decorators.id;


--
-- TOC entry 228 (class 1259 OID 41013)
-- Name: order_decorators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_decorators (
    id integer NOT NULL,
    order_id integer,
    decorator_id integer
);


ALTER TABLE public.order_decorators OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 41012)
-- Name: order_decorators_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_decorators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_decorators_id_seq OWNER TO postgres;

--
-- TOC entry 4976 (class 0 OID 0)
-- Dependencies: 227
-- Name: order_decorators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_decorators_id_seq OWNED BY public.order_decorators.id;


--
-- TOC entry 230 (class 1259 OID 41032)
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer,
    product_id integer,
    quantity smallint NOT NULL,
    subtotal numeric(10,2) NOT NULL
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 41031)
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- TOC entry 4977 (class 0 OID 0)
-- Dependencies: 229
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- TOC entry 224 (class 1259 OID 40983)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    user_id integer NOT NULL,
    total_amount numeric(10,2) NOT NULL,
    created_at timestamp without time zone DEFAULT '2026-02-15 16:11:44.930418'::timestamp without time zone
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 40982)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- TOC entry 4978 (class 0 OID 0)
-- Dependencies: 223
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- TOC entry 226 (class 1259 OID 40995)
-- Name: product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product (
    id integer NOT NULL,
    category_id integer,
    name character varying(255) NOT NULL,
    price numeric(10,2) NOT NULL,
    description text
);


ALTER TABLE public.product OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 40994)
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_id_seq OWNER TO postgres;

--
-- TOC entry 4979 (class 0 OID 0)
-- Dependencies: 225
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;


--
-- TOC entry 4780 (class 2604 OID 40965)
-- Name: category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);


--
-- TOC entry 4781 (class 2604 OID 40975)
-- Name: decorators id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.decorators ALTER COLUMN id SET DEFAULT nextval('public.decorators_id_seq'::regclass);


--
-- TOC entry 4785 (class 2604 OID 41016)
-- Name: order_decorators id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_decorators ALTER COLUMN id SET DEFAULT nextval('public.order_decorators_id_seq'::regclass);


--
-- TOC entry 4786 (class 2604 OID 41035)
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- TOC entry 4782 (class 2604 OID 40986)
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- TOC entry 4784 (class 2604 OID 40998)
-- Name: product id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);


--
-- TOC entry 4958 (class 0 OID 40962)
-- Dependencies: 220
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category (id, name) FROM stdin;
1	Электроника
2	Одежда
3	Бытовая техника
4	Книги
5	Спорт и отдых
\.


--
-- TOC entry 4960 (class 0 OID 40972)
-- Dependencies: 222
-- Data for Name: decorators; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.decorators (id, name, cost) FROM stdin;
1	Подарочная упаковка	199.00
2	Срочная доставка	499.00
3	Персонализация (гравировка)	299.00
4	Страхование товара	249.00
5	Расширенная гарантия	999.00
6	Поздравительная открытка	99.00
\.


--
-- TOC entry 4966 (class 0 OID 41013)
-- Dependencies: 228
-- Data for Name: order_decorators; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_decorators (id, order_id, decorator_id) FROM stdin;
1	1	1
2	1	4
3	2	2
4	2	6
5	3	5
6	4	1
7	4	3
8	5	2
11	9	1
12	9	2
13	9	3
\.


--
-- TOC entry 4968 (class 0 OID 41032)
-- Dependencies: 230
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, product_id, quantity, subtotal) FROM stdin;
1	1	1	1	59999.99
2	1	3	1	18999.99
3	1	11	2	9999.98
4	2	6	2	3999.98
5	2	7	1	3999.99
6	2	9	1	6999.99
7	3	2	1	124999.99
8	3	4	1	45999.99
9	3	5	1	24999.99
10	3	13	1	45999.99
11	4	16	1	999.99
12	4	17	1	799.99
13	4	18	1	899.99
14	4	19	1	699.99
15	5	21	1	29999.99
16	5	22	1	1499.99
17	5	23	1	1299.99
24	9	5	1	24999.99
25	9	10	1	5499.99
26	9	23	2	2599.98
27	9	5	1	24999.99
28	9	3	1	18999.99
29	9	2	1	124999.99
\.


--
-- TOC entry 4962 (class 0 OID 40983)
-- Dependencies: 224
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, user_id, total_amount, created_at) FROM stdin;
1	1	65998.98	2026-02-05 16:30:45.410099
2	1	12999.98	2026-02-10 16:30:45.410099
3	1	87998.97	2026-02-13 16:30:45.410099
4	2	3999.99	2026-02-08 16:30:45.410099
5	2	5499.99	2026-02-14 16:30:45.410099
9	1	203096.93	2026-02-15 16:11:44.930418
\.


--
-- TOC entry 4964 (class 0 OID 40995)
-- Dependencies: 226
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product (id, category_id, name, price, description) FROM stdin;
1	1	Смартфон Galaxy S23	59999.99	Смартфон Samsung Galaxy S23, 256GB, черный
2	1	Ноутбук ASUS ROG	124999.99	Игровой ноутбук ASUS ROG Strix, 16GB RAM, 512GB SSD
3	1	Наушники AirPods Pro	18999.99	Беспроводные наушники Apple AirPods Pro с шумоподавлением
4	1	Планшет iPad Air	45999.99	Apple iPad Air 10.9", 64GB, Wi-Fi
5	1	Умные часы Galaxy Watch	24999.99	Samsung Galaxy Watch 6, 44mm, черный
6	2	Футболка классическая	1999.99	Хлопковая футболка, белая, размер M
7	2	Джинсы прямые	3999.99	Классические джинсы, синие, размер 32
8	2	Куртка зимняя	7999.99	Теплая зимняя куртка, черная, размер L
9	2	Кроссовки Nike	6999.99	Спортивные кроссовки Nike Air Max, 42 размер
10	2	Свитер кашемировый	5499.99	Кашемировый свитер, серый, размер M
11	3	Блендер Philips	4999.99	Мощный блендер Philips HR3556, 700W
12	3	Пылесос Dyson	29999.99	Беспроводной пылесос Dyson V15
13	3	Кофемашина DeLonghi	45999.99	Автоматическая кофемашина DeLonghi Magnifica
14	3	Микроволновая печь	8999.99	Микроволновая печь Samsung, 20л, гриль
15	3	Утюг Philips	3999.99	Паровой утюг Philips Azur, 2600W
16	4	Война и мир	999.99	Лев Толстой, роман-эпопея, твердый переплет
17	4	Преступление и наказание	799.99	Федор Достоевский, классический роман
18	4	Мастер и Маргарита	899.99	Михаил Булгаков, культовый роман
19	4	1984	699.99	Джордж Оруэлл, роман-антиутопия
20	4	Маленький принц	599.99	Антуан де Сент-Экзюпери, философская сказка
21	5	Велосипед горный	29999.99	Горный велосипед, 26 дюймов, 21 скорость
22	5	Гантели 5кг	1499.99	Пара гантелей по 5 кг, резиновое покрытие
23	5	Коврик для йоги	1299.99	Коврик для йоги, нескользящий, 6мм
24	5	Мяч футбольный	1999.99	Футбольный мяч, размер 5, профессиональный
25	5	Термос	2499.99	Термос нержавеющая сталь, 1л
\.


--
-- TOC entry 4980 (class 0 OID 0)
-- Dependencies: 219
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_id_seq', 5, true);


--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 221
-- Name: decorators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.decorators_id_seq', 6, true);


--
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 227
-- Name: order_decorators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_decorators_id_seq', 13, true);


--
-- TOC entry 4983 (class 0 OID 0)
-- Dependencies: 229
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 29, true);


--
-- TOC entry 4984 (class 0 OID 0)
-- Dependencies: 223
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 9, true);


--
-- TOC entry 4985 (class 0 OID 0)
-- Dependencies: 225
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_id_seq', 25, true);


--
-- TOC entry 4788 (class 2606 OID 40969)
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- TOC entry 4791 (class 2606 OID 40980)
-- Name: decorators decorators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.decorators
    ADD CONSTRAINT decorators_pkey PRIMARY KEY (id);


--
-- TOC entry 4801 (class 2606 OID 41019)
-- Name: order_decorators order_decorators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_decorators
    ADD CONSTRAINT order_decorators_pkey PRIMARY KEY (id);


--
-- TOC entry 4804 (class 2606 OID 41040)
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- TOC entry 4795 (class 2606 OID 40992)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 4798 (class 2606 OID 41005)
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- TOC entry 4789 (class 1259 OID 40970)
-- Name: ix_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_category_id ON public.category USING btree (id);


--
-- TOC entry 4792 (class 1259 OID 40981)
-- Name: ix_decorators_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_decorators_id ON public.decorators USING btree (id);


--
-- TOC entry 4799 (class 1259 OID 41030)
-- Name: ix_order_decorators_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_decorators_id ON public.order_decorators USING btree (id);


--
-- TOC entry 4802 (class 1259 OID 41051)
-- Name: ix_order_items_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_id ON public.order_items USING btree (id);


--
-- TOC entry 4793 (class 1259 OID 40993)
-- Name: ix_orders_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_id ON public.orders USING btree (id);


--
-- TOC entry 4796 (class 1259 OID 41011)
-- Name: ix_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_id ON public.product USING btree (id);


--
-- TOC entry 4806 (class 2606 OID 41025)
-- Name: order_decorators order_decorators_decorator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_decorators
    ADD CONSTRAINT order_decorators_decorator_id_fkey FOREIGN KEY (decorator_id) REFERENCES public.decorators(id);


--
-- TOC entry 4807 (class 2606 OID 41020)
-- Name: order_decorators order_decorators_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_decorators
    ADD CONSTRAINT order_decorators_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- TOC entry 4808 (class 2606 OID 41041)
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- TOC entry 4809 (class 2606 OID 41046)
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- TOC entry 4805 (class 2606 OID 41006)
-- Name: product product_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id);


-- Completed on 2026-02-15 21:43:31

--
-- PostgreSQL database dump complete
--

\unrestrict 7rEMs8vDv3cGKnoRcuQ5oyxRAIZSrFSRn5KFJnqJ0SuVPbc2e3gRwbQ3ExCYhdZ

