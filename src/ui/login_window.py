from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RouteDesk - Operatör Girişi")
        self.setFixedSize(400, 500)
        self.operator_name = None
        
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QIcon
        import os
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 400) // 2
        y = (screen.height() - 500) // 2
        self.move(x, y)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Logo / Header
        lbl_logo = QLabel("RouteDesk")
        lbl_logo.setStyleSheet("font-size: 32px; font-weight: 900; color: #3b82f6; margin-bottom: 10px;")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_logo)
        
        lbl_sub = QLabel("Terminal Operasyon Sistemi")
        lbl_sub.setStyleSheet("font-size: 14px; color: #9ca3af; margin-bottom: 20px;")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_sub)
        
        # Mode Toggle (Login vs Register)
        self.is_login_mode = True
        
        self.mode_btn = QPushButton("Hesabınız yok mu? Kayıt Olun")
        self.mode_btn.setStyleSheet("background: transparent; color: #60a5fa; border: none; font-weight: bold;")
        self.mode_btn.clicked.connect(self.toggle_mode)
        layout.addWidget(self.mode_btn)
        
        # Form Container
        self.form_frame = QFrame()
        self.form_layout = QVBoxLayout(self.form_frame)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(15)
        
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("İsim Soyisim")
        self.fullname_input.setFixedHeight(40)
        self.form_layout.addWidget(self.fullname_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.form_layout.addWidget(self.password_input)
        
        layout.addWidget(self.form_frame)
        
        layout.addStretch()
        
        # Action Button
        self.action_btn = QPushButton("Giriş Yap")
        self.action_btn.setObjectName("primaryButton")
        self.action_btn.setFixedHeight(45)
        self.action_btn.clicked.connect(self.process_action)
        layout.addWidget(self.action_btn)
        
        # Check if any operators exist, if not force register mode
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM operators")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            self.toggle_mode()
            self.mode_btn.setVisible(False)

    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        if self.is_login_mode:
            self.action_btn.setText("Giriş Yap")
            self.mode_btn.setText("Hesabınız yok mu? Kayıt Olun")
        else:
            self.action_btn.setText("Kayıt Ol")
            self.mode_btn.setText("Zaten hesabınız var mı? Giriş Yapın")

    def process_action(self):
        fullname = self.fullname_input.text().strip()
        password = self.password_input.text().strip()
        
        if not fullname or not password:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
            return
            
        if self.is_login_mode:
            full_name_db = DBManager.verify_operator(fullname, password)
            if full_name_db:
                self.operator_name = f"Operatör: {full_name_db}"
                self.accept()
            else:
                QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı.")
        else:
            success = DBManager.register_operator(fullname, password, fullname)
            if success:
                QMessageBox.information(self, "Başarılı", "Kayıt başarılı. Şimdi giriş yapabilirsiniz.")
                self.toggle_mode()
                self.password_input.clear()
            else:
                QMessageBox.warning(self, "Hata", "Bu isimle zaten bir kayıt mevcut.")
