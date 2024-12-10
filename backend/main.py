from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload, load_only
from sqlalchemy import text
import uvicorn
from datetime import datetime
from typing import List

from models import StokBarang, Gudang, Barang, RestokBarang, Supplier, Customer, OrderCustomer, OrderCustomerItem
from schemas import RestokCreate, OrderCustomerCreate, OrderCustomerItemUpdate

from db import get_db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STOK BARANG
# List stok
@app.get("/api/stock", tags=["Warehouse Stock"])
def read_all_stok(
    id_gudang: List[int]=Query(None),
    id_barang: List[int]=Query(None),
    db: Session=Depends(get_db)
): # [{nama barang, lokasi gudang, stok, tanggal_diperbarui}]
    query = db.query(Barang.nama_barang, Gudang.kota, StokBarang.stok, StokBarang.tanggal_diperbarui).\
        join(Barang, Barang.id_barang == StokBarang.id_barang).\
        join(Gudang, Gudang.id_gudang == StokBarang.id_gudang)
    
    # Apply filters conditionally
    if id_barang is not None:
        query = query.filter(Barang.id_barang.in_(id_barang))
    if id_gudang is not None:
        query = query.filter(Gudang.id_gudang.in_(id_gudang))
    
    # Execute query
    stok_barang = query.all()
    
    stok_barang_clean = [{
        "nama_barang": d[0],
        "lokasi_gudang": d[1],
        "stok": d[2],
        "tanggal_diperbarui": d[3]
    } for d in stok_barang]

    results = {
        "status": "success",
        "message": "Stok barang retrieved successfully",
        "data": stok_barang_clean
    }

    return results

# RESTOK BARANG
# Create restok
@app.post("/api/restock", tags=["Warehouse Restock"])
def create_restok_record(
    data: RestokCreate,
    db: Session=Depends(get_db)
):
    if data.tanggal_restok == None:
        data.tanggal_restok = datetime.now()

    new_restok = RestokBarang(
        id_barang=data.id_barang,
        id_gudang=data.id_gudang,
        id_supplier=data.id_supplier,
        jumlah=data.jumlah,
        tanggal_restok=data.tanggal_restok
    )
    
    db.add(new_restok)
    db.flush()
    db.commit()
    db.refresh(new_restok)

    results = {
        "status": "success",
        "message": "Restok barang created successfully",
        "data": new_restok
    }

    return results

# List restok
@app.get("/api/restock", tags=["Warehouse Restock"])
def read_all_restok(
    id_gudang: List[int]=Query(None),
    id_barang: List[int]=Query(None),
    id_supplier: List[int]=Query(None),
    db: Session=Depends(get_db)
): # [{id_restok, nama barang, lokasi gudang, nama_supplier, jumlah, tanggal_restok}]
    query = db.query(
        RestokBarang.id_restok,
        Barang.nama_barang,
        Gudang.kota,
        Supplier.nama_supplier,
        RestokBarang.jumlah,
        RestokBarang.tanggal_restok
    ).\
        join(Barang, Barang.id_barang == RestokBarang.id_barang).\
        join(Gudang, Gudang.id_gudang == RestokBarang.id_gudang).\
        join(Supplier, Supplier.id_supplier == RestokBarang.id_supplier)
    
    # Apply filters conditionally
    if id_barang is not None:
        query = query.filter(Barang.id_barang.in_(id_barang))
    if id_gudang is not None:
        query = query.filter(Gudang.id_gudang.in_(id_gudang))
    if id_supplier is not None:
        query = query.filter(Supplier.id_supplier.in_(id_supplier))
    
    # Execute query
    restok_barang = query.all()
    
    restok_barang_clean = [{
        "id_restok": d[0],
        "nama_barang": d[1],
        "lokasi_gudang": d[2],
        "nama_supplier": d[3],
        "jumlah": d[4],
        "tanggal_restok": d[5]
    } for d in restok_barang]

    results = {
        "status": "success",
        "message": "Restok barang retrieved successfully",
        "data": restok_barang_clean
    }

    return results


