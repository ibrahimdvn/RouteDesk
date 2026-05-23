from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QComboBox, QLineEdit, QDialog, QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager

class AddTripDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Sefer Oluştur")
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        self.code_input = QLineEdit()
        self.company_input = QComboBox()
        self.company_input.addItems(["Kamil Koç", "Metro Turizm", "Pamukkale", "Varan"])
        
        self.route_input = QLineEdit()
        self.dep_input = QLineEdit()
        self.arr_input = QLineEdit()
        
        self.driver_input = QLineEdit()
        self.plate_input = QLineEdit()
        self.platform_input = QLineEdit()
        self.price_input = QLineEdit()
        
        self.layout_input = QComboBox()
        self.layout_input.addItems(["2+2 Standart (46 Koltuk)", "2+1 (38 Koltuk)", "3+1 Özel (50 Koltuk)"])
        
        form_layout.addRow("Sefer Kodu:", self.code_input)
        form_layout.addRow("Firma:", self.company_input)
        form_layout.addRow("Güzergah:", self.route_input)
        form_layout.addRow("Kalkış Saati:", self.dep_input)
        form_layout.addRow("Varış Saati:", self.arr_input)
        form_layout.addRow("Şoför:", self.driver_input)
        form_layout.addRow("Plaka:", self.plate_input)
        form_layout.addRow("Peron:", self.platform_input)
        form_layout.addRow("Bilet Fiyatı (₺):", self.price_input)
        form_layout.addRow("Koltuk Düzeni:", self.layout_input)
        
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Kaydet")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
    def get_data(self):
        try:
            price = int(self.price_input.text() or 0)
        except:
            price = 0
            
        layout_text = self.layout_input.currentText()
        if "2+1" in layout_text:
            layout = "2+1"
            total_seats = 38
        else:
            layout = "2+2"
            total_seats = 46
            
        return (
            self.code_input.text(),
            self.company_input.currentText(),
            self.route_input.text(),
            self.dep_input.text(),
            self.arr_input.text(),
            self.driver_input.text(),
            self.plate_input.text(),
            self.platform_input.text(),
            price,
            f"0/{total_seats}",
            "Planlandı",
            total_seats,
            layout
        )

class TripManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header_layout = QHBoxLayout()
        header = QLabel("Sefer Yönetimi")
        header.setStyleSheet("font-size: 22px; font-weight: 800;")
        header_layout.addWidget(header)
        
        btn_new = QPushButton("+ Yeni Sefer Oluştur")
        btn_new.setObjectName("primaryButton")
        btn_new.clicked.connect(self.add_new_trip)
        header_layout.addStretch()
        header_layout.addWidget(btn_new)
        
        layout.addLayout(header_layout)
        
        toolbar = QHBoxLayout()
        
        search = QLineEdit()
        search.setPlaceholderText("Güzergah, kod veya şoför ara...")
        search.setFixedWidth(250)
        toolbar.addWidget(search)
        
        filter_status = QComboBox()
        filter_status.addItems(["Tüm Durumlar", "Planlandı", "Yolcu Alımında", "Rötarlı", "Tam Dolu", "Zamanında"])
        toolbar.addWidget(filter_status)
        
        toolbar.addStretch()
        
        # Update Status Controls
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Planlandı", "Yolcu Alımında", "Rötarlı", "Tam Dolu", "Zamanında", "İptal Edildi"])
        toolbar.addWidget(self.status_combo)
        
        btn_update_status = QPushButton("Durumu Güncelle")
        btn_update_status.setObjectName("primaryButton")
        btn_update_status.clicked.connect(self.update_status)
        toolbar.addWidget(btn_update_status)
        
        btn_refresh = QPushButton("Yenile")
        btn_refresh.clicked.connect(self.load_data)
        toolbar.addWidget(btn_refresh)
        
        btn_delete = QPushButton("Seferi Sil")
        btn_delete.setStyleSheet("background-color: #ef4444; color: white; border: none;")
        btn_delete.clicked.connect(self.delete_trip)
        toolbar.addWidget(btn_delete)
        
        layout.addLayout(toolbar)
        
        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels(["Saat", "Firma", "Kod", "Güzergah", "Şoför", "Plaka", "Peron", "Fiyat", "Doluluk", "Durum"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()

    def load_data(self):
        trips = DBManager.get_all_trips()
        self.table.setRowCount(len(trips))
        for row, row_data in enumerate(trips):
            # Need: dep(4), company(2), code(1), route(3), driver(6), plate(7), platform(8), price(9), occ(dynamic), status(11)
            trip_code = row_data[1]
            cap = row_data[12] if len(row_data) > 12 and row_data[12] is not None else 46
            occ = len(DBManager.get_tickets_for_trip(trip_code))
            dynamic_occ = f"{occ}/{cap}"
            display_data = [row_data[4], row_data[2], row_data[1], row_data[3], row_data[6], row_data[7], row_data[8], f"{row_data[9]} ₺", dynamic_occ, row_data[11]]
            
            for col, item_data in enumerate(display_data):
                item = QTableWidgetItem(str(item_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
                
    def add_new_trip(self):
        dialog = AddTripDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data[0] or not data[2]:
                QMessageBox.warning(self, "Hata", "Lütfen Sefer Kodu ve Güzergah giriniz.")
                return
            
            DBManager.add_trip(*data)
            self.load_data()
            
    def delete_trip(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Seçim Yapılmadı", "Lütfen silmek istediğiniz seferi tablodan seçin.")
            return
            
        row = selected_items[0].row()
        code_item = self.table.item(row, 2) # Kolon 2 = Kod
        if code_item:
            code = code_item.text()
            reply = QMessageBox.question(self, 'Onay', 
                f"{code} kodlu seferi silmek istediğinize emin misiniz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
                
            if reply == QMessageBox.StandardButton.Yes:
                DBManager.delete_trip(code)
                self.load_data()
                QMessageBox.information(self, "Başarılı", f"{code} seferi silindi.")

    def update_status(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Seçim Yapılmadı", "Lütfen durumunu güncellemek istediğiniz seferi tablodan seçin.")
            return
            
        row = selected_items[0].row()
        code_item = self.table.item(row, 2) # Kolon 2 = Kod
        if code_item:
            code = code_item.text()
            new_status = self.status_combo.currentText()
            
            DBManager.update_trip_status(code, new_status)
            self.load_data()
            QMessageBox.information(self, "Başarılı", f"{code} seferinin durumu '{new_status}' olarak güncellendi.")
