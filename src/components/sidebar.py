from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QButtonGroup, QFrame
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QDateTime

class Sidebar(QWidget):
    navigation_requested = pyqtSignal(str)

    def __init__(self, operator_name="Operatör: Ahmet Y."):
        super().__init__()
        self.operator_name = operator_name
        self.setObjectName("sidebar")
        self.setFixedWidth(240)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Header
        header = QLabel("RouteDesk")
        header.setObjectName("sidebarHeader")
        layout.addWidget(header)
        
        # Operator Profile
        profile_frame = QFrame()
        profile_frame.setObjectName("sidebarProfile")
        profile_layout = QVBoxLayout(profile_frame)
        profile_layout.setContentsMargins(10, 10, 10, 10)
        profile_layout.setSpacing(2)
        
        self.lbl_time = QLabel()
        self.lbl_time.setStyleSheet("color: #9ca3af; font-size: 11px;")
        profile_layout.addWidget(self.lbl_time)
        
        lbl_name = QLabel(self.operator_name)
        lbl_name.setObjectName("profileName")
        profile_layout.addWidget(lbl_name)
        
        lbl_status = QLabel("● Aktif")
        lbl_status.setObjectName("profileStatus")
        profile_layout.addWidget(lbl_status)
        
        layout.addWidget(profile_frame)
        layout.addSpacing(10)
        
        # Sections
        self.add_section_label(layout, "Operasyon")
        self.add_nav_button(layout, "Kontrol Paneli", "dashboard", True)
        self.add_nav_button(layout, "Sefer Yönetimi", "trips")
        self.add_nav_button(layout, "Hızlı Bilet Satış", "tickets")
        self.add_nav_button(layout, "Koltuk Rezervasyonu", "seats")
        
        self.add_section_label(layout, "Yönetim")
        self.add_nav_button(layout, "Müşteriler", "customers")
        self.add_nav_button(layout, "Bize Ulaşın", "reports")
        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.add_section_label(layout, "Sistem")
        self.add_nav_button(layout, "Ayarlar", "settings")
        self.add_nav_button(layout, "Oturumu Kilitle", "lock")
        
        layout.addSpacing(20)

        # Timer for Live Clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss")
        self.lbl_time.setText(f"{current_time}")

    def add_section_label(self, layout, text):
        label = QLabel(text)
        label.setObjectName("sectionLabel")
        layout.addWidget(label)

    def add_nav_button(self, layout, text, target_view, checked=False):
        btn = QPushButton()
        btn.setText(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        self.button_group.addButton(btn)
        btn.clicked.connect(lambda checked, tv=target_view: self.navigation_requested.emit(tv))
        layout.addWidget(btn)
