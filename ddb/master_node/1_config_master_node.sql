CREATE EXTENSION IF NOT EXISTS postgres_fdw;
ALTER SYSTEM SET wal_level = logical;

ALTER SYSTEM SET max_logical_replication_workers = 16;
ALTER SYSTEM SET max_replication_slots = 32;
ALTER SYSTEM SET max_wal_senders = 16;

-- Foreign Server 1
CREATE SERVER server_1 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'postgres', host '10.42.0.86', port '5432');
CREATE USER MAPPING FOR postgres SERVER server_1 OPTIONS (user 'postgres', password 'postgres');

-- Foreign Server 2 
CREATE SERVER server_2 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'postgres', host 'node-2', port '5432');
CREATE USER MAPPING FOR postgres SERVER server_2 OPTIONS (user 'postgres', password 'postgres');

-- Foreign Server 3
CREATE SERVER server_3 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'postgres', host 'node-3', port '5432');
CREATE USER MAPPING FOR postgres SERVER server_3 OPTIONS (user 'postgres', password 'postgres');