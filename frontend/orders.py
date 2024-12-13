from nicegui import ui
import requests

barang = requests.get("http://localhost:8000/api/products?details=false").json()["data"]
list_barang = [d["nama_barang"] for d in barang]

def add_new_item():
    with ui.row():
        nama_barang = ui.select(list_barang, label="Nama Barang").style("width: 150px")
        jumlah = ui.select(list(range(1, 10)), label="Jumlah").style("width: 150px")        

        # ui.button("add new",on_click=addnewdata)
# http://localhost:8000/api/customers/082734567803
def new_order():
    with ui.dialog() as new_order_dialog, ui.card().style('width: 600px; max-height: 500px'):
        ui.label("Order Baru")
        # check if customer exist
        # customer = requests.get(f"http://localhost:8000/api/customers/{new_telepon}")

        new_nama = ui.input(label="Nama")
        new_telepon = ui.input(label="No.Telepon")
        new_alamat = ui.input(label="Alamat")
        lokasi_gudang = ui.select(["Surabaya", "Jakarta Pusat"], label="Lokasi Gudang").style("width: 150px")
        
        ui.button("tambah barang", on_click=add_new_item)
        
        ui.button("Submit")
    
    new_order_dialog.open()

def order_details(
    data: dict
):
    with ui.dialog() as order_details_dialog, ui.card().style('width: 400px; max-height: 500px'):
        order_items = requests.get(
            f"http://localhost:8000/api/orders/{data['id_order']}"
        ).json()["data"]
        with ui.row().classes('justify-center w-full'):
            with ui.column():
                with ui.row():
                    ui.label(f"Detail Order").classes("text-lg text-gray-600")
                    # ui.button(icon="delete")
                ui.label(f"ID Order: {data['id_order']}").style("font-size: 12px")
                ui.label(f"Nama Customer: {data['nama']}").style("font-size: 12px")
                ui.label(f"Tanggal Order: {data['tanggal_order']}").style("font-size: 12px")
            order_details_table = ui.table(
                columns=[
                    {"name": "id_barang", "label": "ID Barang", "field": "id_barang", "required": True, "align": "left"},
                    {"name": "nama_barang", "label": "Nama Barang", "field": "nama_barang", "required": True, "align": "left"},
                    {"name": "jumlah", "label": "Jumlah", "field": "jumlah", "required": True, "align": "left"},
                    # {"name": "action_button", "label": "Action", "field": "action_button", "required": True, "align": "left"},
                ],
                rows=order_items["order_items"]
            )
            # order_details_table.add_slot(f'body-cell-action_button', """
            #     <q-td :props="props">
            #         <q-btn @click="$parent.$emit('delete', props)" icon="delete" flat dense color='green'/>
            #     </q-td>
            # """)
            #         # <q-btn @click="$parent.$emit('edit', props)" icon="edit" flat dense color='green'/>
            # # order_details_table.on('edit', lambda msg: order_details(msg.args["row"]))
            # order_details_table.on('delete', lambda msg: delete_item(id_order=data["id_order"], id_barang=msg.args["row"]["id_barang"]))

    order_details_dialog.open()

def delete_item(
    id_order: int,
    id_barang: int
):
    requests.delete(f"http://localhost:8000/api/orders/{id_order}/products/{id_barang}")

@ui.page("/orders")
def orders_page():
    not_available = requests.get("http://localhost:8000/api/warhouses").json()["disconnect_servers"]
    params = {
        "id_gudang": list(set([1, 2]) - set(not_available))
    }
    id2server = {
        1: "Surabaya",
        2: "Jakarta Pusat"
    }
    orders_data = requests.get("http://localhost:8000/api/orders", params=params).json()["data"]
    
    with ui.column().classes('justify-center items-center w-full'):
        # Main title
        ui.label("Data Terdistribusi pada Manajemen Pergudangan").classes("text-4xl font-bold text-center")
        # Subtitle with smaller size
        ui.label("Daftar Pesanan Customer").classes("text-lg text-gray-600 text-center")
        
        with ui.row().classes('justify-center w-full'):
            if len(not_available) > 0:
                ui.label(f"Server {id2server[not_available[0]]} saat ini sedang mengalami gangguan, sehingga data yang ditampilkan tidak mencakup lokasi gudang {id2server[not_available[0]]}.").style(
                    "background-color: red; color: white; font-weight: bold"
                )
        
        with ui.row().classes('justify-center w-full'):
            with ui.column():
                # ui.button("Order Baru", on_click=new_order)

                columns = [
                    {"name": "detail", "label": "Detail", "field": "detail", "required": True, "align": "left"},
                    {"name": "id_order", "label": "ID Order", "field": "id_order", "required": True, "align": "left", "sortable": True},
                    {"name": "nama_customer", "label": "Nama Customer", "field": "nama", "required": True, "align": "left", "sortable": True},
                    {"name": "no_telp", "label": "Nomor Telepon", "field": "no_telp", "required": True, "align": "left", "sortable": True},
                    {"name": "lokasi_gudang", "label": "Lokasi Gudang", "field": "lokasi_gudang", "required": True, "align": "left", "sortable": True},
                    {"name": "tanggal_order", "label": "Tanggal Order", "field": "tanggal_order", "required": True, "align": "left", "sortable": True}
                ]
                orders_table = ui.table(
                    columns=columns,
                    rows=orders_data
                ).classes('mt-8')

            orders_table.add_slot(f'body-cell-detail', """
                <q-td :props="props">
                    <q-btn @click="$parent.$emit('action', props)" icon="info" flat dense color='green'/>
                </q-td>
            """)
            orders_table.on('action', lambda msg: order_details(msg.args["row"]))