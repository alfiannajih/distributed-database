from orders import orders_page
from warehouse import warehouses_page
from products import products_page
from restock import restock_page
from nicegui import ui

with ui.column().classes('justify-center items-center w-full'):
    # Main title
    ui.label("Data Terdistribusi pada Manajemen Pergudangan").classes("text-4xl font-bold text-center")

    ui.link("Daftar Barang", products_page)
    ui.link("Daftar Stok Barang", warehouses_page)
    ui.link("Daftar Restok Barang", restock_page)
    ui.link("Daftar Pesanan Customer", orders_page)
ui.run()