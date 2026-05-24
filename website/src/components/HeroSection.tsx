import Image from "next/image";
import Link from "next/link";
import { ArrowRight, Monitor } from "lucide-react";

export default function HeroSection() {
  return (
    <section className="relative pt-24 pb-32 overflow-hidden">
      <div className="container mx-auto px-6 relative z-10">
        <div className="flex flex-col lg:flex-row items-center gap-16">
          <div className="flex-1 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-border/50 border border-border text-xs font-medium text-secondary mb-6">
              <Monitor className="w-3.5 h-3.5" />
              <span>Masaüstü Tabanlı Terminal Yönetim Sistemi</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-bold tracking-tight text-primary leading-tight mb-6">
              Modern Ulaşım Operasyon Yazılımı
            </h1>
            <p className="text-lg text-secondary mb-8 leading-relaxed">
              RouteDesk; bilet satış ofislerinin seferleri, bilet satışlarını, rezervasyonları ve özel koltuk planlarını hızlı ve masaüstü tabanlı bir yönetim sistemi üzerinden kontrol etmesini sağlar.
            </p>
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Link href="#contact" className="w-full sm:w-auto px-6 py-3 rounded-md bg-accent text-white font-medium hover:bg-accent/90 transition-colors flex items-center justify-center gap-2">
                Demo Talep Et
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link href="#features" className="w-full sm:w-auto px-6 py-3 rounded-md border border-border text-primary font-medium hover:bg-border/50 transition-colors text-center">
                Özellikleri İncele
              </Link>
            </div>
          </div>
          
          <div className="flex-1 w-full max-w-3xl">
            <div className="relative rounded-xl border border-border bg-card p-2 shadow-2xl overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-tr from-accent/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <Image 
                src="/screenshots/media__1779577969553.png" 
                alt="RouteDesk Dashboard" 
                width={1280} 
                height={800} 
                className="rounded-lg w-full h-auto object-cover border border-border/50 relative z-10"
                priority
              />
            </div>
          </div>
        </div>
      </div>
      
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-bl from-accent/5 to-transparent pointer-events-none blur-3xl"></div>
    </section>
  );
}
