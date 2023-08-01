--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dir_sat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dir_sat (
    rfc text NOT NULL,
    r_social text,
    rubro_aut text,
    entidad_fed text,
    rep_legales text,
    correo_electronico text,
    domicilio text,
    f_oficio text,
    oficio text,
    anio_directorio smallint,
    telefono text,
    f_inscr text,
    fig_jur_cluni text,
    edad smallint
);


ALTER TABLE public.dir_sat OWNER TO postgres;

--
-- Name: itr; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr (
    rfc text NOT NULL,
    id text NOT NULL,
    anio_informe smallint,
    anio_autorizacion smallint,
    mision text,
    vision text,
    socios_asoc text,
    categoria_ppal text,
    plant_laboral real,
    plant_voluntarios integer,
    mto_plant_laboral real,
    activo real,
    pasivo real,
    capital real,
    gastos_adm real,
    gastos_rep real,
    gastos_ope real,
    sit_fiscal text,
    aut_ext boolean,
    estatus text,
    patrimonio real,
    act_legislativas boolean,
    web text,
    entidad_fed text,
    rubros_aut text
);


ALTER TABLE public.itr OWNER TO postgres;

--
-- Name: TABLE itr; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr IS 'Tabla con información base de informes de transparencia';


--
-- Name: itr_ctrl_donat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_ctrl_donat (
    id_itr text NOT NULL,
    id_donat_esp text,
    bienes_rec text,
    q_rec integer,
    q_cuotas_recup integer,
    mto_cuotas_recup real,
    cant_destruc integer,
    f_destruc date,
    remanente integer
);


ALTER TABLE public.itr_ctrl_donat OWNER TO postgres;

--
-- Name: TABLE itr_ctrl_donat; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr_ctrl_donat IS 'Control de donativos - Informe de Transparencia';


--
-- Name: itr_donat_otorgados; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_donat_otorgados (
    id_itr text NOT NULL,
    benef text,
    mto_total real,
    rfc_donante text,
    rfc_donataria text,
    mto_efe real,
    mto_esp real
);


ALTER TABLE public.itr_donat_otorgados OWNER TO postgres;

--
-- Name: TABLE itr_donat_otorgados; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr_donat_otorgados IS 'Donativos otorgados - Informe de Transparencia';


--
-- Name: itr_gastos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_gastos (
    id_itr text NOT NULL,
    concepto text,
    detalle_concepto text,
    mto_nac_ope real,
    mto_nac_adm real,
    mto_ext_ope real,
    mto_ext_adm real,
    mto_total bigint
);


ALTER TABLE public.itr_gastos OWNER TO postgres;

--
-- Name: itr_ing_donat_rec; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_ing_donat_rec (
    id_itr text NOT NULL,
    tipo_ingreso text,
    monto real,
    tipo_donante text,
    concepto text,
    donat_esp text
);


ALTER TABLE public.itr_ing_donat_rec OWNER TO postgres;

--
-- Name: TABLE itr_ing_donat_rec; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr_ing_donat_rec IS 'Ingresos + Donativos recibidos - Informe de Transparencia';


--
-- Name: itr_inv_finan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_inv_finan (
    id_itr text NOT NULL,
    concepto text,
    mto_ext bigint,
    mto_nac bigint
);


ALTER TABLE public.itr_inv_finan OWNER TO postgres;

--
-- Name: TABLE itr_inv_finan; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr_inv_finan IS 'Inversiones financieras - Informe de Transparencia';


--
-- Name: itr_nec_atend; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_nec_atend (
    id_itr text NOT NULL,
    concepto text,
    num_benef bigint,
    entidad_fed text,
    municipio text,
    sect_benef text,
    monto real
);


ALTER TABLE public.itr_nec_atend OWNER TO postgres;

--
-- Name: TABLE itr_nec_atend; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr_nec_atend IS 'Necesidades atendidas - Informe de Transparencia';


--
-- Name: itr_org_gob; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_org_gob (
    id_itr text NOT NULL,
    nombre text,
    puesto text,
    salario real
);


ALTER TABLE public.itr_org_gob OWNER TO postgres;

--
-- Name: TABLE itr_org_gob; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr_org_gob IS 'Organo de gobierno - Informe de Transparencia';


--
-- Name: itr_sect_benef; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_sect_benef (
    id_itr text NOT NULL,
    id_donat_esp integer,
    sect_benef text,
    cant integer
);


ALTER TABLE public.itr_sect_benef OWNER TO postgres;

--
-- Name: TABLE itr_sect_benef; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr_sect_benef IS 'Sector beneficiado - Informe de Transparencia';


--
-- Name: itr_transm_patr; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itr_transm_patr (
    id_itr text NOT NULL,
    rfc_donante text,
    rfc_donataria text,
    raz_soc_dest text,
    mto_efe real,
    mto_esp real
);


ALTER TABLE public.itr_transm_patr OWNER TO postgres;

--
-- Name: TABLE itr_transm_patr; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.itr_transm_patr IS 'Transmisión de patrimonio - Informe de Transparencia';


--
-- Name: org; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.org (
    rfc text NOT NULL,
    r_social text,
    categoria text,
    subcategoria text,
    domicilio text,
    localidad text,
    rubro_aut text,
    f_constit date,
    f_insc_cluni date,
    mision text,
    vision text,
    web text,
    telefono text,
    entidad_fed text,
    codigo_postal text,
    cluni text,
    figura_jur_cluni text,
    ult_anio_sat smallint,
    ult_anio_rda smallint,
    ult_anio_itr smallint,
    rep_legales text,
    correo_electronico text,
    oficio text,
    f_oficio text,
    tipo text
);


ALTER TABLE public.org OWNER TO postgres;

--
-- Name: TABLE org; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.org IS 'Tabla con información base de las organizaciones';


--
-- Name: rda; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rda (
    rfc text NOT NULL,
    anio_reporte smallint,
    donat_ef_local bigint,
    donat_ef_ext bigint,
    donat_esp_loc bigint,
    ing_arrend bigint,
    ing_div bigint,
    ing_regalias bigint,
    ing_inter_dev bigint,
    ing_otros bigint,
    sueldos_salarios_gastos bigint,
    aport_infonavit_jub bigint,
    cuotas_imss bigint,
    gastos_ope_leg bigint,
    gastos_adm_leg bigint,
    gastos_adm_ext bigint,
    gastos_adm_nac bigint,
    gastos_ope_nac bigint,
    gastos_ope_ext bigint,
    donat_esp_ext bigint
);


ALTER TABLE public.rda OWNER TO postgres;


