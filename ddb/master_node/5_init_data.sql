SELECT PG_SLEEP(2);

INSERT INTO "kategori_barang"
("id_kategori", "nama_kategori")
VALUES
(1, 'Elektronik'),
(2, 'Pakaian Pria'),
(3, 'Pakaian Wanita'),
(4, 'Peralatan Rumah Tangga'),
(5, 'Kesehatan & Kecantikan'),
(6, 'Makanan & Minuman'),
(7, 'Olahraga & Outdoor'),
(8, 'Mainan Anak & Bayi'),
(9, 'Otomotif'),
(10, 'Buku & Alat Tulis'),
(11, 'Handphone & Aksesoris'),
(12, 'Komputer & Laptop'),
(13, 'Furniture'),
(14, 'Perlengkapan Dapur'),
(15, 'Hobi & Koleksi)');

INSERT INTO "barang"
("id_kategori", "nama_barang", "harga", "deskripsi_barang", "berat", "panjang", "lebar", "tinggi")
VALUES
(1, 'TV LED 32 Inch', 2500000, 'TV LED dengan resolusi HD dan desain minimalis.', 5, 73, 20, 48),
(1, 'Kipas Angin Tornado', 500000, 'Kipas angin berkecepatan tinggi untuk ruangan besar.', 3, 40, 40, 60),
(1, 'Rice Cooker Digital', 850000, 'Rice cooker dengan pengaturan digital dan fitur penghangat.', 2, 25, 25, 30),
(2, 'Kemeja Formal Putih', 150000, 'Kemeja formal untuk acara resmi, bahan katun.', 0.3, 30, 25, 3),
(2, 'Kaos Polos Hitam', 80000, 'Kaos polos bahan nyaman, cocok untuk santai.', 0.2, 30, 25, 3),
(2, 'Celana Chino', 200000, 'Celana chino slim fit, warna krem.', 0.5, 35, 25, 5),
(3, 'Blouse Satin', 180000, 'Blouse elegan bahan satin, cocok untuk pesta.', 0.3, 28, 20, 2),
(3, 'Rok Plisket', 170000, 'Rok plisket panjang dengan warna pastel.', 0.4, 30, 20, 5),
(3, 'Dress Maxi', 300000, 'Dress maxi dengan motif floral.', 0.5, 35, 25, 10),
(4, 'Set Alat Pel', 100000, 'Alat pel lengkap dengan ember dan kain microfiber.', 1.5, 40, 20, 20),
(4, 'Gantungan Baju Stainless', 80000, 'Gantungan baju anti karat dengan desain minimalis.', 1, 50, 10, 30),
(4, 'Vacuum Cleaner Mini', 400000, 'Vacuum cleaner mini untuk membersihkan sofa dan karpet.', 1.2, 30, 15, 10),
(5, 'Skincare Paket Lengkap', 500000, 'Paket skincare untuk perawatan wajah sehari-hari.', 0.8, 20, 15, 10),
(5, 'Hair Dryer', 250000, 'Hair dryer dengan pengaturan suhu panas dan dingin.', 0.6, 25, 20, 10),
(5, 'Vitamin C 1000mg', 120000, 'Suplemen vitamin C untuk daya tahan tubuh.', 0.3, 10, 5, 5),
(6, 'Cokelat Batang', 25000, 'Cokelat batang premium dengan rasa susu.', 0.1, 15, 5, 1),
(6, 'Kopi Arabika 250g', 75000, 'Bubuk kopi arabika asli dari pegunungan.', 0.25, 20, 10, 5),
(6, 'Keripik Singkong Pedas', 20000, 'Keripik singkong dengan rasa pedas gurih.', 0.2, 20, 15, 5),
(7, 'Matras Yoga', 150000, 'Matras yoga anti slip dengan ketebalan 6mm.', 1.5, 60, 20, 10),
(7, 'Sepatu Lari Pria', 350000, 'Sepatu lari ringan untuk olahraga sehari-hari.', 1, 30, 20, 15),
(7, 'Botol Minum 1L', 80000, 'Botol minum tahan panas dan dingin.', 0.5, 10, 10, 25),
(8, 'Boneka Teddy Bear', 120000, 'Boneka teddy bear berbulu halus.', 0.8, 30, 25, 30),
(8, 'Puzzle Kayu', 50000, 'Puzzle kayu edukatif untuk anak usia 3 tahun ke atas.', 0.3, 25, 20, 5),
(8, 'Mobil Remote Control', 250000, 'Mobil remote control dengan kecepatan tinggi.', 1, 40, 20, 15),
(9, 'Helm Full Face', 600000, 'Helm full face standar SNI dengan desain sporty.', 2, 35, 30, 25),
(9, 'Cover Motor', 100000, 'Cover motor anti air untuk segala cuaca.', 1.5, 30, 20, 5),
(9, 'Kunci Inggris', 75000, 'Kunci inggris ukuran universal untuk perbaikan.', 0.8, 20, 5, 2),
(10, 'Notebook Hardcover', 30000, 'Notebook dengan cover keras dan 100 halaman.', 0.5, 20, 15, 2),
(10, 'Pensil Warna 24', 45000, 'Set pensil warna 24 pcs untuk menggambar.', 0.4, 20, 10, 3),
(10, 'Pulpen Gel Hitam', 10000, 'Pulpen gel dengan tinta hitam pekat.', 0.1, 15, 2, 1),
(11, 'Charger Fast Charging', 120000, 'Charger fast charging kompatibel dengan berbagai perangkat.', 0.3, 15, 10, 5),
(11, 'Casing HP Transparan', 50000, 'Casing HP anti gores, desain transparan.', 0.2, 10, 8, 2),
(11, 'Powerbank 10000mAh', 300000, 'Powerbank kapasitas besar dengan dual output.', 0.5, 15, 8, 2),
(12, 'Keyboard Mechanical', 800000, 'Keyboard mechanical RGB untuk gaming.', 1, 40, 15, 5),
(12, 'Mouse Wireless', 200000, 'Mouse wireless dengan desain ergonomis.', 0.2, 10, 5, 2),
(12, 'Webcam HD', 350000, 'Webcam dengan resolusi 1080p untuk streaming.', 0.3, 10, 10, 5),
(13, 'Meja Lipat', 400000, 'Meja lipat praktis untuk belajar atau bekerja.', 5, 60, 40, 5),
(13, 'Kursi Kayu Minimalis', 750000, 'Kursi kayu dengan desain minimalis dan kokoh.', 8, 45, 45, 90),
(13, 'Rak Buku 3 Tingkat', 500000, 'Rak buku dengan 3 tingkat, bahan kayu MDF.', 10, 80, 30, 120),
(14, 'Pisau Dapur Set', 200000, 'Set pisau dapur lengkap dengan talenan.', 1.5, 30, 20, 5),
(14, 'Panci Stainless Steel', 300000, 'Panci stainless steel ukuran 24 cm.', 2.5, 40, 20, 15),
(14, 'Blender Multifungsi', 500000, 'Blender multifungsi dengan 3 mode kecepatan.', 2, 30, 20, 20),
(15, 'Gitar Akustik', 1200000, 'Gitar akustik 6 senar untuk pemula dan profesional.', 3, 100, 35, 10),
(15, 'Action Figure Superhero', 350000, 'Action figure superhero dengan detail tinggi.', 0.8, 20, 15, 5),
(15, 'Cat Acrylic 12 Warna', 150000, 'Set cat acrylic 12 warna untuk melukis.', 0.5, 20, 10, 5);

INSERT INTO "supplier"
("id_supplier", "nama_supplier")
VALUES
(1, 'Samsung'),
(2, 'Miyako'),
(3, 'Uniqlo'),
(4, 'Ace Hardware'),
(5, 'Cosrx'),
(6, 'Indofood'),
(7, 'Adidas'),
(8, 'Miniso'),
(9, 'Xiaomi');