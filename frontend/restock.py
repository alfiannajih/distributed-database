from nicegui import ui
import requests

@ui.page("/restock")
def restock_page():
    not_available = requests.get("http://localhost:8000/api/warhouses").json()["disconnect_servers"]
    params = {
        "id_gudang": list(set([1, 2]) - set(not_available))
    }
    id2server = {
        1: "Surabaya",
        2: "Jakarta Pusat"
    }
    
    rows = requests.get("http://localhost:8000/api/restock", params=params).json()

    with ui.column().classes('justify-center items-center w-full'):
        # Main title
        ui.label("Data Terdistribusi pada Manajemen Pergudangan").classes("text-4xl font-bold text-center")
        # Subtitle with smaller size
        ui.label("Daftar Restok Barang pada Gudang").classes("text-lg text-gray-600 text-center")
        with ui.row().classes('justify-center w-full'):
            if len(not_available) > 0:
                ui.label(f"Server {id2server[not_available[0]]} saat ini sedang mengalami gangguan, sehingga data yang ditampilkan tidak mencakup lokasi gudang {id2server[not_available[0]]}.").style(
                    "background-color: red; color: white; font-weight: bold"
                )


    with ui.row().classes('justify-center items-center w-full'):
        columns = [
            {"name": "id_restok", "label": "ID Restok", "field": "id_restok", "required": True, "align": "left"},
            {"name": "nama_barang", "label": "Nama Barang", "field": "nama_barang", "required": True, "align": "left"},
            {"name": "lokasi_gudang", "label": "Lokasi Gudang", "field": "lokasi_gudang", "required": True, "align": "left"},
            {"name": "nama_supplier", "label": "Supplier", "field": "nama_supplier", "required": True, "align": "left"},
            {"name": "jumlah_barang", "label": "Jumlah Barang", "field": "jumlah", "required": True, "align": "left"},
            {"name": "tanggal_restok", "label": "Tanggal Restok", "field": "tanggal_restok", "required": True, "align": "left", "sortable": True}
        ]

        ui.table(
            columns=columns,
            rows=rows["data"]
        )