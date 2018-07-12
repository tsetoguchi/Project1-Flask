-- Adminer 4.6.3-dev PostgreSQL dump

\connect "d7lmc0jhphip5p";

DROP TABLE IF EXISTS "checkins";
CREATE TABLE "public"."checkins" (
    "comment" character varying NOT NULL,
    "visit" integer DEFAULT '0' NOT NULL,
    "location" character varying NOT NULL,
    "zipcode" character varying NOT NULL,
    "username" character varying NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "logins";
DROP SEQUENCE IF EXISTS logins_id_seq;
CREATE SEQUENCE logins_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."logins" (
    "id" integer DEFAULT nextval('logins_id_seq') NOT NULL,
    "username" character varying NOT NULL,
    "password" character varying NOT NULL,
    "email" character varying NOT NULL,
    CONSTRAINT "logins_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "zips";
CREATE TABLE "public"."zips" (
    "zipcode" character varying NOT NULL,
    "city" character varying NOT NULL,
    "state" character varying NOT NULL,
    "lat" numeric NOT NULL,
    "long" numeric NOT NULL,
    "population" integer NOT NULL
) WITH (oids = false);


-- 2018-07-12 21:14:20.071804+00
