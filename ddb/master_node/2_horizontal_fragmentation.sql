-- Create the gudang table
CREATE TABLE "gudang" (
    "id_gudang" INTEGER,
    "alamat" VARCHAR(255) NOT NULL,
    "kota" VARCHAR(100) NOT NULL,
    "provinsi" VARCHAR(100) NOT NULL,
    "kode_pos" VARCHAR(10) NOT NULL
) PARTITION BY LIST ("id_gudang");

-- Create the stok_barang table
CREATE TABLE "stok_barang" (
    "id_barang" INTEGER,
    "id_gudang" INTEGER,
    "stok" INTEGER NOT NULL,
    "tanggal_diperbarui" TIMESTAMP NOT NULL
) PARTITION BY LIST ("id_gudang");

-- Create the order table
CREATE TABLE "order_customer" (
    "id_order" INTEGER GENERATED ALWAYS AS IDENTITY,
    "id_gudang" INTEGER,
    "tanggal_order" TIMESTAMP DEFAULT NOW() NOT NULL,
    "id_customer" INTEGER NOT NULL
) PARTITION BY LIST ("id_gudang");

-- Create supplier shipment item table
CREATE TABLE "restok_barang" (
    "id_restok" INTEGER GENERATED ALWAYS AS IDENTITY,
    "id_barang" INTEGER,
    "id_gudang" INTEGER,
    "id_supplier" INTEGER,
    "jumlah" INTEGER NOT NULL,
    "tanggal_restok" TIMESTAMP DEFAULT NOW() NOT NULL
) PARTITION BY LIST ("id_gudang");

-- Foreign Table: gudang surabaya (server 1)
CREATE FOREIGN TABLE "gudang_surabaya" PARTITION OF "gudang" FOR VALUES IN (1)
SERVER server_1 OPTIONS (schema_name 'public', table_name 'gudang');
CREATE FOREIGN TABLE "stok_barang_surabaya" PARTITION OF "stok_barang" FOR VALUES IN (1)
SERVER server_1 OPTIONS (schema_name 'public', table_name 'stok_barang');
CREATE FOREIGN TABLE "order_customer_surabaya" PARTITION OF "order_customer" FOR VALUES IN (1)
SERVER server_1 OPTIONS (schema_name 'public', table_name 'order_customer');
CREATE FOREIGN TABLE "order_customer_item_surabaya" (
    "id_order" INTEGER,
    "id_barang" INTEGER,
    "jumlah" INTEGER
) SERVER server_1 OPTIONS (schema_name 'public', table_name 'order_customer_item');
CREATE FOREIGN TABLE "restok_barang_surabaya" PARTITION OF "restok_barang" FOR VALUES IN (1)
SERVER server_1 OPTIONS (schema_name 'public', table_name 'restok_barang');

-- Foreign Table: gudang jakarta (server 2)
CREATE FOREIGN TABLE "gudang_jakarta" PARTITION OF "gudang" FOR VALUES IN (2)
SERVER server_2 OPTIONS (schema_name 'public', table_name 'gudang');
CREATE FOREIGN TABLE "stok_barang_jakarta" PARTITION OF "stok_barang" FOR VALUES IN (2)
SERVER server_2 OPTIONS (schema_name 'public', table_name 'stok_barang');
CREATE FOREIGN TABLE "order_customer_jakarta" PARTITION OF "order_customer" FOR VALUES IN (2)
SERVER server_2 OPTIONS (schema_name 'public', table_name 'order_customer');
CREATE FOREIGN TABLE "order_customer_item_jakarta" (
    "id_order" INTEGER,
    "id_barang" INTEGER,
    "jumlah" INTEGER
) SERVER server_2 OPTIONS (schema_name 'public', table_name 'order_customer_item');
CREATE FOREIGN TABLE "restok_barang_jakarta" PARTITION OF "restok_barang" FOR VALUES IN (2)
SERVER server_2 OPTIONS (schema_name 'public', table_name 'restok_barang');

CREATE VIEW "order_customer_item" AS
SELECT * FROM "order_customer_item_surabaya"
UNION
SELECT * FROM "order_customer_item_jakarta";

