from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class RestokCreate(BaseModel):
    id_barang: int
    id_supplier: int
    id_gudang: int
    jumlah: int
    tanggal_restok: Optional[datetime] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id_barang": 2,
                "id_gudang": 1,
                "id_supplier": 1,
                "jumlah": 34
            }
        }
    }

class CustomerCreate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    no_telp: str

class OrderCustomerItemCreate(BaseModel):
    id_barang: int
    jumlah: int

class OrderCustomerItemUpdate(BaseModel):
    jumlah: int

class OrderCustomerCreate(BaseModel):
    id_gudang: int
    tanggal_order: datetime=None
    customer: CustomerCreate
    order_items: List[OrderCustomerItemCreate]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id_gudang": 1,
                "customer": {
                    "nama": "Eko Santoso",
                    "alamat": "Jl. Embong Malang No. 21 Surabaya",
                    "no_telp": "081534567896"
                },
                "order_items": [
                    {"id_barang": 2, "jumlah": 2}
                ]
            }
        }
    }

# class ProductCreate(BaseModel):
#     product_name: str
#     description: Optional[str] = None
#     price: float
#     category: str

# class ProductUpdate(BaseModel):
#     product_name: Optional[str] = None
#     description: Optional[str] = None
#     price: Optional[float] = None
#     category: Optional[str] = None

# class InventoryCreate(BaseModel):
#     product_id: int
#     quantity: int

# class InventoryUpdate(BaseModel):
#     quantity: int