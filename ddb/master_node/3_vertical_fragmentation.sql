-- Create the kategori_barang table
CREATE TABLE "kategori_barang" (
    "id_kategori" INTEGER PRIMARY KEY,
    "nama_kategori" VARCHAR(45) NOT NULL
);

-- Create the barang table (most frequently accesed columns)
CREATE TABLE "barang_core" (
    "id_barang" INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "id_kategori" INTEGER,
    "nama_barang" VARCHAR(225) NOT NULL,
    "harga" FLOAT NOT NULL,
    FOREIGN KEY ("id_kategori") REFERENCES "kategori_barang" ("id_kategori")
);

-- Foreign Table: Barang (Less frequent accesed columns)
CREATE FOREIGN TABLE "barang_detail" (
    "id_barang" INTEGER,
    "deskripsi_barang" TEXT,
    "berat" FLOAT,
    "panjang" FLOAT,
    "lebar" FLOAT,
    "tinggi" FLOAT
) SERVER server_3 OPTIONS (schema_name 'public', table_name 'barang_detail');

-- View Table: Barang
CREATE VIEW "barang" AS
SELECT
    bc.id_barang,
    bc.id_kategori,
    bc.nama_barang,
    bc.harga,
    bd.deskripsi_barang,
    bd.berat,
    bd.panjang,
    bd.lebar,
    bd.tinggi
FROM barang_core bc
LEFT JOIN barang_detail bd
ON bc.id_barang = bd.id_barang;

-- Trigger: View table of products
CREATE OR REPLACE FUNCTION update_barang()
RETURNS TRIGGER AS $$
DECLARE var_id_barang INTEGER;
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO barang_core (id_kategori, nama_barang, harga)
        VALUES (NEW.id_kategori, NEW.nama_barang, NEW.harga)
        RETURNING id_barang INTO var_id_barang;

        INSERT INTO barang_detail (id_barang, deskripsi_barang, berat, panjang, lebar, tinggi)
        VALUES (
            var_id_barang, NEW.deskripsi_barang, NEW.berat, NEW.panjang, NEW.lebar, NEW.tinggi
        );

        NEW.id_barang := var_id_barang;

        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE barang_core
        SET id_kategori = NEW.id_kategori, nama_barang = NEW.nama_barang, harga = NEW.harga
        WHERE id_barang = NEW.id_barang;

        UPDATE barang_detail
        SET deskripsi_barang = NEW.deskripsi_barang, berat = NEW.berat, panjang = NEW.panjang, lebar = NEW.lebar, tinggi = NEW.tinggi
        WHERE id_barang = NEW.id_barang;

        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        DELETE FROM barang_detail WHERE id_barang = OLD.id_barang;
        DELETE FROM barang_core WHERE id_barang = OLD.id_barang;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_barang
INSTEAD OF INSERT OR UPDATE OR DELETE
ON barang
FOR EACH ROW
EXECUTE FUNCTION update_barang();