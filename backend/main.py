from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, load_only
import uvicorn
from datetime import datetime
from typing import List

from models import StokBarang, Gudang, Barang, RestokBarang, Supplier, Customer, OrderCustomer, OrderCustomerItem
from schemas import RestokCreate, OrderCustomerCreate, OrderCustomerItemUpdate, OrderCustomerItemCreate

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

@app.get("/api/products", tags=["Products"])
def read_all_products(
    details: bool=False,
    db: Session=Depends(get_db)
):
    if details:
        barang = db.query(Barang).order_by(Barang.nama_barang).all()
    else:
        barang = db.query(Barang).options(
            load_only(Barang.id_barang, Barang.id_kategori, Barang.nama_barang, Barang.harga)
        ).order_by(Barang.nama_barang).all()

    results = {
        "status": "success",
        "message": "Products retrieved successfully",
        "data": barang
    }

    return results    

@app.get("/api/customers/{phone_number}", tags=["Customers"])
def read_customer_by_phone(
    phone_number: str,
    db: Session=Depends(get_db)
):
    try:
        customer = db.query(Customer).filter(Customer.no_telp == phone_number).one()

    except:
        raise HTTPException(404, "Customer not found!")
    
    results = {
        "status": "success",
        "message": "Customer retrieved successfully",
        "data": customer
    }

    return results

@app.get("/api/warhouses", tags=["Warehouses"])
def check_server_status(
    db: Session=Depends(get_db)
):
    disconnect_servers = []
    
    for i in range(1, 3):
        # with get_db() as db:
        try:
            db.query(Gudang.id_gudang).filter(Gudang.id_gudang == i).one()

        except:
            db.rollback()
            disconnect_servers.append(i)
    
    return {"disconnect_servers": disconnect_servers}

# STOK BARANG
# List stok
@app.get("/api/stock", tags=["Warehouse Stock"])
def read_all_stok(
    id_gudang: List[int]=Query(None),
    id_barang: List[int]=Query(None),
    db: Session=Depends(get_db)
): # [{nama barang, lokasi gudang, stok, tanggal_diperbarui}]
    query = db.query(
        StokBarang.id_barang,
        Barang.nama_barang,
        StokBarang.id_gudang,
        Gudang.kota,
        StokBarang.stok,
        StokBarang.tanggal_diperbarui
    ).\
        join(Barang, Barang.id_barang == StokBarang.id_barang).\
        join(Gudang, Gudang.id_gudang == StokBarang.id_gudang).order_by(StokBarang.tanggal_diperbarui.desc())
    
    # Apply filters conditionally
    if id_barang is not None:
        query = query.filter(Barang.id_barang.in_(id_barang))
    if id_gudang is not None:
        query = query.filter(Gudang.id_gudang.in_(id_gudang))
    
    # Execute query
    stok_barang = query.all()
    
    stok_barang_clean = [{
        "number": i + 1,
        "id_barang": d[0],
        "nama_barang": d[1],
        "id_gudang": d[2],
        "lokasi_gudang": d[3],
        "stok": d[4],
        "tanggal_diperbarui": d[5].strftime("%Y-%m-%d, %H.%M.%S")
    } for i, d in enumerate(stok_barang)]

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
        RestokBarang.id_barang,
        Barang.nama_barang,
        RestokBarang.id_gudang,
        Gudang.kota,
        RestokBarang.id_supplier,
        Supplier.nama_supplier,
        RestokBarang.jumlah,
        RestokBarang.tanggal_restok
    ).\
        join(Barang, Barang.id_barang == RestokBarang.id_barang).\
        join(Gudang, Gudang.id_gudang == RestokBarang.id_gudang).\
        join(Supplier, Supplier.id_supplier == RestokBarang.id_supplier).\
        order_by(RestokBarang.tanggal_restok.desc())
    
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
        "id_barang": d[1],
        "nama_barang": d[2],
        "id_gudang": d[3],
        "lokasi_gudang": d[4],
        "id_supplier": d[5],
        "nama_supplier": d[6],
        "jumlah": d[7],
        "tanggal_restok": d[8].strftime("%Y-%m-%d, %H.%M.%S")
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
    # disconnect_servers = check_server_status(db)
    
    query = db.query(
        OrderCustomer.id_order,
        OrderCustomer.id_customer,
        Customer.nama,
        Customer.no_telp,
        OrderCustomer.id_gudang,
        Gudang.kota,
        OrderCustomer.tanggal_order
    ).\
        join(Customer, Customer.id_customer == OrderCustomer.id_customer).\
        join(Gudang, Gudang.id_gudang == OrderCustomer.id_gudang).order_by(OrderCustomer.tanggal_order.desc())
    
    # Apply filters conditionally
    if id_customer is not None:
        query = query.filter(OrderCustomer.id_customer.in_(id_customer))
    if id_gudang is not None:
        query = query.filter(OrderCustomer.id_gudang.in_(id_gudang))

    # if len(disconnect_servers) > 0:
    #     query = query.filter(OrderCustomer.id_gudang.not_in(disconnect_servers))
    #     warning_message = {
    #         "details": "Some server is disconnected",
    #         "disconnected_servers": disconnect_servers
    #     }
    # else:
    #     warning_message = None

    orders = query.all() 

    orders_clean = [{
        "id_order": d[0],
        "id_customer": d[1],
        "nama": d[2],
        "no_telp": d[3],
        "id_gudang": d[4],
        "lokasi_gudang": d[5],
        "tanggal_order": d[6].strftime("%Y-%m-%d, %H.%M.%S")
    } for d in orders]

    results = {
        "status": "success",
        "message": "Orders retrieved successfully",
        "data": orders_clean
        # "warning": warning_message
    }

    return results

