from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGridLayout, QFrame, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager

class SeatButton(QPushButton):
    def __init__(self, seat_num, status="available", passenger_info=None):
        super().__init__(str(seat_num))
        self.seat_num = seat_num
        self.setFixedSize(50, 50)
        self.status = status
        self.passenger_info = passenger_info
        
        self.update_style()
        self.update_tooltip()

    def set_status(self, status, passenger_info=None):
        self.status = status
        self.passenger_info = passenger_info
        self.update_style()
        self.update_tooltip()

    def update_style(self):
        self.setProperty("class", f"seat-{self.status}")
        self.style().unpolish(self)
        self.style().polish(self)
        
    def update_tooltip(self):
        if self.passenger_info:
            self.setToolTip(f"Koltuk {self.text()}\nYolcu: {self.passenger_info['name']}\nTel: {self.passenger_info['phone']}")
        else:
            self.setToolTip(f"Koltuk {self.text()} (Boş)")
            
    def toggle_seat(self):
        if self.status == "available":
            self.status = "selected"
        elif self.status == "selected":
            self.status = "available"
        self.update_style()

class SeatReservation(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(30)
        
        # Left Panel (Controls)
        left_panel = QVBoxLayout()
        left_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        header = QLabel("Koltuk Planı & Ayarlar")
        header.setStyleSheet("font-size: 20px; font-weight: 800; margin-bottom: 20px;")
        left_panel.addWidget(header)
        
        # Trip Selector
        lbl_trip = QLabel("Sefer Seçimi:")
        lbl_trip.setStyleSheet("font-weight: bold; color: #9ca3af;")
        self.trip_select = QComboBox()
        self.trip_select.setFixedWidth(250)
        self.trip_select.currentIndexChanged.connect(self.load_seats)
        left_panel.addWidget(lbl_trip)
        left_panel.addWidget(self.trip_select)
        
        left_panel.addSpacing(15)
        
        # Layout / Seat Count Selector
        lbl_layout = QLabel("Otobüs Tipi / Koltuk Sayısı:")
        lbl_layout.setStyleSheet("font-weight: bold; color: #9ca3af;")
        self.layout_select = QComboBox()
        self.layout_select.setFixedWidth(250)
        self.layout_select.addItems(["2+2 Standart (46 Koltuk)", "2+1 VIP (38 Koltuk)", "3+1 Özel (50 Koltuk)"])
        self.layout_select.currentIndexChanged.connect(self.force_layout_change)
        left_panel.addWidget(lbl_layout)
        left_panel.addWidget(self.layout_select)
        
        left_panel.addSpacing(25)
        
        # Legend
        lbl_legend = QLabel("Renk Göstergeleri:")
        lbl_legend.setStyleSheet("font-weight: bold; color: #9ca3af; margin-bottom: 5px;")
        left_panel.addWidget(lbl_legend)
        
        legend_layout = QVBoxLayout()
        legend_layout.setSpacing(10)
        legend_layout.addWidget(self.create_legend_item("Boş", "gray"))
        legend_layout.addWidget(self.create_legend_item("Seçili", "blue"))
        legend_layout.addWidget(self.create_legend_item("Dolu", "red"))
        legend_layout.addWidget(self.create_legend_item("Rezerve", "orange"))
        
        left_panel.addLayout(legend_layout)
        left_panel.addStretch()
        
        main_layout.addLayout(left_panel, stretch=1)
        
        # Bus Layout Container
        self.bus_container = QFrame()
        self.bus_container.setObjectName("card")
        
        self.bus_layout = QVBoxLayout(self.bus_container)
        self.bus_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Center the bus container horizontally and vertically in the remaining space
        center_h_layout = QHBoxLayout()
        center_h_layout.addStretch()
        center_h_layout.addWidget(self.bus_container)
        center_h_layout.addStretch()
        
        center_v_layout = QVBoxLayout()
        center_v_layout.addStretch()
        center_v_layout.addLayout(center_h_layout)
        center_v_layout.addStretch()
        
        main_layout.addLayout(center_v_layout, stretch=3)

        self.seat_buttons = []
        self.load_trips()
        
    def force_layout_change(self):
        self.load_seats(force_layout=self.layout_select.currentText())

    def showEvent(self, event):
        super().showEvent(event)
        self.load_trips()
        
    def load_trips(self):
        self.trip_select.clear()
        trips = DBManager.get_all_trips()
        for row in trips:
            # row: id(0), code(1), company(2), route(3), dep(4), ... total_seats(12), layout(13)
            total_seats = row[12] if len(row) > 12 and row[12] is not None else 46
            layout_type = row[13] if len(row) > 13 and row[13] is not None else "2+2"
            
            self.trip_select.addItem(f"{row[1]} | {row[3]} | {row[4]}", userData={"total_seats": total_seats, "layout": layout_type})
            
    def load_seats(self, force_layout=None):
        # Clear existing layout
        while self.bus_layout.count():
            item = self.bus_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget(): sub.widget().deleteLater()
                item.layout().deleteLater()
                
        self.seat_buttons.clear()
        
        trip_idx = self.trip_select.currentIndex()
        
        user_data = None
        if trip_idx >= 0:
            user_data = self.trip_select.itemData(trip_idx)
            
        if not user_data:
            user_data = {"total_seats": 46, "layout": "2+2"}
            
        # If user explicitly changed the layout dropdown, override it
        if isinstance(force_layout, str):
            if "2+1" in force_layout:
                layout_type = "2+1"
                total_seats = 38
            elif "3+1" in force_layout:
                layout_type = "3+1"
                total_seats = 50
            else:
                layout_type = "2+2"
                total_seats = 46
        else:
            total_seats = user_data["total_seats"]
            layout_type = user_data["layout"]
            
            # Sync the dropdown with the trip's actual layout silently
            self.layout_select.blockSignals(True)
            if layout_type == "2+1":
                self.layout_select.setCurrentIndex(1)
            elif layout_type == "3+1":
                self.layout_select.setCurrentIndex(2)
            else:
                self.layout_select.setCurrentIndex(0)
            self.layout_select.blockSignals(False)
        
        # Driver area
        driver_label = QLabel("Direksiyon")
        driver_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        driver_label.setStyleSheet("color: #6b7280; padding: 15px; font-weight: bold; font-size: 14px; border: 2px dashed #4b5563; border-radius: 8px;")
        
        # Seats Grid
        seats_grid = QGridLayout()
        seats_grid.setSpacing(15)
        
        # Add driver to the left (Col 0, spans row 0 to 1)
        seats_grid.addWidget(driver_label, 0, 0, 2, 1)
        
        # Aisle definition
        if layout_type == "3+1":
            aisle_row = 3
            seats_grid.setRowMinimumHeight(aisle_row, 30)
        else:
            aisle_row = 2
            seats_grid.setRowMinimumHeight(aisle_row, 30)
        
        seat_num = 1
        col = 1
        
        while seat_num <= total_seats:
            if layout_type == "2+1":
                # 2+1: Single on bottom (Row 3), Double on top (Row 1, Row 0)
                rows = [3, 1, 0]
            elif layout_type == "3+1":
                # 3+1: Single on bottom (Row 4), Triple on top (Row 2, Row 1, Row 0)
                rows = [4, 2, 1, 0]
            else:
                # 2+2: Double on bottom (Row 4, Row 3), Double on top (Row 1, Row 0)
                rows = [4, 3, 1, 0]
                
            for r in rows:
                if seat_num > total_seats:
                    break
                btn = SeatButton(seat_num, "available", None)
                btn.clicked.connect(lambda checked, b=btn: self.seat_clicked(b))
                self.seat_buttons.append(btn)
                seats_grid.addWidget(btn, r, col)
                seat_num += 1
                
            col += 1
            
        self.bus_layout.addLayout(seats_grid)
            
        trip = self.trip_select.currentText()
        if not trip:
            return
            
        trip_code = trip.split("|")[0].strip()
        tickets = DBManager.get_tickets_for_trip(trip_code)
        
        for ticket in tickets:
            seat_num_str = ticket[0]
            if seat_num_str.isdigit():
                sn = int(seat_num_str)
                for btn in self.seat_buttons:
                    if btn.seat_num == sn:
                        btn.set_status("occupied", {"name": ticket[1], "phone": ticket[2]})
                        break

    def seat_clicked(self, btn):
        if btn.status in ["occupied", "reserved"]:
            QMessageBox.information(self, "Koltuk Bilgisi", f"Koltuk {btn.text()}\nAd: {btn.passenger_info['name']}\nTel: {btn.passenger_info['phone']}")
            return
            
        btn.toggle_seat()

    def create_legend_item(self, text, color_name):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 10, 0)
        
        color_box = QLabel()
        color_box.setFixedSize(14, 14)
        
        colors = {
            "gray": "#2d3748",
            "blue": "#3b82f6",
            "red": "#ef4444", # Occupied
            "orange": "#d97706"
        }
        color_box.setStyleSheet(f"background-color: {colors[color_name]}; border-radius: 3px;")
        
        label = QLabel(text)
        label.setStyleSheet("font-size: 11px; color: #9ca3af; font-weight: bold;")
        
        layout.addWidget(color_box)
        layout.addWidget(label)
        layout.addStretch()
        return widget
