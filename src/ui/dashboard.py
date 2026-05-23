from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame, 
    QTableWidget, QTableWidgetItem, QHeaderView, QListWidget, QListWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt

class DashboardCard(QFrame):
    def __init__(self, title, value, color_class=""):
        super().__init__()
        self.setObjectName("card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #6b7280; font-size: 11px; font-weight: bold; text-transform: uppercase;")
        layout.addWidget(lbl_title)
        
        self.lbl_value = QLabel(value)
        style = f"font-size: 22px; font-weight: 800;"
        if color_class == "success":
            style += " color: #22c55e;"
        elif color_class == "warning":
            style += " color: #f59e0b;"
        elif color_class == "accent":
            style += " color: #3b82f6;"
        else:
            style += " color: #f3f4f6;"
            
        self.lbl_value.setStyleSheet(style)
        layout.addWidget(self.lbl_value)
        
    def set_value(self, value):
        self.lbl_value.setText(str(value))

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Canlı Operasyon Paneli")
        header.setStyleSheet("font-size: 22px; font-weight: 800;")
        layout.addWidget(header)
        
        # Cards Grid
        grid = QGridLayout()
        grid.setSpacing(15)
        
        self.card_sales = DashboardCard("Bugünkü Bilet Satışı", "0", "accent")
        self.card_trips = DashboardCard("Aktif Seferler", "0", "success")
        self.card_occupancy = DashboardCard("Doluluk Oranı", "%0", "warning")
        self.card_seats = DashboardCard("Boş Koltuklar", "0")
        self.card_revenue = DashboardCard("Günlük Hasılat", "0 ₺", "success")
        self.card_reservations = DashboardCard("Rötarlı Seferler", "0", "warning")
        
        grid.addWidget(self.card_sales, 0, 0)
        grid.addWidget(self.card_trips, 0, 1)
        grid.addWidget(self.card_occupancy, 0, 2)
        grid.addWidget(self.card_seats, 0, 3)
        grid.addWidget(self.card_revenue, 0, 4)
        grid.addWidget(self.card_reservations, 0, 5)
        
        layout.addLayout(grid)
        
        # Bottom Layout (Table + Feed)
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)
        
        # Left Table
        table_frame = QVBoxLayout()
        lbl_recent = QLabel("Canlı Kalkış Tablosu (Departure Board)")
        lbl_recent.setStyleSheet("font-size: 14px; font-weight: bold;")
        table_frame.addWidget(lbl_recent)
        
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Saat", "Güzergah", "Firma", "Peron", "Doluluk", "Durum"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        table_frame.addWidget(self.table)
        
        bottom_layout.addLayout(table_frame, stretch=3)
        
        # Right Feed
        feed_frame = QVBoxLayout()
        lbl_feed = QLabel("Son Bilet Hareketleri")
        lbl_feed.setStyleSheet("font-size: 14px; font-weight: bold;")
        feed_frame.addWidget(lbl_feed)
        
        self.list_feed = QListWidget()
        self.list_feed.setObjectName("card")
        self.list_feed.setStyleSheet("QListWidget { background-color: #1a202c; border: 1px solid #2d3748; padding: 5px; border-radius: 6px; } QListWidget::item { padding: 10px; border-bottom: 1px solid #2d3748; }")
        feed_frame.addWidget(self.list_feed)
        
        btn_delete_ticket = QPushButton("Seçili Bileti İptal Et (Sil)")
        btn_delete_ticket.setStyleSheet("background-color: #ef4444; color: white; border: none; font-weight: bold; padding: 8px; border-radius: 4px;")
        btn_delete_ticket.clicked.connect(self.delete_ticket)
        feed_frame.addWidget(btn_delete_ticket)
        
        bottom_layout.addLayout(feed_frame, stretch=1)
        
        layout.addLayout(bottom_layout)
        
        self.load_data()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()

    def load_data(self):
        from database.db_manager import DBManager
        trips = DBManager.get_all_trips()
        
        active_trips = len(trips)
        total_occupancy = 0
        total_capacity = 0
        delayed_trips = 0
        revenue = 0
        
        for row_data in trips:
            # DB: id(0), code(1), company(2), route(3), dep(4), arr(5), driver(6), plate(7), price(8), occ(9), status(10), total_seats(12)
            trip_code = row_data[1]
            status = row_data[11]
            
            cap = row_data[12] if len(row_data) > 12 and row_data[12] is not None else 46
            
            if status == "Rötarlı":
                delayed_trips += 1
                
            tickets = DBManager.get_tickets_for_trip(trip_code)
            occ = len(tickets)
            
            total_occupancy += occ
            total_capacity += cap
            
            for t in tickets:
                try:
                    revenue += int(t[3])
                except:
                    pass
                
        occ_rate = int((total_occupancy / total_capacity * 100)) if total_capacity > 0 else 0
        free_seats = total_capacity - total_occupancy
        
        self.card_sales.set_value(str(total_occupancy))
        self.card_trips.set_value(str(active_trips))
        self.card_occupancy.set_value(f"%{occ_rate}")
        self.card_seats.set_value(str(free_seats))
        self.card_revenue.set_value(f"{revenue:,} ₺")
        self.card_reservations.set_value(str(delayed_trips))
        
        # Update Table (First 10 trips)
        recent_trips = trips[:10]
        self.table.setRowCount(len(recent_trips))
        
        for row, row_data in enumerate(recent_trips):
            trip_code = row_data[1]
            cap = row_data[12] if len(row_data) > 12 and row_data[12] is not None else 46
            occ = len(DBManager.get_tickets_for_trip(trip_code))
            dynamic_occ = f"{occ}/{cap}"
            
            display_data = [row_data[3], row_data[2], row_data[1], row_data[8], dynamic_occ, row_data[11]]
            for col, item_data in enumerate(display_data):
                item = QTableWidgetItem(str(item_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

        # Update Feed List dynamically with recent ticket sales
        self.list_feed.clear()
        
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, trip_code, seat, passenger_name FROM tickets ORDER BY id DESC LIMIT 8")
        recent_tickets = cursor.fetchall()
        conn.close()
        
        if recent_tickets:
            for t in recent_tickets:
                item = QListWidgetItem(f"🎟️ Bilet Satışı | {t[1]} Seferi, Koltuk: {t[2]} ({t[3]})")
                item.setData(Qt.ItemDataRole.UserRole, t[0])
                self.list_feed.addItem(item)
        else:
            self.list_feed.addItem("Henüz bilet satışı yapılmadı.")

    def delete_ticket(self):
        from PyQt6.QtWidgets import QMessageBox
        from database.db_manager import DBManager
        
        selected = self.list_feed.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Seçim Yapılmadı", "Lütfen iptal etmek istediğiniz bileti sağdaki listeden seçin.")
            return
            
        item = selected[0]
        ticket_id = item.data(Qt.ItemDataRole.UserRole)
        
        if not ticket_id:
            return
            
        reply = QMessageBox.question(self, 'Onay', 
            f"Seçili bileti iptal etmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
        if reply == QMessageBox.StandardButton.Yes:
            DBManager.delete_ticket(ticket_id)
            self.load_data()
            QMessageBox.information(self, "Başarılı", "Bilet başarıyla iptal edildi ve sistemden silindi.")
