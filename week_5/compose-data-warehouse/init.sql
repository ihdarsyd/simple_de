CREATE USER analysisUser WITH PASSWORD 'qwerty123' CREATEDB;
CREATE DATABASE dvdrental_analysis
    WITH 
    OWNER = analysisUser
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;