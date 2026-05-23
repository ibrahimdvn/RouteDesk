from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtCore import pyqtSignal, Qt

class LockScreen(QWidget):
    unlocked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        lbl_title = QLabel("Oturum Kilitlendi")
        lbl_title.setStyleSheet("font-size: 28px; font-weight: bold; color: #f3f4f6;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)
        
        lbl_desc = QLabel("Güvenlik nedeniyle oturumunuz zaman aşımına uğradı veya kilitlendi.")
        lbl_desc.setStyleSheet("color: #9ca3af; font-size: 14px;")
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_desc)
        
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Şifre (Boş bırakıp giriş yapın)")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_input.setFixedWidth(300)
        self.pwd_input.setStyleSheet("padding: 10px; font-size: 14px; background: #0f1219; border: 1px solid #3b82f6; border-radius: 6px; color: white;")
        layout.addWidget(self.pwd_input, alignment=Qt.AlignmentFlag.AlignCenter)
        
        btn_unlock = QPushButton("Kilidi Aç")
        btn_unlock.setObjectName("primaryButton")
        btn_unlock.setFixedWidth(300)
        btn_unlock.setFixedHeight(45)
        btn_unlock.clicked.connect(self.unlock)
        layout.addWidget(btn_unlock, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def unlock(self):
        self.pwd_input.clear()
        self.unlocked.emit()
