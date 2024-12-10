-- Create the customer table (Revised User table)
CREATE TABLE "customer" (
    "id_customer" INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nama" VARCHAR(225) NOT NULL,
    "alamat" VARCHAR(225),
    "no_telp" VARCHAR(15)
);

-- Create supplier table
CREATE TABLE "supplier" (
    "id_supplier" INTEGER PRIMARY KEY,
    "nama_supplier" VARCHAR NOT NULL
);

-- Replicate: Kategori
CREATE PUBLICATION kategori_pub FOR TABLE kategori_barang;

-- Replicate: Products
CREATE PUBLICATION barang_pub FOR TABLE barang_core;

-- Replicate: Customer
CREATE PUBLICATION customer_pub FOR TABLE customer;

-- Replicate: Supplier
CREATE PUBLICATION supplier_pub FOR TABLE supplier;