export default function PricingSection() {
  const plans = [
    {
      name: "Başlangıç",
      desc: "Bağımsız bilet ofisleri için.",
      features: ["Tek Terminal Lisansı", "Temel Koltuk Planları", "Yerel Veritabanı", "Standart Destek"]
    },
    {
      name: "İşletme",
      desc: "Büyüyen ulaşım filoları için.",
      features: ["5 Terminale Kadar", "Gelişmiş 2+1 ve 3+1 Planları", "Hasılat Analitiği", "Öncelikli Destek"],
      highlight: true
    },
    {
      name: "Kurumsal",
      desc: "Bölgesel transit ağlar için.",
      features: ["Sınırsız Terminal", "Özel Entegrasyonlar", "Ağ Veritabanı Senkronizasyonu", "Özel Müşteri Temsilcisi"]
    }
  ];

  return (
    <section id="pricing" className="py-24 bg-section border-y border-border">
      <div className="container mx-auto px-6">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-primary mb-4">Şeffaf Lisanslama</h2>
          <p className="text-secondary">Karmaşıklıktan uzak kurumsal yazılım lisanslaması.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, idx) => (
            <div key={idx} className={`p-8 rounded-xl border ${plan.highlight ? 'border-accent bg-card relative' : 'border-border bg-background'}`}>
              {plan.highlight && (
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-accent text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                  Önerilen
                </div>
              )}
              <h3 className="text-xl font-bold text-primary mb-2">{plan.name}</h3>
              <p className="text-sm text-secondary mb-8 h-10">{plan.desc}</p>
              
              <div className="mb-8">
                <span className="text-3xl font-bold text-primary">Özel</span>
                <span className="text-secondary text-sm"> / lisans</span>
              </div>
              
              <ul className="space-y-4 mb-8">
                {plan.features.map((feature, fIdx) => (
                  <li key={fIdx} className="flex items-center gap-3 text-sm text-secondary">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent"></div>
                    {feature}
                  </li>
                ))}
              </ul>
              
              <button className={`w-full py-2.5 rounded-md text-sm font-medium transition-colors ${plan.highlight ? 'bg-accent text-white hover:bg-accent/90' : 'bg-card border border-border text-primary hover:bg-border/50'}`}>
                Satış Ekibiyle Görüş
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
