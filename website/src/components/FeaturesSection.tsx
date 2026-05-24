import { Ticket, Map, LayoutGrid, Users, LineChart, WifiOff, Zap } from "lucide-react";

const features = [
  {
    icon: <Map className="w-5 h-5" />,
    title: "Sefer Yönetimi",
    description: "Kalkış noktalarını, rotaları ve canlı durum güncellemelerini kolayca planlayın ve yönetin."
  },
  {
    icon: <Ticket className="w-5 h-5" />,
    title: "Bilet Satışları",
    description: "Dinamik fiyatlandırma ve anlık veritabanı senkronizasyonu ile bilet satışlarını işleyin."
  },
  {
    icon: <LayoutGrid className="w-5 h-5" />,
    title: "Dinamik Koltuk Planı",
    description: "Canlı doluluk göstergeleriyle 2+1 VIP veya 2+2 standart gibi yapılandırılabilir koltuk düzenleri."
  },
  {
    icon: <Users className="w-5 h-5" />,
    title: "Müşteri Yönetimi",
    description: "Yolcu kayıtlarını ve rezervasyon durumlarını merkezi bir sistemde takip edin."
  },
  {
    icon: <LineChart className="w-5 h-5" />,
    title: "Hasılat Analitiği",
    description: "Günlük geliri, doluluk oranlarını ve aktif seferleri gerçek zamanlı olarak izleyin."
  },
  {
    icon: <WifiOff className="w-5 h-5" />,
    title: "Çevrimdışı Destek",
    description: "Ağ kesintilerinde bile yerel veritabanı dayanıklılığı ile operasyonlara kesintisiz devam edin."
  },
  {
    icon: <Zap className="w-5 h-5" />,
    title: "Hızlı Masaüstü Performansı",
    description: "Tarayıcı gecikmelerinden kaçınan, yerel masaüstü teknolojileri (Native) üzerine inşa edilmiştir."
  }
];

export default function FeaturesSection() {
  return (
    <section id="features" className="py-24 bg-section border-y border-border">
      <div className="container mx-auto px-6">
        <div className="max-w-2xl mb-16">
          <h2 className="text-3xl font-bold text-primary mb-4">Kapsamlı Terminal Operasyonları</h2>
          <p className="text-secondary">Bir ulaşım şirketinin günlük operasyonları verimli, güvenli ve hızlı bir şekilde yönetmesi için ihtiyaç duyduğu her şey.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {features.map((feature, idx) => (
            <div key={idx} className="bg-card border border-border p-6 rounded-lg hover:border-accent/50 transition-colors group">
              <div className="w-10 h-10 rounded-md bg-background border border-border flex items-center justify-center text-secondary group-hover:text-accent transition-colors mb-4">
                {feature.icon}
              </div>
              <h3 className="font-semibold text-primary mb-2">{feature.title}</h3>
              <p className="text-sm text-secondary leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
