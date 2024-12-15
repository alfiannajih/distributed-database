SELECT PG_SLEEP(4);

-- Replicate barang from master-node
CREATE SUBSCRIPTION barang_sub_1
CONNECTION 'host=10.42.0.1 port=5432 dbname=postgres password=postgres'
PUBLICATION barang_pub;

-- Replicate kategori_barang from 10.42.0.1
CREATE SUBSCRIPTION kategori_barang_sub_1
CONNECTION 'host=10.42.0.1 port=5432 dbname=postgres password=postgres'
PUBLICATION kategori_barang_pub;

-- Replicate customer from 10.42.0.1
CREATE SUBSCRIPTION customer_sub_1
CONNECTION 'host=10.42.0.1 port=5432 dbname=postgres password=postgres'
PUBLICATION customer_pub;

-- Replicate supplier from 10.42.0.1
CREATE SUBSCRIPTION supplier_sub_1
CONNECTION 'host=10.42.0.1 port=5432 dbname=postgres password=postgres'
PUBLICATION supplier_pub;