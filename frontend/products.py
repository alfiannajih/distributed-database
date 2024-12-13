from nicegui import ui
import requests

def show_table(details: bool, container):
    container.remove(0) if list(container) else None
    rows = requests.get("http://localhost:8000/api/products", params={"details": details}).json()
      
    with container:
        columns = [
            {"name": "number", "label": "No.", "field": "number", "required": True, "align": "left", "sortable": True},
            {"name": "nama_barang", "label": "Nama Barang", "field": "nama_barang", "required": True, "align": "left", "sortable": True},
            # {"name": "kategori", "label": "Kategori", "field": "kategori", "required": True, "align": "left"},
            {"name": "harga", "label": "Harga Satuan (IDR)", "field": "harga", "required": True, "align": "left", "sortable": True}
        ]

        for i, row in enumerate(rows["data"]):
            row["number"] = i+1

        if details:
            details_col = [
                {"name": "deskripsi_barang", "label": "Deskripsi Barang", "field": "deskripsi_barang", "required": True, "align": "left"},
                {"name": "berat", "label": "Berat (kg)", "field": "berat", "required": True, "align": "left", "sortable": True},
                {"name": "panjang", "label": "Panjang (cm)", "field": "panjang", "required": True, "align": "left", "sortable": True},
                {"name": "lebar", "label": "Lebar (cm)", "field": "lebar", "required": True, "align": "left", "sortable": True},
                {"name": "tinggi", "label": "Tinggi (cm)", "field": "tinggi", "required": True, "align": "left", "sortable": True}
            ]
            for col in details_col:
                columns.insert(-1, col)

        ui.table(
            columns=columns,
            rows=rows["data"]
        )

@ui.page("/products")
def products_page():
    # not_available = requests.get("http://localhost:8000/api/warhouses").json()["disconnect_servers"]
    # params = {
    #     "id_gudang": list(set([1, 2]) - set(not_available))
    # }
    # id2server = {
    #     1: "Surabaya",
    #     2: "Jakarta Pusat"
    # }
    
    with ui.column().classes('justify-center items-center w-full'):
        # Main title
        ui.label("Data Terdistribusi pada Manajemen Pergudangan").classes("text-4xl font-bold text-center")
        # Subtitle with smaller size
        ui.label("Daftar Barang").classes("text-lg text-gray-600 text-center")
        # with ui.row().classes('justify-center w-full'):
        #     if len(not_available) > 0:
        #         ui.label(f"Server {id2server[not_available[0]]} saat ini sedang mengalami gangguan, sehingga data yang ditampilkan tidak mencakup lokasi gudang {id2server[not_available[0]]}.").style(
        #             "background-color: red; color: white; font-weight: bold"
        #         )

        ui.switch('Tampilkan Detail Barang', on_change= lambda e: show_table(e.value, container))

        container =  ui.row().classes('justify-center items-center w-full')
        show_table(False, container)