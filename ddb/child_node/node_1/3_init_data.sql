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
-- (1, 'Gudang A', 'Jl. Bendungan Hilir', 'Jakarta Pusat', 'DKI Jakarta', 10210);

-- -- Insert: Inventories
-- INSERT INTO "inventories" (
--     "warehouse_id",
--     "product_id",
--     "quantity"
-- ) VALUES
-- (1, 4, 84),
-- (1, 2, 66),
-- (1, 14, 34),
-- (1, 10, 12),
-- (1, 11, 63),
-- (1, 12, 67),
-- (1, 15, 76),
-- (1, 13, 27),
-- (1, 1, 11),
-- (1, 5, 29);

INSERT INTO "gudang" ("id_gudang", "alamat", "kota", "provinsi", "kode_pos")
VALUES (1, 'Jl. Keputih Tegal Timur', 'Surabaya', 'Jawa Timur', 60111);

-- INSERT INTO "stok_barang"
-- ("id_barang", "id_gudang", "jumlah_barang")
-- VALUES
-- (1, 1, 50),
-- (2, 1, 30),
-- (3, 1, 20),
-- (4, 1, 45),
-- (5, 1, 60),
-- (6, 1, 35),
-- (7, 1, 25),
-- (8, 1, 40),
-- (9, 1, 55),
-- (10, 1, 50),
-- (11, 1, 70),
-- (12, 1, 30),
-- (13, 1, 20),
-- (14, 1, 15),
-- (15, 1, 10);

-- SELECT PG_SLEEP(3);

-- INSERT INTO "transaksi_item"
-- ("id_transaksi", "id_barang", "id_gudang", "jumlah")
-- VALUES
-- (2, 45, 1, 2),
-- (2, 29, 1, 3),
-- (2, 23, 1, 1);

-- INSERT INTO "kategori_barang"
-- ("id_kategori", "nama_kategori")
-- VALUES
-- (1, 'Elektronik'),
-- (2, 'Pakaian Pria'),
-- (3, 'Pakaian Wanita'),
-- (4, 'Peralatan Rumah Tangga'),
-- (5, 'Kesehatan & Kecantikan'),
-- (6, 'Makanan & Minuman'),
-- (7, 'Olahraga & Outdoor'),
-- (8, 'Mainan Anak & Bayi'),
-- (9, 'Otomotif'),
-- (10, 'Buku & Alat Tulis'),
-- (11, 'Handphone & Aksesoris'),
-- (12, 'Komputer & Laptop'),
-- (13, 'Furniture'),
-- (14, 'Perlengkapan Dapur'),
-- (15, 'Hobi & Koleksi)');

-- INSERT INTO "customer"
-- ("nama", "alamat", "no_telp")
-- VALUES
-- ('Ahmad Fauzi', 'Jl. Merdeka No. 45, Jakarta', '081234567890'),
-- ('Siti Nurhaliza', 'Jl. Sudirman No. 12, Bandung', '082134567891'),
-- ('Budi Santoso', 'Jl. Kartini No. 9, Surabaya', '081334567892'),
-- ('Ani Lestari', 'Jl. Diponegoro No. 34, Yogyakarta', '082234567893'),
-- ('Dian Kurniawan', 'Jl. Ahmad Yani No. 56, Semarang', '081434567894'),
-- ('Fajar Setiawan', 'Jl. Raya Bogor No. 78, Bogor', '082334567895'),
-- ('Rini Wulandari', 'Jl. Gajah Mada No. 21, Malang', '081534567896'),
-- ('Hadi Wijaya', 'Jl. Pemuda No. 14, Medan', '082434567897'),
-- ('Linda Sari', 'Jl. Panglima Polim No. 5, Palembang', '081634567898'),
-- ('Rahmat Hidayat', 'Jl. Antasari No. 88, Balikpapan', '082534567899'),
-- ('Tina Maharani', 'Jl. Sutomo No. 7, Makassar', '081734567800'),
-- ('Bayu Pratama', 'Jl. Imam Bonjol No. 40, Denpasar', '082634567801'),
-- ('Citra Andini', 'Jl. Slamet Riyadi No. 22, Solo', '081834567802'),
-- ('Eko Saputra', 'Jl. Surapati No. 15, Pontianak', '082734567803'),
-- ('Maya Kartika', 'Jl. Sisingamangaraja No. 29, Pekanbaru', '081934567804');

-- INSERT INTO "barang_core"
-- ("id_kategori", "nama_barang", "harga")
-- VALUES
-- (1, 'TV LED 32 Inch', 2500000),
-- (1, 'Kipas Angin Tornado', 500000),
-- (1, 'Rice Cooker Digital', 850000),
-- (2, 'Kemeja Formal Putih', 150000);

-- INSERT INTO "supplier"
-- ("id_supplier", "nama_supplier")
-- VALUES
-- (1, 'Samsung'),
-- (2, 'Miyako'),
-- (3, 'Uniqlo'),
-- (4, 'Ace Hardware'),
-- (5, 'Cosrx'),
-- (6, 'Indofood'),
-- (7, 'Adidas'),
-- (8, 'Miniso'),
-- (9, 'Xiaomi');