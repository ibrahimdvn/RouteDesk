import { HardDrive, MousePointerClick, ShieldCheck } from "lucide-react";

export default function WhyRouteDeskSection() {
  const reasons = [
    {
      icon: <HardDrive className="w-6 h-6" />,
      title: "Masaüstü (Native) Hızı",
      desc: "Ağır web uygulamalarının aksine RouteDesk, makinenizde yerel olarak çalışır ve yoğun saatlerde bile anında yanıt süreleri sağlar."
    },
    {
      icon: <MousePointerClick className="w-6 h-6" />,
      title: "Operatörler İçin Tasarlandı",
      desc: "En az tıklama ile işlem yapılacak şekilde tasarlanmış arayüzler. Klavye dostu girişler ve hızlı açılır menüler biletlemeyi inanılmaz hızlandırır."
    },
    {
      icon: <ShieldCheck className="w-6 h-6" />,
      title: "Veri Güvenliği",
      desc: "Yerel bir SQLite veritabanı kullanarak çalışır, yani internet kesilse bile işletmeniz sorunsuz çalışmaya devam eder."
    }
  ];

  return (
    <section className="py-24 bg-section border-y border-border">
      <div className="container mx-auto px-6">
        <div className="flex flex-col lg:flex-row gap-16">
          <div className="lg:w-1/3">
            <h2 className="text-3xl font-bold text-primary mb-6">Neden RouteDesk?</h2>
            <p className="text-secondary leading-relaxed mb-8">
              Ulaşım yönetimi mutlak güvenilirlik gerektirir. Tarayıcı tabanlı araçlar ağ kesintileri sırasında gecikebilir, çökebilir veya veri kaybedebilir. RouteDesk, kurumsal düzeyde kararlılığı doğrudan terminal masasına getirir.
            </p>
          </div>
          <div className="lg:w-2/3 grid grid-cols-1 md:grid-cols-3 gap-8">
            {reasons.map((reason, idx) => (
              <div key={idx} className="flex flex-col">
                <div className="w-12 h-12 rounded-lg bg-card border border-border flex items-center justify-center text-accent mb-6">
                  {reason.icon}
                </div>
                <h3 className="font-semibold text-primary mb-3">{reason.title}</h3>
                <p className="text-sm text-secondary leading-relaxed">{reason.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
