import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QFormLayout
import pymysql

class MotorDealerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Penambahan Produk dalam Dealer Motor')
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        # Komponen UI
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)  # Menambah satu kolom untuk ID Produk
        self.table_widget.setHorizontalHeaderLabels(["ID Produk", "Nama Produk", "Harga", "Quantity", "Type Barang"])

        self.refresh_button = QPushButton('Refresh Data')
        self.refresh_button.clicked.connect(self.refresh_data)

        self.idproduk_input = QLineEdit()
        self.produk_input = QLineEdit()
        self.harga_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.type_input = QLineEdit()
        
        self.add_button = QPushButton('Tambah Data')
        self.add_button.clicked.connect(self.add_data)

        # Layout
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow('ID Produk:', self.idproduk_input)  # Baris ini menambahkan input ID Produk
        form_layout.addRow('Nama Produk:', self.produk_input)
        form_layout.addRow('Harga:', self.harga_input)
        form_layout.addRow('QTY:', self.quantity_input)
        form_layout.addRow('Type:', self.type_input)

        layout.addWidget(QLabel('Input Data Motor:'))
        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.table_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Koneksi ke database
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='dealer_motor'
        )

        # Refresh data saat aplikasi dimulai
        self.refresh_data()

    def refresh_data(self):
        # Mengambil data dari database
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM produk')
            result = cursor.fetchall()

            # Menampilkan data di tabel
            self.table_widget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_data(self):
        # Mendapatkan nilai dari input
        id_produk = self.idproduk_input.text()
        nama_produk = self.produk_input.text()
        harga = self.harga_input.text()
        quantity = self.quantity_input.text()
        type_barang = self.type_input.text()

        # Menambahkan data baru ke dalam database
        with self.conn.cursor() as cursor:
            cursor.execute('INSERT INTO produk (id_produk, nama_produk, harga, quantity, id_jenis_produk) VALUES (%s, %s, %s, %s, %s)',
                           (id_produk, nama_produk, harga, quantity, type_barang))
            self.conn.commit()

        # Membersihkan input setelah menambahkan data
        self.idproduk_input.clear()
        self.produk_input.clear()
        self.harga_input.clear()
        self.quantity_input.clear()
        self.type_input.clear()

        # Refresh data setelah menambahkan
        self.refresh_data()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MotorDealerApp()
    mainWin.show()
    sys.exit(app.exec_())