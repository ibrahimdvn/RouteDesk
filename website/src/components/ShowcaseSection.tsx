import Image from "next/image";

export default function ShowcaseSection() {
  return (
    <section id="showcase" className="py-24">
      <div className="container mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-primary mb-4">Kurumsal Kontrol Paneli</h2>
          <p className="text-secondary">Tüm operasyonunuza kuşbakışı bakın. Canlı kalkışları izleyin, günlük hasılatı takip edin ve bilet iptallerini tek bir yerel (native) arayüzden yönetin.</p>
        </div>
        
        <div className="rounded-xl border border-border bg-card p-2 md:p-4 shadow-2xl mx-auto max-w-5xl">
          <Image 
            src="/screenshots/media__1779577956914.png" 
            alt="RouteDesk Main Dashboard" 
            width={1280} 
            height={800} 
            className="rounded-lg w-full h-auto object-cover border border-border/50"
          />
        </div>
      </div>
    </section>
  );
}
