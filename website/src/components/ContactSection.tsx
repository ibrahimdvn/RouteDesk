"use client";

import { Mail, Phone, MapPin, CheckCircle2, Loader2 } from "lucide-react";
import { useState } from "react";

export default function ContactSection() {
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setStatus("submitting");
    const form = e.currentTarget;
    const data = new FormData(form);

    try {
      const response = await fetch("https://formspree.io/f/xykvplyv", {
        method: "POST",
        body: data,
        headers: {
          Accept: "application/json",
        },
      });
      
      if (response.ok) {
        setStatus("success");
        form.reset();
        setTimeout(() => setStatus("idle"), 5000);
      } else {
        setStatus("error");
        setTimeout(() => setStatus("idle"), 5000);
      }
    } catch (error) {
      setStatus("error");
      setTimeout(() => setStatus("idle"), 5000);
    }
  };

  return (
    <section id="contact" className="py-24">
      <div className="container mx-auto px-6">
        <div className="flex flex-col lg:flex-row gap-16 max-w-6xl mx-auto">
          <div className="flex-1">
            <h2 className="text-3xl font-bold text-primary mb-6">Terminal operasyonlarınızı yükseltmeye hazır mısınız?</h2>
            <p className="text-secondary leading-relaxed mb-12">
              RouteDesk'in kişiselleştirilmiş bir demosunu talep etmek veya ulaşım ağınız için özel entegrasyon gereksinimlerini görüşmek üzere kurumsal satış ekibimizle iletişime geçin.
            </p>
            
            <div className="space-y-6">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-card border border-border flex items-center justify-center text-accent">
                  <Mail className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-xs text-secondary mb-1">Satış E-posta</p>
                  <p className="text-sm font-medium text-primary">ibrahimcanduven1@gmail.com</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-card border border-border flex items-center justify-center text-accent">
                  <Phone className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-xs text-secondary mb-1">Kurumsal Telefon</p>
                  <p className="text-sm font-medium text-primary">+90 (505) 065 66 31</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-card border border-border flex items-center justify-center text-accent">
                  <MapPin className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-xs text-secondary mb-1">Merkez</p>
                  <p className="text-sm font-medium text-primary">Balıkesir, Türkiye</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex-1">
            <div className="bg-card border border-border rounded-xl p-8 relative overflow-hidden">
              <h3 className="text-xl font-bold text-primary mb-6">Demo Talep Et</h3>
              
              {status === "success" && (
                <div className="absolute inset-0 bg-card z-10 flex flex-col items-center justify-center p-8 text-center">
                  <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mb-4">
                    <CheckCircle2 className="w-8 h-8 text-accent" />
                  </div>
                  <h4 className="text-xl font-bold text-primary mb-2">Talebiniz Alındı</h4>
                  <p className="text-secondary text-sm">Satış ekibimiz en kısa sürede ibrahimcanduven1@gmail.com üzerinden sizinle iletişime geçecektir.</p>
                </div>
              )}
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-secondary">Ad</label>
                    <input name="name" required type="text" className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm text-primary focus:outline-none focus:border-accent transition-colors" placeholder="Ahmet" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-medium text-secondary">Soyad</label>
                    <input name="surname" required type="text" className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm text-primary focus:outline-none focus:border-accent transition-colors" placeholder="Yılmaz" />
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-medium text-secondary">İş E-postası</label>
                  <input name="email" required type="email" className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm text-primary focus:outline-none focus:border-accent transition-colors" placeholder="ahmet@firma.com.tr" />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-medium text-secondary">Firma Adı</label>
                  <input name="company" required type="text" className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm text-primary focus:outline-none focus:border-accent transition-colors" placeholder="Ulaşım A.Ş." />
                </div>
                
                {status === "error" && (
                  <p className="text-red-400 text-xs mt-2">Bir hata oluştu. Lütfen Formspree'yi etkinleştirdiğinizden veya endpoint'in doğru olduğundan emin olun.</p>
                )}
                
                <button 
                  type="submit" 
                  disabled={status === "submitting"}
                  className="w-full bg-accent hover:bg-accent/90 text-white font-medium py-2.5 rounded-md transition-colors mt-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {status === "submitting" ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Gönderiliyor...
                    </>
                  ) : (
                    "Talebi Gönder"
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
