from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customer"

    id_customer = Column(Integer, primary_key=True)
    nama = Column(String)
    alamat = Column(String)
    no_telp = Column(String)

    order_customer = relationship("OrderCustomer", back_populates="customer")

class OrderCustomer(Base):
    __tablename__ = "order_customer"

    id_order = Column(Integer, primary_key=True)
    id_gudang = Column(Integer, ForeignKey("gudang.id_gudang"))
    tanggal_order = Column(DateTime)
    id_customer = Column(Integer, ForeignKey("customer.id_customer"))

    customer = relationship("Customer", back_populates="order_customer")
    gudang = relationship("Gudang", back_populates="order_customer")
    order_customer_item = relationship("OrderCustomerItem", back_populates="order_customer")

class OrderCustomerItem(Base):
    __tablename__ = "order_customer_item"

    id_order = Column(Integer, ForeignKey("order_customer.id_order"), primary_key=True)
    id_barang = Column(Integer, ForeignKey("barang.id_barang"), primary_key=True)
    jumlah = Column(Integer)

    order_customer = relationship("OrderCustomer", back_populates="order_customer_item")
    barang = relationship("Barang", back_populates="order_customer_item")
    
class Kategori(Base):
    __tablename__ = "kategori"

    id_kategori = Column(Integer, primary_key=True)
    nama_kategori = Column(String)

    barang = relationship("Barang", back_populates="kategori")

class Barang(Base):
    __tablename__ = "barang"

    id_barang = Column(Integer, primary_key=True)
    id_kategori = Column(Integer, ForeignKey("kategori.id_kategori"))
    nama_barang = Column(String)
    harga = Column(Float)
    deskripsi_barang = Column(String)
    berat = Column(Float)
    panjang = Column(Float)
    lebar = Column(Float)
    tinggi = Column(Float)

    kategori = relationship("Kategori", back_populates="barang")
    order_customer_item = relationship("OrderCustomerItem", back_populates="barang")
    stok_barang = relationship("StokBarang", back_populates="barang")
    restok_barang = relationship("RestokBarang", back_populates="barang")

class Gudang(Base):
    __tablename__ = "gudang"

    id_gudang = Column(Integer, primary_key=True)
    alamat = Column(String)
    kota = Column(String)
    provinsi = Column(String)
    kode_pos = Column(Integer)

    order_customer = relationship("OrderCustomer", back_populates="gudang")
    stok_barang = relationship("StokBarang", back_populates="gudang")
    restok_barang = relationship("RestokBarang", back_populates="gudang")

class StokBarang(Base):
    __tablename__ = "stok_barang"

    id_barang = Column(Integer, ForeignKey("barang.id_barang"), primary_key=True)
    id_gudang = Column(Integer, ForeignKey("gudang.id_gudang"), primary_key=True)
    stok = Column(Integer)
    tanggal_diperbarui = Column(DateTime)

    barang = relationship("Barang", back_populates="stok_barang")
    gudang = relationship("Gudang", back_populates="stok_barang")

class RestokBarang(Base):
    __tablename__ = "restok_barang"

    id_restok = Column(Integer, primary_key=True)
    id_barang = Column(Integer, ForeignKey("barang.id_barang"))
    id_gudang = Column(Integer, ForeignKey("gudang.id_gudang"))
    id_supplier = Column(Integer, ForeignKey("supplier.id_supplier"))
    jumlah = Column(Integer)
    tanggal_restok = Column(DateTime)

    barang = relationship("Barang", back_populates="restok_barang")
    gudang = relationship("Gudang", back_populates="restok_barang")
    supplier = relationship("Supplier", back_populates="restok_barang")

class Supplier(Base):
    __tablename__ = "supplier"

    id_supplier = Column(Integer, primary_key=True)
    nama_supplier = Column(String)
    
    restok_barang = relationship("RestokBarang", back_populates="supplier")

# class Product(Base):
#     __tablename__ = "products"

#     product_id = Column(Integer, primary_key=True, index=True)
#     product_name = Column(String, nullable=False)
#     description = Column(String)
#     price = Column(Float, nullable=False)
#     category = Column(String)

#     inventory = relationship("Inventory", back_populates="product")

# class Warehouse(Base):
#     __tablename__ = "warehouses"

#     warehouse_id = Column(Integer, primary_key=True, index=True)
#     warehouse_name = Column(String, nullable=False)
#     address = Column(String, nullable=False)
#     city = Column(String, nullable=False)
#     state = Column(String, nullable=False)
#     postal_code = Column(Integer, nullable=False)

#     inventory = relationship("Inventory", back_populates="warehouse")

# class Inventory(Base):
#     __tablename__ = "inventories"
    
#     warehouse_id = Column(Integer, ForeignKey("warehouses.warehouse_id"), primary_key=True)
#     product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
#     quantity = Column(Integer, nullable=False)
#     last_updated = Column(DateTime, default=func.now())
    
#     product = relationship("Product", back_populates="inventory")
#     warehouse = relationship("Warehouse", back_populates="inventory")