@app.get("/api/orders/{id_order}", tags=["Orders"])
def read_order_details(
    id_order: int,
    db: Session=Depends(get_db)
):
    order_items = db.query(
        OrderCustomerItem.id_barang,
        Barang.nama_barang,
        OrderCustomerItem.jumlah
    ).join(
        Barang, Barang.id_barang == OrderCustomerItem.id_barang
    ).filter(OrderCustomerItem.id_order == id_order).all()

    id_gudang = db.query(OrderCustomer.id_gudang).filter(OrderCustomer.id_order == id_order).one()[0]

    order_items_clean = [{
        "id_barang": d[0],
        "nama_barang": d[1],
        "jumlah": d[2]
    } for d in order_items]

    results = {
        "status": "success",
        "message": "Order details retrieved successfully",
        "data": {
            "id_order": id_order,
            "id_gudang": id_gudang,
            "order_items": order_items_clean
        }
    }

    return results

@app.delete("/api/orders/{id_order}", tags=["Orders"])
def delete_order(
    id_order: int,
    db: Session=Depends(get_db)
):  
    db.query(OrderCustomerItem).filter(OrderCustomerItem.id_order == id_order).delete()
    orders = db.query(OrderCustomer).filter(OrderCustomer.id_order == id_order).first()

    db.delete(orders)
    db.commit()

    results = {
        "status": "success",
        "message": "Order deleted successfully"
    }

    return results

# @app.post("/api/orders/{id_order}", tags=["Orders"])
# def create_order_item(
#     id_order: int,
#     data: OrderCustomerItemCreate,
#     db: Session=Depends(get_db)
# ):
#     new_order_item = OrderCustomerItem(
#         id_order=id_order,
#         id_barang=data.id_barang,
#         jumlah=data.jumlah
#     )

#     db.add(new_order_item)
#     db.flush()
#     db.commit()
#     db.refresh(new_order_item)

#     results = {
#         "status": "success",
#         "message": "Orders retrieved successfully",
#         "data": new_order_item
#     }

#     return results

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