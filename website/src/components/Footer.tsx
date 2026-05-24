import { BusFront } from "lucide-react";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-background pt-16 pb-8">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6 mb-12">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
              <BusFront className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg tracking-tight text-primary">RouteDesk</span>
          </div>
          
          <div className="flex gap-6 text-sm text-secondary">
            <Link href="/gizlilik" className="hover:text-primary transition-colors">Gizlilik Politikası</Link>
            <Link href="/hizmet-sartlari" className="hover:text-primary transition-colors">Hizmet Şartları</Link>
            <Link href="/cerez-politikasi" className="hover:text-primary transition-colors">Çerez Politikası</Link>
          </div>
        </div>
        
        <div className="border-t border-border/50 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-secondary">
          <p>&copy; {new Date().getFullYear()} RouteDesk Yazılım. Tüm hakları saklıdır.</p>
          <p>Profesyonel ulaşım yönetimi için tasarlandı.</p>
        </div>
      </div>
    </footer>
  );
}
