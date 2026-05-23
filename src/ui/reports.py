from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt

class Reports(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Bize Ulaşın")
        header.setStyleSheet("font-size: 28px; font-weight: 800; color: #f3f4f6;")
        layout.addWidget(header)
        
        subtitle = QLabel("RouteDesk Kurumsal İletişim ve Yasal Mevzuat Bilgileri")
        subtitle.setStyleSheet("font-size: 14px; color: #9ca3af; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Main Content Frame
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(25)
        
        # Contact Info Section
        contact_header = QLabel("Kurumsal İletişim Bilgileri")
        contact_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #3b82f6;")
        card_layout.addWidget(contact_header)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        lbl_name = QLabel("<b>İsim Soyisim:</b> İbrahim Can Düven")
        lbl_name.setStyleSheet("font-size: 15px;")
        
        lbl_phone = QLabel("<b>İrtibata Geçilecek Telefon No:</b> 0505 065 66 31")
        lbl_phone.setStyleSheet("font-size: 15px;")
        
        lbl_mail = QLabel("<b>Mail:</b> ibrahimcanduven1@gmail.com")
        lbl_mail.setStyleSheet("font-size: 15px;")
        
        info_layout.addWidget(lbl_name)
        info_layout.addWidget(lbl_phone)
        info_layout.addWidget(lbl_mail)
        
        card_layout.addLayout(info_layout)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("background-color: #374151;")
        card_layout.addWidget(divider)
        
        # Legal Section
        legal_header = QLabel("Yasal Mevzuatlar ve Kullanım Koşulları")
        legal_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #3b82f6;")
        card_layout.addWidget(legal_header)
        
        legal_text = (
            "1. İşbu RouteDesk Terminal Operasyon Yönetim Sistemi, biletleme ve yolcu taşımacılığı "
            "hizmeti veren firmaların operasyonel süreçlerini yönetmeleri amacıyla geliştirilmiştir.\n\n"
            "2. Sisteme girilen tüm yolcu bilgileri (TC Kimlik No, Ad Soyad, Telefon), 6698 Sayılı Kişisel "
            "Verilerin Korunması Kanunu (KVKK) kapsamında şirketinizin sorumluluğu altındadır ve üçüncü şahıslarla "
            "izinsiz paylaşılamaz.\n\n"
            "3. Bilet satış, iptal ve iade süreçlerinde, Karayolu Taşıma Yönetmeliği ve Tüketicinin Korunması "
            "Hakkında Kanun'da belirtilen mevzuatlara uyulması zorunludur.\n\n"
            "4. Sistem üzerindeki finansal veriler (Günlük Hasılat vb.), işletme içi analiz amaçlı olup resmi "
            "muhasebe kayıtlarının veya e-Arşiv/e-Fatura bildirimlerinin yerine geçmez.\n\n"
            "Her türlü teknik destek, sistemsel sorun veya geliştirme talebiniz için yukarıdaki iletişim kanallarından "
            "7/24 bizlere ulaşabilirsiniz."
        )
        
        lbl_legal = QLabel(legal_text)
        lbl_legal.setWordWrap(True)
        lbl_legal.setStyleSheet("font-size: 14px; color: #d1d5db; line-height: 1.6;")
        card_layout.addWidget(lbl_legal)
        
        layout.addWidget(card)
        layout.addStretch()
