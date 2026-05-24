import Link from "next/link";
import { BusFront } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border bg-background/80 backdrop-blur-md">
      <div className="container mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
            <BusFront className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-lg tracking-tight text-primary">RouteDesk</span>
        </div>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-secondary">
          <Link href="#features" className="hover:text-primary transition-colors">Özellikler</Link>
          <Link href="#showcase" className="hover:text-primary transition-colors">Platform</Link>
          <Link href="#workflow" className="hover:text-primary transition-colors">İş Akışı</Link>
          <Link href="#pricing" className="hover:text-primary transition-colors">Fiyatlandırma</Link>
        </div>

        <div className="flex items-center gap-4">
          <Link href="#contact" className="text-sm font-medium text-secondary hover:text-primary transition-colors hidden md:block">
            İletişim
          </Link>
          <Link href="#contact" className="text-sm font-medium bg-primary text-background px-4 py-2 rounded-md hover:bg-white transition-colors">
            Demo Talep Et
          </Link>
        </div>
      </div>
    </nav>
  );
}
