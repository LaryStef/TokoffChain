-- REPLACE dbname, rolename, password with your values from .env

CREATE DATABASE dbname WITH OWNER rolename ENCODING 'UTF8';
CREATE ROLE rolename WITH NOCREATEDB NOCREATEROLE NOREPLICATION LOGIN PASSWORD password;
GRANT ALL PRIVILEGES ON DATABASE dbname TO rolename;
