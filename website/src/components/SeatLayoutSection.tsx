import Image from "next/image";
import { Settings, CheckCircle2 } from "lucide-react";

export default function SeatLayoutSection() {
  const capabilities = [
    "2+1 VIP, 2+2 Standart ve 3+1 Özel düzenleri arasında anında geçiş yapın.",
    "Bilet satış veritabanı ile gerçek zamanlı senkronizasyon.",
    "Boş, Seçili, Dolu ve Rezerve durumları için görsel göstergeler.",
    "Dolu koltukların üzerine gelindiğinde yolcu bilgilerini önizleme."
  ];

  return (
    <section className="py-24 bg-section border-y border-border">
      <div className="container mx-auto px-6">
        <div className="flex flex-col lg:flex-row items-center gap-16">
          <div className="flex-1 w-full">
            <div className="rounded-xl border border-border bg-card p-2 shadow-2xl relative">
              <div className="absolute -top-4 -left-4 w-20 h-20 bg-accent/20 blur-2xl rounded-full"></div>
              <Image 
                src="/screenshots/media__1779578497908.png" 
                alt="RouteDesk Seat Reservation Editor" 
                width={1280} 
                height={800} 
                className="rounded-lg w-full h-auto object-cover border border-border/50 relative z-10"
              />
            </div>
          </div>
          
          <div className="flex-1">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-card border border-border text-xs font-medium text-accent mb-6">
              <Settings className="w-3.5 h-3.5" />
              <span>Dinamik Koltuk Yapılandırması</span>
            </div>
            <h2 className="text-3xl font-bold text-primary mb-6">Akıllı Koltuk Planı Oluşturucu</h2>
            <p className="text-secondary mb-8 leading-relaxed">
              Filonuzdaki herhangi bir otobüs yapısına uyum sağlayın. RouteDesk'in dinamik koltuk planı oluşturucusu, operatörlerinizin koltukları sıfır zorlukla yapılandırmasına, görüntülemesine ve atamasına olanak tanır.
            </p>
            
            <ul className="space-y-4">
              {capabilities.map((text, idx) => (
                <li key={idx} className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-accent shrink-0 mt-0.5" />
                  <span className="text-sm text-secondary">{text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