-- Trigger: View table of products
CREATE OR REPLACE FUNCTION order_customer_item()
RETURNS TRIGGER AS $$
DECLARE var_id_gudang INTEGER;
DECLARE var_tanggal_order TIMESTAMP;
BEGIN
    SELECT id_gudang FROM order_customer WHERE id_order = NEW.id_order INTO var_id_gudang;
    SELECT tanggal_order FROM order_customer WHERE id_order = NEW.id_order INTO var_tanggal_order;

    IF TG_OP = 'INSERT' THEN

        IF var_id_gudang = 1 THEN
            INSERT INTO "order_customer_item_surabaya" VALUES (NEW.*);
        
        ELSIF var_id_gudang = 2 THEN
            INSERT INTO "order_customer_item_jakarta" VALUES (NEW.*);

        END IF;

        UPDATE stok_barang
        SET stok = stok - NEW.jumlah, tanggal_diperbarui = var_tanggal_order
        WHERE id_barang = NEW.id_barang AND id_gudang = var_id_gudang;

    ELSIF TG_OP = 'UPDATE' THEN
        IF var_id_gudang = 1 THEN
            UPDATE "order_customer_item_surabaya"
            SET jumlah = NEW.jumlah
            WHERE id_order = NEW.id_order AND id_barang = NEW.id_barang;

        ELSIF var_id_gudang = 2 THEN
            UPDATE "order_customer_item_jakarta"
            SET jumlah = NEW.jumlah
            WHERE id_order = NEW.id_order AND id_barang = NEW.id_barang;

        END IF;

        UPDATE stok_barang
        SET stok = stok + (OLD.jumlah - NEW.jumlah)
        WHERE id_barang = OLD.id_barang AND id_gudang = var_id_gudang;

    ELSIF TG_OP = 'DELETE' THEN
        SELECT id_gudang FROM order_customer WHERE id_order = OLD.id_order INTO var_id_gudang;

        IF var_id_gudang = 1 THEN
            DELETE FROM "order_customer_item_surabaya" WHERE id_order = OLD.id_order AND id_barang = OLD.id_barang;

        ELSIF var_id_gudang = 2 THEN
            DELETE FROM "order_customer_item_jakarta" WHERE id_order = OLD.id_order AND id_barang = OLD.id_barang;

        END iF;

        UPDATE stok_barang
        SET stok = stok + OLD.jumlah
        WHERE id_barang = OLD.id_barang AND id_gudang = var_id_gudang;

    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_order_customer_item
INSTEAD OF INSERT OR UPDATE OR DELETE
ON order_customer_item
FOR EACH ROW
EXECUTE FUNCTION order_customer_item();

-- Trigger Restok barang
CREATE OR REPLACE FUNCTION update_restok_barang()
RETURNS TRIGGER AS $$
DECLARE var_row_count INTEGER;
BEGIN
    -- Is stok exists
    SELECT COUNT(1)
    FROM stok_barang
    WHERE id_barang = NEW.id_barang AND id_gudang = NEW.id_gudang
    INTO var_row_count;

    IF var_row_count != 0 THEN
        UPDATE stok_barang
        SET stok = stok + NEW.jumlah, tanggal_diperbarui = NEW.tanggal_restok
        WHERE id_barang = NEW.id_barang AND id_gudang = NEW.id_gudang;
    ELSE
        INSERT INTO stok_barang ("id_barang", "id_gudang", "stok", "tanggal_diperbarui")
        VALUES (NEW.id_barang, NEW.id_gudang, NEW.jumlah, NEW.tanggal_restok);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_restok_barang
BEFORE INSERT
ON restok_barang
FOR EACH ROW
EXECUTE FUNCTION update_restok_barang();

-- -- Trigger order customer
-- CREATE OR REPLACE FUNCTION update_order_customer_item()
-- RETURNS TRIGGER AS $$
-- DECLARE var_id_gudang INTEGER;
-- DECLARE var_tanggal_order TIMESTAMP;
-- BEGIN
--     SELECT id_gudang FROM order_customer WHERE id_order = NEW.id_order INTO var_id_gudang;
--     SELECT tanggal_order FROM order_customer WHERE id_order = NEW.id_order INTO var_tanggal_order;

--     UPDATE stok_barang
--     SET stok = stok - NEW.jumlah, tanggal_diperbarui = var_tanggal_order
--     WHERE id_barang = NEW.id_barang AND id_gudang = var_id_gudang;
    
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER trigger_restok_barang
-- BEFORE INSERT
-- ON order_customer_item
-- FOR EACH ROW
-- EXECUTE FUNCTION update_order_customer_item();