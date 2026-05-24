from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout, QApplication
)
from PyQt6.QtCore import Qt, QTimer, QEvent

from components.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.trip_management import TripManagement
from ui.ticket_sales import TicketSales
from ui.seat_reservation import SeatReservation
from ui.customer_management import CustomerManagement
from ui.reports import Reports
from ui.settings import Settings
from ui.lock_screen import LockScreen

class MainWindow(QMainWindow):
    def __init__(self, operator_name="Operatör: Ahmet Y."):
        super().__init__()
        self.operator_name = operator_name
        self.setWindowTitle("RouteDesk - Terminal Operasyon Yönetim Sistemi")
        self.setMinimumSize(1280, 800)
        
        from PyQt6.QtGui import QIcon
        import os
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.timeout.connect(self.lock_session)
        self.current_timeout_ms = 0
        
        self.last_view = "dashboard"
        
        self.init_ui()
        QApplication.instance().installEventFilter(self)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar(self.operator_name)
        main_layout.addWidget(self.sidebar)
        
        # Main Content Area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Initialize views
        self.views = {
            "dashboard": Dashboard(),
            "trips": TripManagement(),
            "tickets": TicketSales(),
            "seats": SeatReservation(),
            "customers": CustomerManagement(),
            "reports": Reports(),
            "settings": Settings(),
            "lock": LockScreen()
        }
        
        for view in self.views.values():
            self.content_stack.addWidget(view)
            
        # Connect sidebar signals
        self.sidebar.navigation_requested.connect(self.navigate_to)
        
        # Connect settings saved signal
        self.views["settings"].settings_saved.connect(self.apply_settings)
        
        # Connect unlock signal
        self.views["lock"].unlocked.connect(self.unlock_session)
        
        # Status Bar
        self.statusBar().showMessage("Sistem Hazır | Operasyon Modu Aktif")
        
        # Set default view
        self.navigate_to("dashboard")
        
        # Initial settings application
        self.apply_settings()

    def apply_settings(self):
        import os
        import json
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    
                    window_mode = config.get("window_mode", "Pencereli")
                    if window_mode == "Tam Ekran (Fullscreen)":
                        self.showFullScreen()
                    elif window_mode == "Genişletilmiş (Maximized)":
                        self.showMaximized()
                    else:
                        self.showNormal()
                        self.setMinimumSize(1280, 800)
                        
                        # Center window
                        screen = QApplication.primaryScreen().availableGeometry()
                        size = self.geometry()
                        x = (screen.width() - size.width()) // 2
                        y = (screen.height() - size.height()) // 2
                        self.move(x, y)
                        
                    timeout_setting = config.get("timeout", "15 Dakika")
                    if timeout_setting == "15 Dakika":
                        self.current_timeout_ms = 15 * 60 * 1000
                    elif timeout_setting == "30 Dakika":
                        self.current_timeout_ms = 30 * 60 * 1000
                    elif timeout_setting == "1 Saat":
                        self.current_timeout_ms = 60 * 60 * 1000
                    else: # Hiçbir Zaman
                        self.current_timeout_ms = 0
                        
                    self.reset_inactivity_timer()
                        
            except Exception as e:
                pass

    def navigate_to(self, view_name: str):
        if view_name == "lock":
            self.lock_session()
        elif view_name in self.views:
            if view_name != "lock":
                self.last_view = view_name
            target = self.views[view_name]
            self.content_stack.setCurrentWidget(target)
            
            # Refresh data on navigation to keep views in sync
            if hasattr(target, "load_data"):
                target.load_data()
            
            if hasattr(target, "load_trips"):
                target.load_trips()
                
            if hasattr(target, "load_seats"):
                target.load_seats()

    def lock_session(self):
        self.inactivity_timer.stop()
        self.sidebar.hide()
        self.content_stack.setCurrentWidget(self.views["lock"])
        self.statusBar().showMessage("Oturum Kilitlendi.")

    def unlock_session(self):
        self.sidebar.show()
        self.content_stack.setCurrentWidget(self.views[self.last_view])
        self.statusBar().showMessage("Sistem Hazır | Operasyon Modu Aktif")
        self.reset_inactivity_timer()

    def reset_inactivity_timer(self):
        if self.current_timeout_ms > 0:
            self.inactivity_timer.start(self.current_timeout_ms)
        else:
            self.inactivity_timer.stop()

    def eventFilter(self, obj, event):
        # Reset timer on any mouse or keyboard activity
        if event.type() in (QEvent.Type.KeyPress, QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress, QEvent.Type.Wheel):
            # Only reset if we are not currently locked
            if self.content_stack.currentWidget() != self.views["lock"]:
                self.reset_inactivity_timer()
        return super().eventFilter(obj, event)
