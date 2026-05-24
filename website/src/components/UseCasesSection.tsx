import { Building2, Navigation, Briefcase, Network } from "lucide-react";

export default function UseCasesSection() {
  const useCases = [
    { icon: <Building2 className="w-5 h-5" />, title: "Yerel Otobüs Terminalleri", desc: "Günlük kalkışları, peron atamalarını ve bölgesel bilet satışlarını zahmetsizce yönetin." },
    { icon: <Briefcase className="w-5 h-5" />, title: "Ulaşım Acenteleri", desc: "Birden fazla filoyu koordine edin ve rota talebine göre fiyatlandırmayı dinamik olarak ayarlayın." },
    { icon: <Navigation className="w-5 h-5" />, title: "VIP Taşıma Hizmetleri", desc: "2+1 koltuk düzenlerinden yararlanın ve yüksek kalitede müşteri kayıtları tutun." },
    { icon: <Network className="w-5 h-5" />, title: "Bölgesel Bilet Ofisleri", desc: "Bireysel şubeleri sağlam ve bağımsız bir biletleme ortamıyla donatın." }
  ];

  return (
    <section className="py-24">
      <div className="container mx-auto px-6">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-primary mb-4">Sektör İçin Üretildi</h2>
          <p className="text-secondary">RouteDesk, tekli bilet ofislerinden bölgesel transit merkezlerine kadar çeşitli ulaşım iş modellerine uyum sağlar.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {useCases.map((useCase, idx) => (
            <div key={idx} className="bg-section border border-border p-6 rounded-lg">
              <div className="w-10 h-10 rounded bg-card border border-border flex items-center justify-center text-primary mb-4">
                {useCase.icon}
              </div>
              <h3 className="font-semibold text-primary mb-2">{useCase.title}</h3>
              <p className="text-sm text-secondary">{useCase.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
