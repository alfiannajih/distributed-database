ALTER SYSTEM SET max_logical_replication_workers = 16;

-- Create the kategori_barang table
CREATE TABLE "kategori_barang" (
    "id_kategori" INTEGER PRIMARY KEY,
    "nama_kategori" VARCHAR(45) NOT NULL
);

-- Create the barang table
CREATE TABLE "barang_core" (
    "id_barang" INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "id_kategori" INTEGER,
    "nama_barang" VARCHAR(225) NOT NULL,
    "harga" FLOAT NOT NULL,
    FOREIGN KEY ("id_kategori") REFERENCES "kategori_barang" ("id_kategori")
);

-- Create the gudang table
CREATE TABLE "gudang" (
    "id_gudang" INTEGER PRIMARY KEY,
    "alamat" VARCHAR(255) NOT NULL,
    "kota" VARCHAR(100) NOT NULL,
    "provinsi" VARCHAR(100) NOT NULL,
    "kode_pos" VARCHAR(10) NOT NULL
);

-- Create the stok_barang table
CREATE TABLE "stok_barang" (
    "id_barang" INTEGER,
    "id_gudang" INTEGER,
    "stok" INTEGER NOT NULL,
    "tanggal_diperbarui" TIMESTAMP NOT NULL,
    PRIMARY KEY ("id_barang", "id_gudang"),
    FOREIGN KEY ("id_barang") REFERENCES "barang_core" ("id_barang"),
    FOREIGN KEY ("id_gudang") REFERENCES "gudang" ("id_gudang")
);

-- Create the customer table (Revised User table)
CREATE TABLE "customer" (
    "id_customer" INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nama" VARCHAR(225) NOT NULL,
    "alamat" VARCHAR(225),
    "no_telp" VARCHAR(15)
);

-- Create the order table
CREATE TABLE "order_customer" (
    "id_order" INTEGER PRIMARY KEY,
    "id_gudang" INTEGER,
    "tanggal_order" TIMESTAMP DEFAULT NOW() NOT NULL,
    "id_customer" INTEGER NOT NULL,
    FOREIGN KEY ("id_customer") REFERENCES "customer" ("id_customer"),
    FOREIGN KEY ("id_gudang") REFERENCES "gudang" ("id_gudang")
);

-- Create the order_customer_item table (Revised orderBarang table)
CREATE TABLE "order_customer_item" (
    "id_order" INTEGER,
    "id_barang" INTEGER,
    "jumlah" INTEGER NOT NULL,
    PRIMARY KEY ("id_order", "id_barang"),
    FOREIGN KEY ("id_order") REFERENCES "order_customer" ("id_order"),
    FOREIGN KEY ("id_barang") REFERENCES "barang_core" ("id_barang")
);

-- Create supplier table
CREATE TABLE "supplier" (
    "id_supplier" INTEGER PRIMARY KEY,
    "nama_supplier" VARCHAR NOT NULL
);

-- Create restok_barnag table
CREATE TABLE "restok_barang" (
    "id_restok" INTEGER PRIMARY KEY,
    "id_barang" INTEGER,
    "id_gudang" INTEGER,
    "id_supplier" INTEGER,
    "jumlah" INTEGER NOT NULL,
    "tanggal_restok" TIMESTAMP DEFAULT NOW() NOT NULL,
    FOREIGN KEY ("id_barang") REFERENCES "barang_core" ("id_barang"),
    FOREIGN KEY ("id_gudang") REFERENCES "gudang" ("id_gudang"),
    FOREIGN KEY ("id_supplier") REFERENCES "supplier" ("id_supplier")
);