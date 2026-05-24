import { PlusCircle, Search, CreditCard, CheckSquare, BarChart3 } from "lucide-react";

const steps = [
  { icon: <PlusCircle className="w-5 h-5" />, title: "Sefer Oluştur", desc: "Rota, saat ve otobüs tipini belirleyin." },
  { icon: <Search className="w-5 h-5" />, title: "Planı Görüntüle", desc: "Eşleşen koltuk düzenini anında önizleyin." },
  { icon: <CreditCard className="w-5 h-5" />, title: "Bilet Sat", desc: "Dinamik fiyatlandırma ile ödemeleri işleyin." },
  { icon: <CheckSquare className="w-5 h-5" />, title: "Durumu Yönet", desc: "Sefer durumlarını güncelleyin (Yolcu alımında, rötarlı)." },
  { icon: <BarChart3 className="w-5 h-5" />, title: "Raporlar", desc: "Günlük hasılatı dinamik olarak izleyin." }
];

export default function WorkflowSection() {
  return (
    <section id="workflow" className="py-24">
      <div className="container mx-auto px-6">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-primary mb-4">Akıcı Operasyonel İş Akışı</h2>
          <p className="text-secondary">Tempolu bilet satış ofisleri için özel olarak tasarlandı. Tıklamaları en aza indirin, hızı en üst düzeye çıkarın.</p>
        </div>
        
        <div className="relative">
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-px bg-border -translate-y-1/2 z-0"></div>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-8 relative z-10">
            {steps.map((step, idx) => (
              <div key={idx} className="flex flex-col items-center text-center bg-background md:bg-transparent">
                <div className="w-12 h-12 rounded-full bg-card border border-border flex items-center justify-center text-accent mb-4 shadow-sm relative z-10">
                  {step.icon}
                </div>
                <h3 className="font-semibold text-primary mb-2">{step.title}</h3>
                <p className="text-sm text-secondary">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
