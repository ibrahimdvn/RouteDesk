from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFormLayout, QFrame, QComboBox, QMessageBox, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QMarginsF
from PyQt6.QtGui import QTextDocument, QPdfWriter, QPageSize, QPageLayout
import os
import datetime

class TicketSales(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("Bilet Satış İşlemleri")
        header.setStyleSheet("font-size: 22px; font-weight: 800;")
        layout.addWidget(header)
        
        # Progress Indicator
        progress_layout = QHBoxLayout()
        steps = ["1. Yolcu Bilgileri", "2. Sefer Seçimi", "3. Koltuk & Ödeme"]
        for i, step in enumerate(steps):
            lbl = QLabel(step)
            lbl.setStyleSheet(f"font-weight: bold; padding: 5px 15px; border-radius: 15px; background-color: {'#3b82f6' if i==0 else '#2d3748'}; color: {'white' if i==0 else '#9ca3af'};")
            progress_layout.addWidget(lbl)
            if i < len(steps)-1:
                arrow = QLabel("→")
                arrow.setStyleSheet("color: #4a5568;")
                progress_layout.addWidget(arrow)
        progress_layout.addStretch()
        layout.addLayout(progress_layout)
        
        main_content = QHBoxLayout()
        main_content.setSpacing(20)
        
        # Left Form (Guided Process)
        form_frame = QFrame()
        form_frame.setObjectName("card")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Customer Section
        lbl_cust = QLabel("Yolcu Bilgileri")
        lbl_cust.setStyleSheet("font-weight: bold; color: #9ca3af; margin-bottom: 5px;")
        form_layout.addWidget(lbl_cust)
        
        phone_layout = QHBoxLayout()
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefon No (Müşteri Ara)")
        
        btn_search_cust = QPushButton("Bul")
        btn_search_cust.setObjectName("primaryButton")
        btn_search_cust.clicked.connect(self.search_customer)
        
        phone_layout.addWidget(self.phone_input)
        phone_layout.addWidget(btn_search_cust)
        form_layout.addLayout(phone_layout)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ad Soyad")
        form_layout.addWidget(self.name_input)
        
        self.tc_input = QLineEdit()
        self.tc_input.setPlaceholderText("T.C. Kimlik No")
        form_layout.addWidget(self.tc_input)
        
        form_layout.addSpacing(15)
        
        # Trip Section
        lbl_trip = QLabel("Sefer ve Koltuk Seçimi")
        lbl_trip.setStyleSheet("font-weight: bold; color: #9ca3af; margin-bottom: 5px;")
        form_layout.addWidget(lbl_trip)
        
        self.trip_select = QComboBox()
        self.load_trips()
        form_layout.addWidget(self.trip_select)
        
        self.seat_input = QLineEdit()
        self.seat_input.setPlaceholderText("Koltuk No (Örn: 12, 14)")
        self.seat_input.textChanged.connect(self.update_preview)
        form_layout.addWidget(self.seat_input)
        
        form_layout.addSpacing(15)
        
        # Payment Section
        lbl_pay = QLabel("Ödeme Yöntemi")
        lbl_pay.setStyleSheet("font-weight: bold; color: #9ca3af; margin-bottom: 5px;")
        form_layout.addWidget(lbl_pay)
        
        pay_layout = QHBoxLayout()
        self.pay_group = QButtonGroup()
        
        r_cash = QRadioButton("Nakit")
        r_cash.setChecked(True)
        r_card = QRadioButton("Kredi Kartı")
        r_havale = QRadioButton("Cari/Havale")
        
        self.pay_group.addButton(r_cash)
        self.pay_group.addButton(r_card)
        self.pay_group.addButton(r_havale)
        
        pay_layout.addWidget(r_cash)
        pay_layout.addWidget(r_card)
        pay_layout.addWidget(r_havale)
        form_layout.addLayout(pay_layout)
        
        form_layout.addStretch()
        main_content.addWidget(form_frame, stretch=2)
        
        # Right Checkout & Live Preview
        preview_frame = QFrame()
        preview_frame.setObjectName("card")
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_summary = QLabel("Canlı Bilet Önizleme")
        lbl_summary.setStyleSheet("font-size: 16px; font-weight: bold;")
        preview_layout.addWidget(lbl_summary)
        
        # Ticket Mockup
        ticket_mock = QFrame()
        ticket_mock.setStyleSheet("background-color: #0f1219; border: 1px dashed #4a5568; border-radius: 8px;")
        mock_layout = QVBoxLayout(ticket_mock)
        
        self.preview_route = QLabel("Güzergah: İzmir -> İstanbul")
        self.preview_route.setStyleSheet("font-weight: bold; color: #3b82f6;")
        mock_layout.addWidget(self.preview_route)
        
        self.preview_passenger = QLabel("Yolcu: -")
        mock_layout.addWidget(self.preview_passenger)
        
        self.preview_seats = QLabel("Koltuklar: -")
        mock_layout.addWidget(self.preview_seats)
        
        self.preview_time = QLabel("Tarih/Saat: 24.05.2026 14:00")
        mock_layout.addWidget(self.preview_time)
        
        preview_layout.addWidget(ticket_mock)
        
        preview_layout.addStretch()
        
        self.lbl_total = QLabel("Toplam: 0.00 ₺")
        self.lbl_total.setStyleSheet("font-size: 24px; font-weight: 800; color: #22c55e;")
        preview_layout.addWidget(self.lbl_total)
        
        self.btn_print = QPushButton("Ödemeyi Al ve Yazdır")
        self.btn_print.setObjectName("primaryButton")
        self.btn_print.setFixedHeight(45)
        self.btn_print.clicked.connect(self.complete_sale)
        preview_layout.addWidget(self.btn_print)
        
        main_content.addWidget(preview_frame, stretch=1)
        
        layout.addLayout(main_content)
        
        self.name_input.textChanged.connect(self.update_preview)
        self.trip_select.currentIndexChanged.connect(self.update_preview)
        self.seat_input.textChanged.connect(self.update_preview)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_trips()

    def load_trips(self):
        self.trip_select.clear()
        from database.db_manager import DBManager
        trips = DBManager.get_all_trips()
        for row in trips:
            # Format: "TR-1004 | İzmir -> İstanbul | 14:00"
            code = row[1]
            route = row[3]
            time = row[4]
            try:
                price = int(row[9])
            except ValueError:
                price = 0
            self.trip_select.addItem(f"{code} | {route} | {time}", userData={"price": price})

    def search_customer(self):
        phone = self.phone_input.text().strip()
        if not phone:
            return
            
        from database.db_manager import DBManager
        result = DBManager.get_customer_by_phone(phone)
        if result:
            self.name_input.setText(result[0])
            self.tc_input.setText(result[1])
        else:
            QMessageBox.information(self, "Bulunamadı", "Bu telefon numarasına ait müşteri kaydı bulunamadı. Lütfen yeni müşteri bilgilerini girin.")
            self.name_input.clear()
            self.tc_input.clear()

    def update_preview(self):
        name = self.name_input.text() or "-"
        self.preview_passenger.setText(f"Yolcu: {name}")
        
        trip = self.trip_select.currentText()
        route = trip.split("|")[1].strip() if "|" in trip else trip
        time = trip.split("|")[2].strip() if "|" in trip else "-"
        
        self.preview_route.setText(f"Güzergah: {route}")
        self.preview_time.setText(f"Tarih/Saat: {time}")
        
        seats_text = self.seat_input.text()
        seats = [s.strip() for s in seats_text.split(",") if s.strip()]
        self.preview_seats.setText(f"Koltuklar: {', '.join(seats) if seats else '-'}")
        
        user_data = self.trip_select.currentData()
        price = user_data.get("price", 0) if user_data else 0
        total = len(seats) * price
        self.lbl_total.setText(f"Toplam: {total:,} ₺")

    def complete_sale(self):
        if not self.seat_input.text() or not self.name_input.text():
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen Yolcu Adı ve Koltuk Numarası giriniz.")
            return
            
        trip = self.trip_select.currentText()
        if not trip:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen sefer seçiniz.")
            return
            
        trip_code = trip.split("|")[0].strip()
        seats_text = self.seat_input.text()
        seats = [s.strip() for s in seats_text.split(",") if s.strip()]
        
        user_data = self.trip_select.currentData()
        price = user_data.get("price", 0) if user_data else 0
        
        # Confirmation Modal
        msg = QMessageBox(self)
        msg.setWindowTitle('Onay')
        msg.setText(f"{self.name_input.text()} için bilet kesilecektir.\nToplam: {len(seats)*price:,} ₺\nOnaylıyor musunuz?")
        msg.setIcon(QMessageBox.Icon.Question)
        evet = msg.addButton("Evet", QMessageBox.ButtonRole.YesRole)
        msg.addButton("Hayır", QMessageBox.ButtonRole.NoRole)
        msg.setDefaultButton(evet)
        msg.exec()

        if msg.clickedButton() == evet:
            from database.db_manager import DBManager
            passenger_name = self.name_input.text()
            tc_no = self.tc_input.text()
            
            # 1. Save to DB
            for seat in seats:
                DBManager.add_ticket(trip_code, seat, passenger_name, tc_no, price)
                
            # 2. Generate PDF
            try:
                self.generate_pdf(trip_code, passenger_name, seats)
            except Exception as e:
                QMessageBox.warning(self, "PDF Hatası", f"Bilet oluşturulurken hata oluştu: {str(e)}")
                
            QMessageBox.information(self, "Başarılı", "Bilet satışı onaylandı ve PDF olarak masaüstüne kaydedildi.")
            self.phone_input.clear()
            self.name_input.clear()
            self.tc_input.clear()
            self.seat_input.clear()
            self.update_preview()

    def generate_pdf(self, trip_code, passenger_name, seats):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Bilet_{trip_code}_{timestamp}.pdf"
        filepath = os.path.join(desktop, filename)
        
        trip_full = self.trip_select.currentText()
        route = trip_full.split("|")[1].strip() if "|" in trip_full else trip_full
        time = trip_full.split("|")[2].strip() if "|" in trip_full else "-"
        date_now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: sans-serif; }}
                h1 {{ color: #1d4ed8; }}
                h3 {{ color: #4b5563; }}
                table {{ border-collapse: collapse; width: 100%; }}
                td {{ padding: 8px; border-bottom: 1px solid #e5e7eb; }}
                .label {{ font-weight: bold; color: #4b5563; width: 30%; }}
                .value {{ font-weight: bold; color: #111827; }}
            </style>
        </head>
        <body>
            <center>
                <h1>RouteDesk Bilet</h1>
                <h3>Resmi Yolcu Taşıma Belgesi</h3>
                <hr>
            </center>
            <br>
            <table width="100%">
                <tr>
                    <td class="label">Yolcu Adi:</td>
                    <td class="value">{passenger_name}</td>
                </tr>
                <tr>
                    <td class="label">Sefer Kodu:</td>
                    <td class="value">{trip_code}</td>
                </tr>
                <tr>
                    <td class="label">Guzergah:</td>
                    <td class="value">{route}</td>
                </tr>
                <tr>
                    <td class="label">Tarih / Saat:</td>
                    <td class="value">{time}</td>
                </tr>
                <tr>
                    <td class="label">Koltuk No:</td>
                    <td class="value">{', '.join(seats)}</td>
                </tr>
                <tr>
                    <td class="label">Islem Zamani:</td>
                    <td class="value">{date_now}</td>
                </tr>
            </table>
            <br><br>
            <center>
                <p style="color: #6b7280; font-size: 12px;">Bu bilet RouteDesk Terminal Sistemi tarafindan olusturulmustur.<br>Iyi yolculuklar dileriz.</p>
            </center>
        </body>
        </html>
        """
        
        doc = QTextDocument()
        doc.setHtml(html)
        
        pdf = QPdfWriter(filepath)
        pdf.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        
        # In PyQt6, page margins are handled via pageLayout
        layout = pdf.pageLayout()
        layout.setMargins(QMarginsF(20, 20, 20, 20))
        pdf.setPageLayout(layout)
        
        doc.print(pdf)
