from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
import pymysql

class AddDataWidget(QWidget):
    def __init__(self, conn):
        super().__init__()

        self.conn = conn

        self.init_ui()

    def init_ui(self):
        self.idproduk_input = QLineEdit()
        self.produk_input = QLineEdit()
        self.harga_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.type_input = QLineEdit()

        self.add_button = QPushButton('Tambah Data')
        self.add_button.clicked.connect(self.add_data)

        form_layout = QFormLayout()
        form_layout.addRow('ID Produk:', self.idproduk_input)
        form_layout.addRow('Nama Produk:', self.produk_input)
        form_layout.addRow('Harga:', self.harga_input)
        form_layout.addRow('QTY:', self.quantity_input)
        form_layout.addRow('Type:', self.type_input)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Input Data Motor:'))
        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_data(self):
        id_produk = self.idproduk_input.text()
        nama_produk = self.produk_input.text()
        harga = self.harga_input.text()
        quantity = self.quantity_input.text()
        type_barang = self.type_input.text()

        with self.conn.cursor() as cursor:
            cursor.execute('INSERT INTO produk (id_produk, nama_produk, harga, quantity, id_jenis_produk) VALUES (%s, %s, %s, %s, %s)',
                           (id_produk, nama_produk, harga, quantity, type_barang))
            self.conn.commit()

        self.clear_inputs()

    def clear_inputs(self):
        self.idproduk_input.clear()
        self.produk_input.clear()
        self.harga_input.clear()
        self.quantity_input.clear()
        self.type_input.clear()

