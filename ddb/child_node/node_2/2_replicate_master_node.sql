SELECT PG_SLEEP(4);

-- Replicate barang from master-node
CREATE SUBSCRIPTION barang_sub_2
CONNECTION 'host=master-node port=5432 dbname=postgres password=postgres'
PUBLICATION barang_pub;

-- Replicate kategori_barang from master-node
CREATE SUBSCRIPTION kategori_barang_sub_2
CONNECTION 'host=master-node port=5432 dbname=postgres password=postgres'
PUBLICATION kategori_barang_pub;

-- Replicate customer from master-node
CREATE SUBSCRIPTION customer_sub_2
CONNECTION 'host=master-node port=5432 dbname=postgres password=postgres'
PUBLICATION customer_pub;

-- Replicate supplier from master-node
CREATE SUBSCRIPTION supplier_sub_2
CONNECTION 'host=master-node port=5432 dbname=postgres password=postgres'
PUBLICATION supplier_pub;