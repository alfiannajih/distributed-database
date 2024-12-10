-- SELECT PG_SLEEP(6);

-- -- Insert: Warehouses
-- INSERT INTO "warehouses" (
--     "warehouse_id",
--     "warehouse_name",
--     "address",
--     "city",
--     "state",
--     "postal_code"
-- ) VALUES 
-- (2, 'Gudang B', 'Jl. Keputih Tegal Timur', 'Surabaya', 'Jawa Timur', 60111);

-- -- Insert: Inventories
-- INSERT INTO "inventories" (
--     "warehouse_id",
--     "product_id",
--     "quantity"
-- ) VALUES
-- (2, 1, 46),
-- (2, 6, 72),
-- (2, 7, 38),
-- (2, 14, 62),
-- (2, 13, 60),
-- (2, 15, 49),
-- (2, 4, 36),
-- (2, 3, 55),
-- (2, 5, 37);

INSERT INTO "gudang" ("id_gudang", "alamat", "kota", "provinsi", "kode_pos")
VALUES (2, 'Jl. Bendungan Hilir', 'Jakarta Pusat', 'DKI Jakarta', 10210);

-- INSERT INTO "stok_barang"
-- ("id_barang", "id_gudang", "jumlah_barang")
-- VALUES
-- (1, 2, 45),
-- (2, 2, 25),
-- (3, 2, 35),
-- (4, 2, 50),
-- (5, 2, 55),
-- (6, 2, 40),
-- (7, 2, 30),
-- (8, 2, 20),
-- (9, 2, 60),
-- (10, 2, 45),
-- (11, 2, 65),
-- (12, 2, 25),
-- (13, 2, 30),
-- (14, 2, 20),
-- (15, 2, 15);

-- SELECT PG_SLEEP(3);

-- INSERT INTO "transaksi_item"
-- ("id_transaksi", "id_barang", "id_gudang", "jumlah")
-- VALUES
-- (1, 1, 2, 1),
-- (1, 3, 2, 1),
-- (1, 25, 2, 2);