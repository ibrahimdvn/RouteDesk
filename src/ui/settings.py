import os
import json
import shutil
import csv
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QFormLayout, QFrame, QScrollArea, QCheckBox, QComboBox, QGroupBox, 
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import pyqtSignal

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "routedesk.db")

class Settings(QWidget):
    settings_saved = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Sistem Ayarları")
        header.setStyleSheet("font-size: 22px; font-weight: 800;")
        main_layout.addWidget(header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        
        # General Settings
        group_general = QGroupBox("GENEL AYARLAR")
        group_general.setStyleSheet("font-weight: bold; color: #9ca3af; margin-top: 10px;")
        gen_layout = QFormLayout(group_general)
        gen_layout.setContentsMargins(15, 20, 15, 15)
        
        self.comp_name = QLineEdit("RouteDesk A.Ş.")
        self.comp_name.setStyleSheet("font-weight: normal; color: white;")
        self.term_name = QLineEdit("Merkez Otogar Peron 1")
        self.term_name.setStyleSheet("font-weight: normal; color: white;")
        self.printer = QComboBox()
        self.printer.addItems(["Termal Yazıcı (COM3)", "Lazer Yazıcı (Ağ)", "PDF Olarak Kaydet"])
        self.printer.setStyleSheet("font-weight: normal; color: white;")
        
        gen_layout.addRow("Firma Adı:", self.comp_name)
        gen_layout.addRow("Terminal Adı:", self.term_name)
        gen_layout.addRow("Varsayılan Yazıcı:", self.printer)
        layout.addWidget(group_general)
        
        # Ticketing Settings
        group_ticket = QGroupBox("BİLETLENDİRME")
        group_ticket.setStyleSheet("font-weight: bold; color: #9ca3af; margin-top: 10px;")
        t_layout = QFormLayout(group_ticket)
        t_layout.setContentsMargins(15, 20, 15, 15)
        
        self.template = QComboBox()
        self.template.addItems(["Standart (Termal)", "Geniş (A4)", "E-Bilet (Sms/Mail)"])
        self.template.setStyleSheet("font-weight: normal; color: white;")
        
        self.auto_print = QCheckBox("Satış sonrası otomatik yazdır")
        self.auto_print.setChecked(True)
        self.auto_print.setStyleSheet("font-weight: normal; color: white;")
        
        t_layout.addRow("Bilet Şablonu:", self.template)
        t_layout.addRow("", self.auto_print)
        layout.addWidget(group_ticket)
        
        # Database Settings
        group_db = QGroupBox("VERİTABANI & BAKIM")
        group_db.setStyleSheet("font-weight: bold; color: #9ca3af; margin-top: 10px;")
        db_layout = QHBoxLayout(group_db)
        db_layout.setContentsMargins(15, 20, 15, 15)
        
        btn_backup = QPushButton("Yedek Al")
        btn_backup.clicked.connect(self.backup_db)
        
        btn_restore = QPushButton("Yedekten Dön")
        btn_restore.clicked.connect(self.restore_db)
        
        btn_export = QPushButton("Verileri Dışa Aktar (CSV)")
        btn_export.clicked.connect(self.export_csv)
        
        db_layout.addWidget(btn_backup)
        db_layout.addWidget(btn_restore)
        db_layout.addWidget(btn_export)
        db_layout.addStretch()
        layout.addWidget(group_db)
        
        # System Settings
        group_sys = QGroupBox("SİSTEM")
        group_sys.setStyleSheet("font-weight: bold; color: #9ca3af; margin-top: 10px;")
        sys_layout = QFormLayout(group_sys)
        sys_layout.setContentsMargins(15, 20, 15, 15)
        
        self.window_mode = QComboBox()
        self.window_mode.addItems(["Pencereli", "Tam Ekran (Fullscreen)", "Genişletilmiş (Maximized)"])
        self.window_mode.setStyleSheet("font-weight: normal; color: white;")
        
        self.timeout = QComboBox()
        self.timeout.addItems(["15 Dakika", "30 Dakika", "1 Saat", "Hiçbir Zaman"])
        self.timeout.setStyleSheet("font-weight: normal; color: white;")
        
        sys_layout.addRow("Ekran Modu:", self.window_mode)
        sys_layout.addRow("Oturum Zaman Aşımı:", self.timeout)
        layout.addWidget(group_sys)
        
        layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        # Save Button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        btn_save = QPushButton("Ayarları Kaydet")
        btn_save.setObjectName("primaryButton")
        btn_save.clicked.connect(self.save_settings)
        bottom_layout.addWidget(btn_save)
        
        main_layout.addLayout(bottom_layout)

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.comp_name.setText(config.get("comp_name", "RouteDesk A.Ş."))
                    self.term_name.setText(config.get("term_name", "Merkez Otogar Peron 1"))
                    self.printer.setCurrentText(config.get("printer", "Termal Yazıcı (COM3)"))
                    self.template.setCurrentText(config.get("template", "Standart (Termal)"))
                    self.auto_print.setChecked(config.get("auto_print", True))
                    self.window_mode.setCurrentText(config.get("window_mode", "Pencereli"))
                    self.timeout.setCurrentText(config.get("timeout", "15 Dakika"))
            except Exception as e:
                pass

    def save_settings(self):
        config = {
            "comp_name": self.comp_name.text(),
            "term_name": self.term_name.text(),
            "printer": self.printer.currentText(),
            "template": self.template.currentText(),
            "auto_print": self.auto_print.isChecked(),
            "window_mode": self.window_mode.currentText(),
            "timeout": self.timeout.currentText()
        }
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            self.settings_saved.emit()
            QMessageBox.information(self, "Başarılı", "Ayarlar başarıyla kaydedildi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ayarlar kaydedilirken hata oluştu:\n{str(e)}")

    def backup_db(self):
        if not os.path.exists(DB_PATH):
            QMessageBox.warning(self, "Uyarı", "Yedeklenecek veritabanı bulunamadı.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "Yedek Kaydet", "routedesk_yedek.db", "SQLite Veritabanı (*.db)")
        if file_path:
            try:
                shutil.copy2(DB_PATH, file_path)
                QMessageBox.information(self, "Başarılı", "Veritabanı başarıyla yedeklendi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Yedekleme hatası:\n{str(e)}")

    def restore_db(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Yedek Seç", "", "SQLite Veritabanı (*.db)")
        if file_path:
            reply = QMessageBox.question(self, 'Onay', 
                "Mevcut veritabanının üzerine yazılacak. Tüm mevcut veriler silinip seçilen yedek yüklenecek. Onaylıyor musunuz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    shutil.copy2(file_path, DB_PATH)
                    QMessageBox.information(self, "Başarılı", "Veritabanı başarıyla geri yüklendi. Uygulamayı yeniden başlatmanız önerilir.")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Geri yükleme hatası:\n{str(e)}")

    def export_csv(self):
        if not os.path.exists(DB_PATH):
            QMessageBox.warning(self, "Uyarı", "Dışa aktarılacak veri bulunamadı.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "CSV Olarak Kaydet", "seferler.csv", "CSV Dosyası (*.csv)")
        if file_path:
            try:
                from database.db_manager import DBManager
                trips = DBManager.get_all_trips()
                with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Kod", "Firma", "Güzergah", "Kalkış", "Varış", "Şoför", "Plaka", "Peron", "Fiyat", "Doluluk", "Durum"])
                    writer.writerows(trips)
                QMessageBox.information(self, "Başarılı", "Veriler başarıyla CSV formatında dışa aktarıldı.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dışa aktarma hatası:\n{str(e)}")