# ORDER CUSTOMER
# Create orders
@app.post("/api/orders", tags=["Orders"])
def create_order_customer(
    data: OrderCustomerCreate,
    db: Session=Depends(get_db)
):
    try:
        # check if customer already exists by no_telp
        id_customer = db.query(Customer.id_customer).filter(Customer.no_telp == data.customer.no_telp).one()[0]

    except:
        # create new customer if not exist
        if data.customer.nama is None and data.customer.alamat is None:
            raise HTTPException(
                status_code=422,
                detail="Nomor telepon not found, please provide nama and alamat to create a new customer"
            )

        new_customer = Customer(
            nama=data.customer.nama,
            alamat=data.customer.alamat,
            no_telp=data.customer.no_telp
        )
        
        db.add(new_customer)
        db.flush()
        db.commit()
        db.refresh(new_customer)

        id_customer = new_customer.id_customer
    
    if data.tanggal_order == None:
        data.tanggal_order = datetime.now()

    order_customer = OrderCustomer(
        id_gudang=data.id_gudang,
        tanggal_order=data.tanggal_order,
        id_customer=id_customer
    )

    db.add(order_customer)
    db.flush()
    db.commit()
    db.refresh(order_customer)

    order_items = [OrderCustomerItem(
        id_order=order_customer.id_order,
        id_barang=d.id_barang,
        jumlah=d.jumlah
    ) for d in data.order_items]
    
    db.bulk_save_objects(order_items, return_defaults=True)
    db.commit()

    results = {
        "status": "success",
        "message": "Orders created successfully",
        "data": order_items
    }

    return results

@app.get("/api/orders", tags=["Orders"])
def read_all_orders(
    id_gudang: List[int]=Query(None),
    id_customer: List[int]=Query(None),
    db: Session=Depends(get_db)
): #[{id_order, nama, no_telp, lokasi_gudang, tanggal_order}]
    query = db.query(
        OrderCustomer.id_order,
        Customer.nama,
        Customer.no_telp,
        Gudang.kota,
        OrderCustomer.tanggal_order
    ).\
        join(Customer, Customer.id_customer == OrderCustomer.id_customer).\
        join(Gudang, Gudang.id_gudang == OrderCustomer.id_gudang)
    
    # Apply filters conditionally
    if id_customer is not None:
        query = query.filter(Customer.id_customer.in_(id_customer))
    if id_gudang is not None:
        query = query.filter(Gudang.id_gudang.in_(id_gudang))

    orders = query.all() 

    orders_clean = [{
        "id_order": d[0],
        "nama": d[1],
        "no_telp": d[2],
        "lokasi_gudang": d[3],
        "tanggal_order": d[4]
    } for d in orders]

    results = {
        "status": "success",
        "message": "Orders retrieved successfully",
        "data": orders_clean
    }

    return results

@app.get("/api/orders/{id_order}", tags=["Orders"])
def read_order_details(
    id_order: int,
    db: Session=Depends(get_db)
):
    order_items = db.query(
        Barang.nama_barang,
        OrderCustomerItem.jumlah
    ).join(
        Barang, Barang.id_barang == OrderCustomerItem.id_barang
    ).filter(OrderCustomerItem.id_order == id_order).all()

    order_items_clean = [{
        "nama_barang": d[0],
        "jumlah": d[1]
    } for d in order_items]

    results = {
        "status": "success",
        "message": "Order details retrieved successfully",
        "data": {
            "id_order": id_order,
            "order_items": order_items_clean
        }
    }

    return results

@app.put("/api/orders/{id_order}/products/{id_barang}", tags=["Orders"])
def update_order_item(
    id_order: int,
    id_barang:int,
    data: OrderCustomerItemUpdate,
    db: Session=Depends(get_db)
):
    order_item = db.query(OrderCustomerItem).\
        filter(OrderCustomerItem.id_order == id_order, OrderCustomerItem.id_barang == id_barang).first()
    
    order_item.jumlah = data.jumlah

    db.commit()
    db.refresh(order_item)

    results = {
        "status": "success",
        "message": "Order item updated successfully",
        "data": {
            "id_order": id_order,
            "order_item": order_item
        }
    }

    return results

@app.delete("/api/orders/{id_order}/products/{id_barang}", tags=["Orders"])
def delete_order_item(
    id_order: int,
    id_barang: int,
    db: Session=Depends(get_db)
):
    order_item = db.query(OrderCustomerItem).\
        filter(OrderCustomerItem.id_order == id_order, OrderCustomerItem.id_barang == id_barang).first()
    
    db.delete(order_item)
    db.commit()

    results = {
        "status": "success",
        "message": "Order item deleted successfully"
    }

    return results

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)