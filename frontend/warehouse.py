from nicegui import ui
import requests

@ui.page("/warehouse")
def warehouses_page():
    not_available = requests.get("http://localhost:8000/api/warhouses").json()["disconnect_servers"]
    params = {
        "id_gudang": list(set([1, 2]) - set(not_available))
    }
    id2server = {
        1: "Surabaya",
        2: "Jakarta Pusat"
    }
    
    rows = requests.get("http://localhost:8000/api/stock", params=params).json()

    with ui.column().classes('justify-center items-center w-full'):
        # Main title
        ui.label("Data Terdistribusi pada Manajemen Pergudangan").classes("text-4xl font-bold text-center")
        # Subtitle with smaller size
        ui.label("Daftar Stok Barang pada Gudang").classes("text-lg text-gray-600 text-center")
        with ui.row().classes('justify-center w-full'):
            if len(not_available) > 0:
                ui.label(f"Server {id2server[not_available[0]]} saat ini sedang mengalami gangguan, sehingga data yang ditampilkan tidak mencakup lokasi gudang {id2server[not_available[0]]}.").style(
                    "background-color: red; color: white; font-weight: bold"
                )


    with ui.row().classes('justify-center items-center w-full'):
        columns = [
            {"name": "number", "label": "No.", "field": "number", "required": True, "align": "left"},
            {"name": "nama_barang", "label": "Nama Barang", "field": "nama_barang", "required": True, "align": "left"},
            {"name": "jumlah_barang", "label": "Stok Barang", "field": "stok", "required": True, "align": "left"},
            {"name": "lokasi_gudang", "label": "Lokasi Gudang", "field": "lokasi_gudang", "required": True, "align": "left"},
            {"name": "tanggal_diperbarui", "label": "Tanggal Diperbarui", "field": "tanggal_diperbarui", "required": True, "align": "left", "sortable": True}
        ]

        ui.table(
            columns=columns,
            rows=rows["data"]
        )