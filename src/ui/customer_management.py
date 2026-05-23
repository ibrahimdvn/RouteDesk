from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QLineEdit, QDialog, QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager

class AddCustomerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Müşteri Ekle")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("05XX XXX XX XX")
        self.name_input = QLineEdit()
        self.tc_input = QLineEdit()
        
        form_layout.addRow("Telefon Numarası:", self.phone_input)
        form_layout.addRow("Ad Soyad:", self.name_input)
        form_layout.addRow("T.C. Kimlik No:", self.tc_input)
        
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Kaydet")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
    def get_data(self):
        return (
            self.phone_input.text().strip(),
            self.name_input.text().strip(),
            self.tc_input.text().strip()
        )

class CustomerManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header_layout = QHBoxLayout()
        header = QLabel("Müşteri Yönetimi")
        header.setStyleSheet("font-size: 22px; font-weight: 800;")
        header_layout.addWidget(header)
        
        btn_new = QPushButton("+ Yeni Müşteri Ekle")
        btn_new.setObjectName("primaryButton")
        btn_new.clicked.connect(self.add_customer)
        header_layout.addStretch()
        header_layout.addWidget(btn_new)
        
        layout.addLayout(header_layout)
        
        toolbar = QHBoxLayout()
        search = QLineEdit()
        search.setPlaceholderText("Telefon No veya Ad ile ara...")
        search.setFixedWidth(300)
        toolbar.addWidget(search)
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Telefon", "Ad Soyad", "T.C. Kimlik No"])
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
        customers = DBManager.get_all_customers()
        self.table.setRowCount(len(customers))
        for row, row_data in enumerate(customers):
            for col, item_data in enumerate(row_data):
                item = QTableWidgetItem(str(item_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
                
    def add_customer(self):
        dialog = AddCustomerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data[0] or not data[1]:
                QMessageBox.warning(self, "Eksik Bilgi", "Lütfen Telefon ve Ad Soyad alanlarını doldurun.")
                return
            
            try:
                DBManager.add_customer(*data)
                self.load_data()
            except Exception as e:
                QMessageBox.warning(self, "Hata", "Müşteri kaydedilemedi. Telefon numarası sistemde kayıtlı olabilir.")
